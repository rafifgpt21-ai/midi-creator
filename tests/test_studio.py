"""Check transport boundaries and real drum/MCP artifacts without opening Cubase."""

import json
from datetime import timedelta
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from pedalboard.io import AudioFile
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from midi_creator.studio.config import StudioError, defaults, load_config, save_json
from midi_creator.studio.drums import approved_sample
from midi_creator.studio.protocol import Assembler, frames
from midi_creator.studio.session import prepare_session, verify_session

ROOT = Path(__file__).resolve().parents[1]


class ProtocolTests(unittest.TestCase):
    def test_unicode_reordered_chunks_and_echo_isolation(self):
        value = {"title": "夜の音 🎹", "data": "x" * 2000}
        packets = frames(value, 231, 1)
        reader = Assembler(231, 1)
        self.assertIsNone(reader.feed(frames({"operation": "save"}, 231, 0)[0]))
        self.assertIsNone(reader.feed(frames(value, 232, 1)[0]))
        result = None
        for packet in reversed(packets):
            self.assertTrue(all(0 <= byte < 128 for byte in packet))
            result = reader.feed(packet)
        self.assertEqual(result, value)

    def test_conflicting_chunks_and_oversized_message_are_rejected(self):
        packets = frames({"data": "x" * 1000}, 1, 0)
        reader = Assembler(1, 0)
        reader.feed(packets[0])
        with self.assertRaises(StudioError):
            reader.feed(packets[0][:-1] + (65,))
        with self.assertRaises(StudioError):
            frames({"data": "x" * 131072}, 1, 0)


class StudioFixture:
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        self.root = self.folder / "workspace"
        self.root.mkdir()
        samples = self.root / "samples"
        samples.mkdir()
        self.sample = samples / "kick.wav"
        # Known nonzero, short signal; first hit deliberately starts late.
        with AudioFile(str(self.sample), "w", 44100, 1, bit_depth=24) as stream:
            stream.write(np.full((1, 4410), 0.3, dtype=np.float32))
        data = defaults(self.root)
        data.update(drum_roots=[str(samples)], drum_samples={"36": str(self.sample)})
        self.config_path = self.root / "studio.local.json"
        save_json(self.config_path, data)
        self.config = load_config(self.config_path)
        self.spec = self.root / "composition.json"
        source = {"version": 1, "title": "Late drum", "tempo_bpm": 110,
                  "time_signature": [4, 4], "bars": 2,
                  "layers": [{"id": "kick", "name": "Kick", "kind": "drums",
                              "notes": [{"pitch": 36, "start": 2, "duration": 0.1, "velocity": 60},
                                        {"pitch": 36, "start": 4, "duration": 0.1, "velocity": 120}]}]}
        save_json(self.spec, source)


class BundleTests(StudioFixture, unittest.TestCase):
    def test_real_sample_render_preserves_silence_velocity_and_length(self):
        result = prepare_session(self.config, "composition.json", "bundle")
        self.assertTrue(result["ok"])
        bundle = self.root / "bundle"
        self.assertTrue(verify_session(bundle)["ok"])
        with AudioFile(str(bundle / "audio/kick.wav")) as stream:
            audio = stream.read(stream.frames)
            self.assertEqual(stream.frames, round(8 * 545455 / 1e6 * 48000))
            self.assertEqual(stream.num_channels, 2)
        first = round(2 * 545455 / 1e6 * 48000)
        second = round(4 * 545455 / 1e6 * 48000)
        self.assertEqual(float(np.max(np.abs(audio[:, :first]))), 0)
        self.assertGreater(float(audio[0, first + 20]), 0)
        self.assertAlmostEqual(float(audio[0, second + 20] / audio[0, first + 20]), 2, places=4)
        self.assertFalse((bundle / "MIDI/arrangement.mid").exists())
        self.assertTrue((bundle / "README.md").is_file())
        self.assertTrue((bundle / "_internal/session.json").is_file())
        with self.assertRaises(StudioError):
            prepare_session(self.config, "composition.json", "bundle")
        with (bundle / "Drums/36-kick.wav").open("ab") as stream:
            stream.write(b"tamper")
        self.assertFalse(verify_session(bundle)["ok"])

    def test_missing_mapping_publishes_nothing(self):
        self.config.data["drum_samples"] = {}
        with self.assertRaisesRegex(StudioError, "36"):
            prepare_session(self.config, "composition.json", "bundle")
        self.assertFalse((self.root / "bundle").exists())

    def test_artifact_and_sample_paths_cannot_escape(self):
        with self.assertRaises(StudioError):
            self.config.artifact("../outside")
        outside = self.folder / "outside.wav"
        shutil.copy2(self.sample, outside)
        with self.assertRaises(StudioError):
            approved_sample(self.config, str(outside))
        try:
            (self.root / "escape").symlink_to(self.folder, target_is_directory=True)
        except OSError:
            return  # Windows may require developer mode to create symlinks.
        with self.assertRaises(StudioError):
            self.config.artifact("escape/outside.wav")

    def test_remote_host_contract(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node unavailable for MIDI Remote host mock")
        result = subprocess.run([node, str(ROOT / "tests/cubase_remote.test.cjs")],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class MCPTests(StudioFixture, unittest.IsolatedAsyncioTestCase):
    async def test_stdio_initialize_real_export_and_scope_error(self):
        params = StdioServerParameters(command=sys.executable,
                 args=["-m", "midi_creator.studio.mcp_server", "--config", str(self.config_path)],
                 cwd=str(ROOT))
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as client:
                await client.initialize()
                tools = await client.list_tools()
                self.assertEqual(len(tools.tools), 20)
                self.assertIn("cubase_assign_serum", {tool.name for tool in tools.tools})
                validated = await client.call_tool("validate_composition", {"spec_path": "composition.json"})
                self.assertFalse(validated.isError)
                generated = await client.call_tool("generate_midi", {"spec_path": "composition.json", "output": "mcp-midi"})
                self.assertFalse(generated.isError)
                verified = await client.call_tool("verify_midi", {"folder": "mcp-midi"})
                self.assertFalse(verified.isError)
                self.assertTrue((verified.structuredContent or json.loads(verified.content[0].text))["ok"])
                refused = await client.call_tool("generate_midi", {"spec_path": "composition.json", "output": "../outside"})
                self.assertTrue(refused.isError)
                prepared = await client.call_tool("prepare_cubase_session", {"spec_path": "composition.json", "output": "mcp-bundle"})
                self.assertFalse(prepared.isError)
                checked = await client.call_tool("verify_cubase_session", {"folder": "mcp-bundle"})
                self.assertFalse(checked.isError)
                self.assertTrue((checked.structuredContent or json.loads(checked.content[0].text))["ok"])


@unittest.skipUnless(os.environ.get("MIDI_STUDIO_TEST_CONFIG"), "Opt-in installed Serum integration")
class InstalledSerumTests(unittest.IsolatedAsyncioTestCase):
    async def test_mcp_worker_starts_with_private_stdin_and_saves_real_state(self):
        # Exercises the Windows JSON-RPC pipe -> child-process startup regression.
        config = load_config(Path(os.environ["MIDI_STUDIO_TEST_CONFIG"]))
        params = StdioServerParameters(command=sys.executable,
                 args=["-m", "midi_creator.studio.mcp_server", "--config", str(config.path)],
                 cwd=str(config.workspace))
        with tempfile.TemporaryDirectory(prefix=".studio-integration-", dir=config.workspace) as temporary:
            destination = Path(temporary).resolve()
            self.assertTrue(destination.is_relative_to(config.workspace))
            async with stdio_client(params) as (reader, writer):
                async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=60)) as client:
                    await client.initialize()
                    inspected = await client.call_tool("serum_parameters", {"query": "main_vol", "limit": 1})
                    self.assertFalse(inspected.isError)
                    data = inspected.structuredContent or json.loads(inspected.content[0].text)
                    self.assertEqual(data["plugin"], config.data["serum_plugin_name"])
                    created = await client.call_tool("create_serum_preset", {"profile": "lead",
                        "output": str(destination / "lead")})
                    self.assertFalse(created.isError)
                    preset = destination / "lead/preset.vstpreset"
                    self.assertEqual(preset.read_bytes()[:4], b"VST3")
                    receipt = json.loads((destination / "lead/recipe.json").read_text())
                    self.assertTrue(receipt["presets"][0]["round_trip_verified"])


if __name__ == "__main__":
    unittest.main()

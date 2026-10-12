"""MCP tools backed by the same checked operations as the studio CLI."""

import argparse
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from midi_creator.export import generate_export, verify_export
from midi_creator.spec import compile_composition, load_json, schema
from midi_creator.timing import timing_report
from .config import load_config
from .serum import run_serum
from .service import Studio
from .session import prepare_session, verify_session


def make_server(config_path: Path):
    server = FastMCP("MIDI Studio", instructions="Prepare Cubase sessions with Serum and explicit drum mappings. "
                     "Call studio_status first. Cubase tools require a live response; an acknowledgment is not proof of effect. "
                     "Preserve previous output folders. Native .cpr creation and file import require Cubase UI setup.")

    def studio():
        return Studio(load_config(config_path))

    @server.tool()
    def studio_status(check_cubase: bool = False) -> dict:
        """Inspect configured Serum, sample roots, MIDI ports, and optional Cubase handshake."""
        return studio().doctor(live=check_cubase)

    @server.tool()
    def composition_schema() -> dict:
        """Get the authoritative performance specification for synchronized MIDI layers."""
        return schema()

    @server.tool()
    def validate_composition(spec_path: str) -> dict:
        """Validate a workspace composition before exporting it."""
        config = studio().config
        composition = compile_composition(load_json(config.artifact(spec_path, must_exist=True)), strict_timing=True)
        return {"ok": True, "layers": len(composition.layers), "duration_seconds": composition.seconds,
                "timing": timing_report(composition)}

    @server.tool()
    def generate_midi(spec_path: str, output: str, combined: bool = False) -> dict:
        """Export one aligned MIDI per instrument. Set combined only if the user requested it."""
        config = studio().config
        return generate_export(config.artifact(spec_path, must_exist=True), config.artifact(output), combined=combined)

    @server.tool()
    def verify_midi(folder: str) -> dict:
        """Reopen MIDI files and verify alignment, single-instrument layers, and checksums."""
        return verify_export(studio().config.artifact(folder, must_exist=True))

    @server.tool()
    def serum_parameters(query: str = "", limit: int = 50) -> dict:
        """Inspect installed Serum parameter names, current display values, and normalized values."""
        if not 1 <= limit <= 100:
            raise ValueError("limit must be 1..100")
        return run_serum(studio().config, "inspect", query=query, limit=limit)

    @server.tool()
    def serum_presets(query: str = "", limit: int = 100) -> dict:
        """Find existing Serum presets; report which formats can be loaded by the offline host."""
        return studio().preset_catalog(query, limit)

    @server.tool()
    def create_serum_preset(output: str, profile: str = "lead", parameters: dict | None = None,
                            base_preset: str | None = None) -> dict:
        """Create a real .vstpreset in a NEW folder, then reload it in Serum. raw values use {'raw': 0..1}."""
        return studio().create_preset(output, profile, parameters, base_preset)

    @server.tool()
    def find_drum_samples(query: str = "", limit: int = 100) -> dict:
        """Read-only filename search across configured sample roots; excludes obvious loops."""
        return studio().sample_catalog(query, limit)

    @server.tool()
    def configure_drums(roots: list[str], samples: dict[str, str] | None = None) -> dict:
        """Set approved sample roots and an explicit mapping of MIDI pitches to one-shot files."""
        return studio().configure_drums(roots, samples)

    @server.tool()
    def prepare_cubase_session(spec_path: str, output: str, bindings: dict[str, str] | None = None,
                                render_audio: bool = True) -> dict:
        """Publish aligned MIDI, reloaded Serum presets, drum kit samples, and optional real audio stems. No .cpr is claimed."""
        return prepare_session(studio().config, spec_path, output, bindings, render_audio=render_audio)

    @server.tool()
    def verify_cubase_session(folder: str) -> dict:
        """Verify bundle checksums, MIDI structure, and audio frame alignment."""
        return verify_session(studio().config.artifact(folder, must_exist=True))

    @server.tool()
    def cubase_status() -> dict:
        """Request a real Cubase handshake and report instrument tracks and supported live functions."""
        return studio().cubase.status()

    @server.tool()
    def cubase_objects() -> dict:
        """Discover the selected track's runtime objects and a short-lived identity token."""
        return studio().cubase.request("objects")

    @server.tool()
    def cubase_parameters(object_id: int, token: str, query: str = "", offset: int = 0, limit: int = 50) -> dict:
        """List current parameters on a freshly discovered Cubase object. Tokens expire after 30 seconds."""
        return studio().cubase.request("parameters", object_id=object_id, token=token, query=query, offset=offset, limit=limit)

    @server.tool()
    def cubase_set_parameters(object_id: int, token: str, values: list[dict]) -> dict:
        """Write explicit parameter tags and normalized raw values. Return actual readback and verification status."""
        return studio().cubase.request("set_parameters", object_id=object_id, token=token, values=values)

    @server.tool()
    def cubase_slot_plugins(object_id: int, token: str) -> dict:
        """List plugins eligible for a discovered plugin slot, using MIDI Remote API 1.3."""
        return studio().cubase.request("plugins", object_id=object_id, token=token)

    @server.tool()
    def cubase_assign_serum(object_id: int, token: str, plugin_uid: str, replace_existing: bool = False) -> dict:
        """Assign the configured Serum instrument to a discovered slot. Rediscover afterward to verify it."""
        return studio().cubase.request("assign_serum", object_id=object_id, token=token,
                                       plugin_uid=plugin_uid, replace_existing=replace_existing)

    @server.tool()
    def cubase_select_instrument(index: int) -> dict:
        """Select one of the first 16 instrument tracks returned by cubase_status; verify selection afterward."""
        return studio().cubase.request("select_track", index=index)

    @server.tool()
    def cubase_command(action: str) -> dict:
        """Dispatch play, stop, rewind, or save. Check transport/file state afterward; Save can open a dialog."""
        return studio().cubase.request("command", action=action)

    return server


def run(config_path: Path | None = None):
    config = load_config(config_path)
    make_server(config.path).run(transport="stdio")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path)
    run(parser.parse_args().config)

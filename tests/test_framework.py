"""Exercise musical timing and exported files, not just JSON serialization."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import mido

from midi_creator.export import generate_export, verify_export
from midi_creator.midi import check_rendered, inspect_midi, render_midi
from midi_creator.spec import CompositionError, compile_composition, load_json, pitch_number


ROOT = Path(__file__).resolve().parents[1]


def basic():
    return {
        "version": 1, "title": "Fixture", "tempo_bpm": 120,
        "time_signature": [4, 4], "bars": 2, "key_signature": "C",
        "layers": [{"id": "piano", "name": "Piano", "kind": "melodic", "program": 0,
                    "notes": [{"pitch": "C4", "start": 2, "duration": 1, "velocity": 90}]}],
    }


def absolute_messages(track):
    absolute = 0
    for message in track:
        absolute += message.time
        yield absolute, message


class ExportTests(unittest.TestCase):
    def test_orchestral_controls_survive_export_and_precede_note_attack(self):
        source = basic()
        source['layers'][0]['control_changes'] = [
            {'start': 0, 'control': 11, 'value': 90},
            {'start': 2, 'control': 1, 'value': 45},
            {'start': 2.01, 'control': 11, 'value': 105},
            {'start': 8, 'control': 1, 'value': 0},
        ]
        output = self.export(source)
        path = output / 'MIDI/piano.mid'
        midi = mido.MidiFile(path)
        events = list(absolute_messages(midi.tracks[0]))
        controls = [(t, m.control, m.value) for t, m in events if m.type == 'control_change']
        self.assertEqual(controls, [(0, 7, 100), (0, 10, 64), (0, 11, 90),
                                    (960, 1, 45), (965, 11, 105), (3840, 1, 0)])
        self.assertEqual([m.type for t, m in events if t == 960], ['control_change', 'note_on'])
        self.assertTrue(verify_export(output)['ok'])
        for message in midi.tracks[0]:
            if message.type == 'control_change' and message.control == 1:
                message.value += 1
                break
        midi.save(path)
        composition = compile_composition(source)
        report = check_rendered(path, composition, composition.layers, single_track=True)
        self.assertFalse(report['ok'])
        self.assertTrue(any('controller automation' in e for e in report['errors']))

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)

    def export(self, source=None, *, combined=False, name="output"):
        path = self.folder / "composition.json"
        path.write_text(json.dumps(source or basic(), ensure_ascii=False), encoding="utf-8")
        output = self.folder / name
        generate_export(path, output, combined=combined)
        return output

    def test_cubase_layer_has_one_track_and_only_import_metadata(self):
        source = basic()
        source['sections'] = [{'name': 'Intro', 'start': 0}, {'name': 'Verse', 'start': 4}]
        from io import BytesIO
        midi = mido.MidiFile(file=BytesIO(render_midi(compile_composition(source),
                            compile_composition(source).layers, single_track=True)))
        self.assertEqual(midi.type, 1)
        self.assertEqual(len(midi.tracks), 1)
        self.assertEqual({message.type for message in midi.tracks[0] if message.is_meta},
                         {'track_name', 'set_tempo', 'time_signature', 'end_of_track'})
        self.assertFalse(any(message.type in ('sysex', 'program_change') for message in midi.tracks[0]))
        self.assertEqual(sum(message.time for message in midi.tracks[0]), 3840)

    def test_producer_layout_and_readme_keep_technical_files_together(self):
        output = self.export()
        self.assertEqual({path.name for path in output.iterdir()}, {'README.md', 'MIDI', '_internal'})
        self.assertEqual({path.name for path in (output / '_internal').iterdir()},
                         {'composition.json', 'manifest.json', 'validation.json', 'summary.md'})
        text = (output / 'README.md').read_text(encoding='utf-8')
        for required in ('Serum 2', 'Drum yang disarankan', 'Instrumen di luar Serum', 'MIDI/piano.mid'):
            self.assertIn(required, text)

    def test_original_v1_exports_remain_verifiable(self):
        for example in ('single-layer', 'multi-layer'):
            with self.subTest(example=example):
                self.assertTrue(verify_export(ROOT / 'examples' / example / 'output')['ok'])

    def test_per_layer_is_one_track_one_instrument_with_silence_and_metadata(self):
        output = self.export()
        midi = mido.MidiFile(output / "MIDI/piano.mid")
        self.assertEqual(midi.type, 1)
        self.assertEqual(len(midi.tracks), 1)
        self.assertEqual(midi.tracks[0].name, "Piano")
        events = list(absolute_messages(midi.tracks[0]))
        self.assertEqual([(t, m.note) for t, m in events if m.type == "note_on"], [(960, 60)])
        self.assertEqual([(t, m.note) for t, m in events if m.type == "note_off"], [(1440, 60)])
        self.assertEqual(events[-1][0], 3840)
        self.assertAlmostEqual(midi.length, 4.0)
        self.assertEqual([m.tempo for _, m in events if m.type == "set_tempo"], [500000])
        self.assertEqual([m.key for _, m in events if m.type == "key_signature"], [])
        self.assertEqual([m.program for _, m in events if m.type == "program_change"], [])
        self.assertFalse((output / "MIDI/arrangement.mid").exists())
        self.assertTrue(verify_export(output)["ok"])

    def test_all_layer_lengths_match_even_if_they_enter_late(self):
        source = basic()
        second = deepcopy(source["layers"][0])
        second.update(id="bass", name="Bass", program=33)
        second["notes"][0].update(pitch="C2", start=6, duration=0.5)
        source["layers"].append(second)
        output = self.export(source)
        midi_files = list((output / "MIDI").glob("*.mid"))
        self.assertEqual(len(midi_files), 2)
        for path in midi_files:
            midi = mido.MidiFile(path)
            self.assertEqual(sum(m.time for m in midi.tracks[0]), 3840)
            self.assertAlmostEqual(midi.length, 4)

    def test_compound_meter_and_quarter_note_tempo(self):
        source = basic()
        source.update(time_signature=[6, 8], bars=2)
        midi = mido.MidiFile(self.export(source) / "MIDI/piano.mid")
        self.assertEqual(sum(m.time for m in midi.tracks[0]), 6 * 480)
        self.assertAlmostEqual(midi.length, 3)

    def test_clips_retrigger_release_before_note_on(self):
        source = basic()
        layer = source["layers"][0]
        layer.pop("notes")
        layer["clips"] = [{"start": 0, "repeat": 8, "every": 1,
                           "notes": [{"pitch": 60, "start": 0, "duration": 1}]}]
        midi = mido.MidiFile(self.export(source) / "MIDI/piano.mid")
        at_boundary = [m.type for t, m in absolute_messages(midi.tracks[0])
                       if t == 480 and m.type in ("note_on", "note_off")]
        self.assertEqual(at_boundary, ["note_off", "note_on"])
        self.assertEqual(sum(m.type == "note_on" for m in midi.tracks[0]), 8)

    def test_chord_polyphony(self):
        source = basic()
        source["layers"][0]["notes"] = [{"pitch": p, "start": 0, "duration": 2} for p in [60, 64, 67]]
        report = inspect_midi(self.export(source) / "MIDI/piano.mid")
        self.assertTrue(report["ok"])
        self.assertEqual(report["tracks"][0]["peak_polyphony"], 3)

    def test_separate_kick_and_hihat_have_channel_ten_no_program(self):
        source = basic()
        source["layers"] = [{"id": identifier, "name": identifier, "kind": "drums", "pan": pan,
                             "notes": [{"pitch": pitch, "start": 0, "duration": 0.2}]}
                            for identifier, pitch, pan in [("kick", 36, 64), ("hihat", 42, 90)]]
        output = self.export(source)
        for path in (output / "MIDI").glob("*.mid"):
            midi = mido.MidiFile(path)
            self.assertEqual(len(midi.tracks), 1)
            self.assertEqual({m.channel for m in midi.tracks[0] if hasattr(m, "channel")}, {9})
            self.assertFalse(any(m.type == "program_change" for m in midi.tracks[0]))
        self.assertTrue(verify_export(output)["ok"])

    def test_combined_is_optional_and_reserves_explicit_channel(self):
        source = basic()
        second = deepcopy(source["layers"][0])
        second.update(id="bass", name="Bass", program=33, channel=1)
        source["layers"].append(second)
        output = self.export(source, combined=True)
        midi = mido.MidiFile(output / "MIDI/arrangement.mid")
        self.assertEqual(midi.type, 1)
        self.assertEqual(len(midi.tracks), 3)
        self.assertEqual({m.channel for m in midi.tracks[1] if hasattr(m, "channel")}, {1})
        self.assertEqual({m.channel for m in midi.tracks[2] if hasattr(m, "channel")}, {0})
        self.assertTrue(verify_export(output)["ok"])

    def test_many_instruments_in_independent_files(self):
        source = basic()
        source["layers"] = [dict(deepcopy(source["layers"][0]), id=f"instrument-{i}") for i in range(20)]
        output = self.export(source)
        self.assertEqual(len(list((output / "MIDI").glob("*.mid"))), 20)
        self.assertTrue(verify_export(output)["ok"])
        with self.assertRaisesRegex(CompositionError, "15 melodic"):
            compile_composition(source, combined=True)

    def test_track_name_unicode(self):
        source = basic()
        source["layers"][0]["name"] = "Biola — lembut 🎻"
        output = self.export(source)
        midi = mido.MidiFile(output / "MIDI/piano.mid", charset="utf-8")
        self.assertEqual(midi.tracks[0].name, source["layers"][0]["name"])

    def test_existing_output_is_preserved(self):
        output = self.export()
        original = (output / "_internal/manifest.json").read_bytes()
        with self.assertRaisesRegex(CompositionError, "already exists"):
            generate_export(self.folder / "composition.json", output)
        self.assertEqual((output / "_internal/manifest.json").read_bytes(), original)

    def test_invalid_input_does_not_publish_output(self):
        source = basic()
        source["layers"][0]["notes"][0]["duration"] = 20
        with self.assertRaises(CompositionError):
            self.export(source)
        self.assertFalse((self.folder / "output").exists())

    def test_verify_detects_tampered_note_and_missing_file(self):
        output = self.export()
        path = output / "MIDI/piano.mid"
        midi = mido.MidiFile(path)
        for m in midi.tracks[0]:
            if m.type in ("note_on", "note_off"):
                m.note += 1
        midi.save(path)
        report = verify_export(output)
        self.assertFalse(report["ok"])
        self.assertTrue(any("differ from the composition" in error for error in report["errors"]))
        path.unlink()
        self.assertFalse(verify_export(output)["ok"])

    def test_verify_rejects_unsafe_inventory(self):
        output = self.export()
        manifest_path = output / "_internal/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["files"][0]["path"] = "../../outside.mid"
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(CompositionError, "inventory"):
            verify_export(output)

    def test_verify_detects_added_midi_and_snapshot_change(self):
        output = self.export()
        (output / "MIDI/extra.mid").write_bytes((output / "MIDI/piano.mid").read_bytes())
        self.assertFalse(verify_export(output)["ok"])
        (output / "MIDI/extra.mid").unlink()
        snapshot = output / "_internal/composition.json"
        snapshot.write_bytes(snapshot.read_bytes() + b"\n")
        self.assertFalse(verify_export(output)["ok"])

    def test_inspect_reports_stuck_notes_and_truncated_midi(self):
        midi = mido.MidiFile(type=0)
        track = mido.MidiTrack([mido.Message("note_on", note=60, velocity=90), mido.MetaMessage("end_of_track", time=480)])
        midi.tracks.append(track)
        path = self.folder / "stuck.mid"
        midi.save(path)
        self.assertFalse(inspect_midi(path)["ok"])
        path.write_bytes(b"MThd")
        self.assertFalse(inspect_midi(path)["ok"])

    def test_cli_returns_nonzero_for_invalid_spec(self):
        path = self.folder / "invalid.json"
        path.write_text('{"version": 1}')
        result = subprocess.run([sys.executable, "-m", "midi_creator", "validate", str(path)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error:", result.stderr)

    def test_example_specs_export_and_reopen(self):
        for example in ["single-layer", "multi-layer"]:
            with self.subTest(example=example):
                output = self.folder / example
                generate_export(ROOT / "examples" / example / "composition.json", output)
                self.assertTrue(verify_export(output)["ok"])

    def test_new_export_rejects_unrequested_off_grid_layer(self):
        source = basic()
        drums = {"id": "hat", "name": "Hat", "kind": "drums",
                 "notes": [{"pitch": 42, "start": 1.002, "duration": .1}]}
        source["ticks_per_beat"] = 960
        source["layers"].append(drums)
        with self.assertRaisesRegex(CompositionError, "off-grid"):
            self.export(source)
        self.assertFalse((self.folder / 'output').exists())

    def test_explicit_free_timing_preserves_intentional_swing_and_reports_it(self):
        source = basic()
        source['timing'] = {'mode': 'free', 'grid_division': 16}
        source['layers'][0]['notes'][0].update(start=.3, duration=.1)
        output = self.export(source)
        midi = mido.MidiFile(output / 'MIDI/piano.mid')
        self.assertEqual([t for t,m in absolute_messages(midi.tracks[0]) if m.type == 'note_on'], [144])
        report = verify_export(output)
        self.assertTrue(report['ok'])
        self.assertFalse(report['timing']['on_grid'])
        self.assertEqual(report['timing']['off_grid_note_ons'], 1)

    def test_grid_resolves_absolute_clips_without_tempo_or_layer_drift(self):
        source = basic()
        source.update(bars=120, tempo_bpm=118, ticks_per_beat=960,
                      timing={'mode': 'strict', 'grid_division': 32})
        source['layers'][0].pop('notes')
        source['layers'][0]['clips'] = [{'start': 0, 'repeat': 120, 'every': 4,
            'notes': [{'pitch': 60, 'start': .125, 'duration': .1}]}]
        source['layers'].append({'id': 'late-bass', 'name': 'Late Bass', 'kind': 'melodic', 'program': 33,
            'notes': [{'pitch': 30, 'start': 400.125, 'duration': .23}]})
        output = self.export(source)
        report = verify_export(output)
        self.assertTrue(report['ok'])
        self.assertTrue(report['timing']['on_grid'])
        for layer in source['layers']:
            midi = mido.MidiFile(output / 'MIDI' / (layer['id']+'.mid'))
            ons = [t for t,m in absolute_messages(midi.tracks[0]) if m.type == 'note_on']
            if layer['id'] == 'piano':
                self.assertEqual(ons, [bar*3840+120 for bar in range(120)])
            else:
                self.assertEqual(ons, [384120])
            self.assertEqual(sum(m.time for m in midi.tracks[0]), 460800)
            self.assertEqual([m.tempo for m in midi.tracks[0] if m.type == 'set_tempo'], [508475])

    def test_validate_cli_catches_the_same_off_grid_source_as_generate(self):
        source = basic()
        source['layers'][0]['notes'][0]['start'] = 1.002
        source['ticks_per_beat'] = 960
        path = self.folder / 'bad-grid.json'
        path.write_text(json.dumps(source), encoding='utf-8')
        result = subprocess.run([sys.executable, '-m', 'midi_creator', 'validate', str(path)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('off-grid', result.stderr)

    def test_grid_allows_note_gates_and_half_tick_rounding(self):
        source = basic()
        source.update(ticks_per_beat=100, timing={'mode': 'strict', 'grid_division': 32})
        source['layers'][0]['notes'][0].update(start=.125, duration=.23)
        output = self.export(source)
        self.assertTrue(verify_export(output)['timing']['on_grid'])

    def test_grid_checks_absolute_clip_offset_not_only_local_pattern(self):
        source = basic()
        source['layers'][0].pop('notes')
        source['layers'][0]['clips'] = [{'start': .01, 'repeat': 2, 'every': 1,
                                        'notes': [{'pitch': 60, 'start': 0, 'duration': .1}]}]
        with self.assertRaisesRegex(CompositionError, 'off-grid'):
            self.export(source)


class ContractTests(unittest.TestCase):
    def test_controller_bounds_reserved_controls_and_tick_collisions(self):
        for event in [
            {'start': 8.01, 'control': 1, 'value': 90},
            {'start': -1, 'control': 1, 'value': 90},
            {'start': 0, 'control': 32, 'value': 90},
            {'start': 0, 'control': 7, 'value': 90},
            {'start': 0, 'control': 11, 'value': 128},
        ]:
            source = basic()
            source['layers'][0]['control_changes'] = [event]
            with self.subTest(event=event), self.assertRaises(CompositionError):
                compile_composition(source)
        source = basic()
        source['layers'][0]['control_changes'] = [
            {'start': 2, 'control': 1, 'value': 40},
            {'start': 2.0001, 'control': 1, 'value': 60},
        ]
        with self.assertRaisesRegex(CompositionError, 'duplicate controller'):
            compile_composition(source)

    def test_combined_drums_reject_conflicting_controller_curves(self):
        source = basic()
        source['layers'] = [
            {'id': 'bass-drum', 'name': 'Bass drum', 'kind': 'drums',
             'notes': [{'pitch': 36, 'start': 0, 'duration': .1}]},
            {'id': 'snare', 'name': 'Snare', 'kind': 'drums',
             'notes': [{'pitch': 40, 'start': 0, 'duration': .1}],
             'control_changes': [{'start': 0, 'control': 11, 'value': 90}]},
        ]
        compile_composition(source)
        with self.assertRaisesRegex(CompositionError, 'same control automation'):
            compile_composition(source, combined=True)

    def test_pitch_names_and_boundaries(self):
        for name, number in [("C4", 60), ("A4", 69), ("Bb2", 46), ("C-1", 0), ("G9", 127)]:
            self.assertEqual(pitch_number(name), number)
        for value in ["C10", "C-2", "H4", 128, -1]:
            with self.subTest(value=value), self.assertRaises(CompositionError):
                pitch_number(value)

    def test_schema_rejects_invalid_notes_and_layer_fields(self):
        for field, value in [("velocity", 0), ("velocity", 128), ("duration", 0),
                             ("start", -1), ("pitch", True), ("pitch", 128), ("typo", 1)]:
            source = basic()
            source["layers"][0]["notes"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(CompositionError):
                compile_composition(source)
        for update in [{"channel": 10}, {"program": 128}, {"id": "../piano"}, {"id": "con"}, {"id": "piano\n"}]:
            source = basic()
            source["layers"][0].update(update)
            with self.subTest(update=update), self.assertRaises(CompositionError):
                compile_composition(source)

    def test_layer_ids_empty_layer_and_duplicate_pitch(self):
        source = basic()
        source["layers"].append(deepcopy(source["layers"][0]))
        with self.assertRaisesRegex(CompositionError, "Duplicate layer"):
            compile_composition(source)
        source = basic()
        source["layers"][0]["notes"] = []
        with self.assertRaises(CompositionError):
            compile_composition(source)
        source = basic()
        source["layers"][0]["notes"].append(dict(source["layers"][0]["notes"][0], start=2.5))
        with self.assertRaisesRegex(CompositionError, "overlapping"):
            compile_composition(source)

    def test_note_bounds_and_zero_tick_duration(self):
        for start, duration in [(7.9, 1), (2, 0.0001)]:
            source = basic()
            source["layers"][0]["notes"][0].update(start=start, duration=duration)
            with self.subTest(start=start), self.assertRaises(CompositionError):
                compile_composition(source)

    def test_clip_requires_interval_and_checks_overlap_and_bounds(self):
        for every in [None, 0.5, 4]:
            source = basic()
            source["layers"][0].pop("notes")
            clip = {"start": 0, "repeat": 3, "notes": [{"pitch": 60, "start": 0, "duration": 1}]}
            if every is not None:
                clip["every"] = every
            source["layers"][0]["clips"] = [clip]
            with self.subTest(every=every), self.assertRaises(CompositionError):
                compile_composition(source)

    def test_shared_drum_channels_are_checked_only_for_combined(self):
        for change in ["pan", "overlap"]:
            source = basic()
            source["layers"] = [
                {"id": "kick", "name": "Kick", "kind": "drums", "notes": [{"pitch": 36, "start": 0, "duration": 1}]},
                {"id": "snare", "name": "Snare", "kind": "drums", "notes": [{"pitch": 38, "start": 0, "duration": 1}]},
            ]
            if change == "pan":
                source["layers"][1]["pan"] = 70
            else:
                source["layers"][1]["notes"][0]["pitch"] = 36
            compile_composition(source)
            with self.subTest(change=change), self.assertRaises(CompositionError):
                compile_composition(source, combined=True)

    def test_integer_valued_json_numbers_are_supported(self):
        source = basic()
        source.update(bars=2.0, ticks_per_beat=480.0, time_signature=[4.0, 4.0])
        source["layers"][0].update(program=0.0, channel=1.0, volume=100.0, pan=64.0)
        source["layers"][0]["notes"][0].update(pitch=60.0, velocity=90.0)
        self.assertEqual(compile_composition(source).layers[0].notes[0].pitch, 60)

    def test_sections_out_of_bounds(self):
        source = basic()
        source["sections"] = [{"name": "Too late", "start": 8}]
        with self.assertRaisesRegex(CompositionError, "Section"):
            compile_composition(source)

    def test_json_duplicate_keys_nonfinite_and_bom(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "spec.json"
            for content in ['{"version": 1, "version": 2}', '{"tempo_bpm": NaN}', '{"tempo_bpm": Infinity}']:
                path.write_text(content)
                with self.subTest(content=content), self.assertRaises(CompositionError):
                    load_json(path)
            path.write_text(json.dumps(basic()), encoding="utf-8-sig")
            self.assertEqual(load_json(path)["version"], 1)


if __name__ == "__main__":
    unittest.main()

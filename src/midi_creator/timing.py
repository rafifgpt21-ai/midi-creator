"""Check musical note-on positions separately from structural MIDI validity.

Note lengths are articulation gates and need not lie on the onset grid. Grid
positions are calculated absolutely, so repeated clips cannot accumulate drift.
"""
from decimal import Decimal

from .spec import Composition, CompositionError, ticks


def timing_report(composition: Composition) -> dict:
    policy = composition.source.get('timing', {})
    division = int(policy.get('grid_division', 32))
    ppqn = composition.ppqn
    layers = []
    for layer in composition.layers:
        count = 0
        examples = []
        for note in layer.notes:
            # Positive half-up rounding to the nearest musical grid point,
            # then the same half-up tick rounding used by the MIDI compiler.
            numerator, denominator = note.start * division, ppqn * 4
            index = (2 * numerator + denominator) // (2 * denominator)
            expected = ticks(Decimal(index * 4) / division, ppqn)
            if note.start != expected:
                count += 1
                if len(examples) < 5:
                    examples.append({'pitch': note.pitch, 'tick': note.start,
                                     'beat': note.start / ppqn, 'nearest_grid_tick': expected,
                                     'offset_ticks': note.start - expected})
        layers.append({'id': layer.id, 'note_ons': len(layer.notes),
                       'off_grid_note_ons': count, 'examples': examples})
    count = sum(layer['off_grid_note_ons'] for layer in layers)
    return {'mode': policy.get('mode', 'undeclared'), 'grid_division': division,
            'on_grid': count == 0, 'off_grid_note_ons': count, 'layers': layers,
            'scope': 'note-on positions; note-off gates may be shorter than the grid'}


def require_grid(composition: Composition) -> None:
    report = timing_report(composition)
    if not report['on_grid']:
        layer = next(layer for layer in report['layers'] if layer['off_grid_note_ons'])
        example = layer['examples'][0]
        raise CompositionError(
            f"{layer['id']}: off-grid note-on at beat {example['beat']:g} "
            f"(tick {example['tick']}, offset {example['offset_ticks']} ticks from "
            f"1/{report['grid_division']}); {report['off_grid_note_ons']} off-grid notes. "
            "Correct source onsets; for explicitly intended swing/humanization declare "
            "timing.mode='free'. Validation never silently quantizes notes.")

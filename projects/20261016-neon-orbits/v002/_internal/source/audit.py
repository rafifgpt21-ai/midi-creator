"""Composition-specific acceptance checks, against the exported performance."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import json
import hashlib
import subprocess
import sys
import mido

ROOT=Path.cwd().resolve()
REV=ROOT/'projects/20261016-neon-orbits/v002'
OLD=ROOT/'projects/20261016-neon-orbits/v001'
if not OLD.exists():OLD=ROOT/'projects/20261016-neon-orbits/_internal/previous-revisions/v001'
spec=json.loads((REV/'_internal/composition.json').read_text(encoding='utf8'))
layers={l['id']:l for l in spec['layers']}
checks={}
def check(name,condition):
    checks[name]=bool(condition)
    if not condition:raise AssertionError(name)

check('scale_all_E_harmonic_minor',all(n['pitch']%12 in {4,6,7,9,11,0,3} for l in spec['layers'] if l['kind']=='melodic' for n in l['notes']))
check('no_D_natural',all(n['pitch']%12!=2 for l in spec['layers'] if l['kind']=='melodic' for n in l['notes']))
check('all_six_drum_parts_root_60_channel_10',all(l['channel']==10 and {n['pitch'] for n in l['notes']}=={60} for l in spec['layers'] if l['kind']=='drums'))

arp=layers['phase-seven-pluck']['notes']
first=[n for n in arp if 64<=n['start']<92]
check('7over8_eight_full_cycles_in_seven_4over4_bars',len(first)==56 and all(abs(n['start']-(64+i*.5))<1e-8 for i,n in enumerate(first)))
check('7over8_accents_2plus2plus3',all(n['velocity']==[94,69,86,68,88,72,65][i%7] for i,n in enumerate(first)))
check('7over8_crosses_barline',first[7]['start']==67.5 and first[14]['start']==71 and first[21]['start']==74.5)
kick={n['start'] for n in layers['kick']['notes']}
check('four_floor_all_active_drop_and_groove_bars',all((bar-1)*4+b in kick for a,z in [(17,33),(49,81),(113,145),(145,161)] for bar in range(a,z) for b in range(4)))
pulse=layers['three-two-pulse']['notes']
for firstbar in [57,121]:
    begin=(firstbar-1)*4
    ns=[n for n in pulse if begin<=n['start']<begin+64]
    check(f'true_3to2_span_{firstbar}',len(ns)==96 and all(abs(n['start']-float(Fraction(begin)+Fraction(2*i,3)))<1e-8 for i,n in enumerate(ns)))
    check(f'three_pulses_vs_two_kicks_{firstbar}',len([n for n in ns if begin<=n['start']<begin+2])==3 and {begin,begin+1}.issubset(kick))

check('beatless_breakdown',all(not any(320<=n['start']<384 for n in l['notes']) for l in spec['layers'] if l['kind']=='drums'))
check('bass_absent_breakdown_and_build_gaps',not any(320<=n['start']<384 or 176<=n['start']<192 or 432<=n['start']<448 for n in layers['mono-bass']['notes']))
check('three_release_bars_no_new_notes',all(n['start']<644 for l in spec['layers'] for n in l['notes']))
check('final_Em_chord', {n['pitch']%12 for n in layers['juno-pad']['notes'] if n['start']==640}=={4,7,11})
check('lead_register_controlled',max(n['pitch'] for n in layers['analog-lead']['notes'])==84)
check('mono_bass_gates_do_not_overlap',all(a['start']+a['duration']<=b['start']+1e-8 for a,b in zip(layers['mono-bass']['notes'],layers['mono-bass']['notes'][1:])))

invent={}
for lid,l in layers.items():
    p=REV/'MIDI'/f'{lid}.mid'
    midi=mido.MidiFile(p)
    check(f'{lid}_SMF1_one_track',midi.type==1 and len(midi.tracks)==1)
    check(f'{lid}_same_length',sum(m.time for m in midi.tracks[0])==629760)
    check(f'{lid}_no_extra_metadata',not any(m.type in {'sysex','program_change','text','marker','key_signature'} or (m.type=='control_change' and m.control in {0,32}) for m in midi.tracks[0]))
    invent[lid]={'notes':len(l['notes']),'pitch_min':min(n['pitch'] for n in l['notes']),'pitch_max':max(n['pitch'] for n in l['notes']),'first_bar':1+l['notes'][0]['start']/4,'last_note_end_beat':max(n['start']+n['duration'] for n in l['notes']),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

old=json.loads((OLD/'_internal/composition.json').read_text(encoding='utf8'))
old={l['id']:l for l in old['layers']}
for lid,l in layers.items():
    if lid not in {'mono-bass','analog-lead'}:
        check(f'revision_preserves_{lid}',l==old[lid])
    else:
        check(f'revision_preserves_onsets_velocity_{lid}',[(n['start'],n['velocity']) for n in l['notes']]==[(n['start'],n['velocity']) for n in old[lid]['notes']])

result=subprocess.run(['uv','run','midi-creator','verify',str(REV)],capture_output=True,text=True,encoding='utf8')
verification=json.loads(result.stdout)
(REV/'_internal/final-verification.json').write_text(json.dumps(verification,indent=2)+'\n',encoding='utf8')
check('CLI_verify_exit0_and_ok',result.returncode==0 and verification['ok'])
check('strict_grid_no_offsets',verification['timing']['on_grid'] and verification['timing']['off_grid_note_ons']==0)
receipt=json.loads((REV/'_internal/serum-bank/receipt.json').read_text())
check('seven_native_presets_structurally_verified',receipt['ok'] and len(receipt['presets'])==7)
for p in receipt['presets']:
    path=REV/'Presets'/f"{p['id']}.SerumPreset"
    check(f"preset_copy_hash_{p['id']}",hashlib.sha256(path.read_bytes()).hexdigest()==p['sha256'])

audit={'ok':all(checks.values()),'checks':checks,'note_count':sum(len(l['notes']) for l in layers.values()),'layer_count':len(layers),'preset_count':7,'inventory':invent,
 'musical_evaluation':{'harmony':'All pitched notes restricted to E harmonic minor; distinct breakdown functional route, B7b9 leading-tone tension and final Em. Non-chord scale tones are passing/extension/suspension choices, not scale violations.',
 'roles':'Offbeat mono bass; upper pad voicings; rotating pluck and limited 3:2 pulse; articulated lead with phrase holes, brass answers, keys in breakdown.',
 'development':'Kick enters bar 9, arp bar 17; two different drop passes; bass withdrawn before drops; beatless 16-bar contrast; subtractive outro and tonic coda.',
 'register':'Corrected pre-publication lead octave zigzag; melodic lead now MIDI 71-84. Mono bass now has no note overlaps. Pad silence thins competing phrases.',
 'limitations':'Paper/MIDI evaluation only; audibility, timbral balance, stereo and FX tails require native plugin audition.'},
 'mc_ai_tell_audit':{'1_section_sizes':'4-bar release coda breaks 8-bar multiples for a musical reason.', '2_energy':'Designed fall at breakdown and outro; audio RMS not measured.', '3_roster':'Explicit staggered entries/exits and holes.', '4_harmony':'Breakdown changes route while retaining requested harmonic minor; no forced modulation.', '5_fills':'31,46,48,63,78,103,110,112,127,142,158; not every fourth bar.', '6_hook':'7/8 accent pattern plus original lead contour; memorability not auditioned.', '7_audio_dynamics':'Untested; velocity/CC1 and preset contrast authored.', '8_grid':'Intentional strict timing per AGENTS.md; not treated as an error.', '9_ending':'5:17.419 with three bars release.', '10_to_14_vocals':'Not applicable: instrumental.'},
 'evidence':{'MIDI_structure':'passed','native_preset_structure':'passed','native_plugin_load':'untested','Cubase_live_import':'untested','audio_render':'not_performed','actual_listening':'not_performed'}}
(REV/'_internal/musical-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf8')
print(json.dumps({'ok':audit['ok'],'checks':len(checks),'notes':audit['note_count'],'layers':13,'native_presets':7,'end_tick':629760,'grid':'strict 1/48','listened':False}))

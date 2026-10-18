"""Audit delivered MIDI, harmonic agreement and arrangement competition."""
from pathlib import Path
from collections import defaultdict
from itertools import combinations
import hashlib
import json
import subprocess
import mido

HERE=Path(__file__).resolve().parent
REV=Path.cwd().resolve()/'projects/20261016-neon-orbits/v003'
def read(p): return json.loads(p.read_text(encoding='utf8'))
new=read(REV/'_internal/composition.json')
old=read(HERE/'baseline-v002.json')
layers={l['id']:l for l in new['layers']}
prior={l['id']:l for l in old['layers']}
plan={h['bar']:h for h in read(HERE/'harmonic-plan.json')}
arr=read(HERE/'arrangement-plan.json')
checks={}
def check(name, ok):
    checks[name]=bool(ok)
    if not ok: raise AssertionError(name)

def competition(spec, use_release=False):
    events=defaultdict(list)
    focus={'analog-lead','phase-seven-pluck','three-two-pulse','poly-brass'}
    for l in spec['layers']:
        if l['id'] not in focus: continue
        release=0
        if use_release:
            release=read(HERE/'preset-specs'/f"{l['id']}.json")['envelopes'][0]['release']*124/60
        for n in l['notes']:
            events[n['start']].append((l['id'],1))
            events[round(n['start']+n['duration']+release,8)].append((l['id'],-1))
    active=defaultdict(int); prev=0; multi=triple=0; max_active=0
    for t,es in sorted(events.items()):
        count=sum(v>0 for v in active.values())
        if count>=2: multi+=t-prev
        if count>=3: triple+=t-prev
        max_active=max(max_active,count)
        for lid,delta in es: active[lid]+=delta
        prev=t
    return dict(two_or_more_foregrounds_beats=round(multi,6),three_or_more_beats=round(triple,6),max_simultaneous_foregrounds=max_active)

def semitone_time(spec):
    events=defaultdict(list)
    for l in spec['layers']:
        if l['kind']!='melodic':continue
        for i,n in enumerate(l['notes']):
            key=(l['id'],i)
            events[n['start']].append((key,n['pitch']))
            events[round(n['start']+n['duration'],8)].append((key,None))
    active={};prev=0;total=0
    for t,es in sorted(events.items()):
        if any(abs(a-b)%12 in (1,11) for a,b in combinations(active.values(),2)):total+=t-prev
        for k,p in es:
            if p is None:active.pop(k,None)
            else:active[k]=p
        prev=t
    return round(total,6)

check('global_tempo_meter_bars_resolution_sections_preserved',all(new[k]==old[k] for k in ('tempo_bpm','time_signature','bars','ticks_per_beat','sections')))
check('strict_no_swing_grid',new['timing']==dict(mode='strict',grid_division=48))
check('all_13_layers_present',set(layers)==set(prior) and len(layers)==13)
check('harmonic_minor_all_pitched_notes',all(n['pitch']%12 in {0,3,4,6,7,9,11} for l in layers.values() if l['kind']=='melodic' for n in l['notes']))
check('chord_tones_all_pitched_notes',all(n['pitch']%12 in {p%12 for p in plan[int(n['start']//4)+1]['pad']} for l in layers.values() if l['kind']=='melodic' for n in l['notes']))
for lid,l in layers.items():
    if l['kind']!='melodic':continue
    safe=True
    for n in l['notes']:
        first=int(n['start']//4)+1
        last=min(164,int((n['start']+n['duration']-1e-8)//4)+1)
        if any(n['pitch']%12 not in {p%12 for p in plan[b]['pad']} for b in range(first,last+1)):safe=False
    check(f'{lid}_no_gate_into_incompatible_chord',safe)

for lid in ('kick','snare-clap','crash'):check(f'{lid}_exactly_preserved',layers[lid]==prior[lid])
check('bass_only_chord_roots',all(n['pitch']==plan[int(n['start']//4)+1]['root'] and n['start']%1==.5 for n in layers['mono-bass']['notes']))
check('bass_nominal_release_ends_before_next_kick',all(n['start']%1+n['duration']+.065*124/60<1 for n in layers['mono-bass']['notes']))
check('pad_voicings_have_no_clusters',all(min(b-a for a,b in zip(h['pad'],h['pad'][1:]))>=3 for h in plan.values()))
main=[plan[b]['pad'] for b in (1,3,5,7,9)]
check('main_pad_voice_leading_max_three_semitones',max(abs(b-a) for oldv,newv in zip(main,main[1:]) for a,b in zip(oldv,newv))<=3)
release=read(HERE/'preset-specs/juno-pad.json')['envelopes'][0]['release']*124/60
check('pad_nominal_amp_release_clears_chord_change',all(n['duration']+release<8 for n in layers['juno-pad']['notes']))

focus=competition(new)
release_focus=competition(new,True)
check('one_foreground_gate_at_a_time',focus['max_simultaneous_foregrounds']==1)
check('one_foreground_with_nominal_amp_releases',release_focus['max_simultaneous_foregrounds']==1)
check('no_vertical_semitones_in_pitched_note_gates',semitone_time(new)==0)
check('cross_rhythm_background_substantially_reduced',len(layers['phase-seven-pluck']['notes'])+len(layers['three-two-pulse']['notes'])<.5*(len(prior['phase-seven-pluck']['notes'])+len(prior['three-two-pulse']['notes'])))
check('lead_at_least_half_as_many_notes',len(layers['analog-lead']['notes'])<.5*len(prior['analog-lead']['notes']))

kick={n['start'] for n in layers['kick']['notes']}
check('four_floor_all_grooves_and_drops',all((b-1)*4+i in kick for a,z in [(17,33),(49,81),(113,145),(145,161)] for b in range(a,z) for i in range(4)))
arp=layers['phase-seven-pluck']['notes']
for first,after in arr['arp_spans']:
    begin=(first-1)*4;end=(after-1)*4
    ns=[n for n in arp if begin<=n['start']<end]
    expected=[(begin+i*.5,[82,57,68,0,74,56,0][i%7]) for i in range((after-first)*8) if i%7 in (0,1,2,4,5)]
    check(f'7over8_continuous_accent_and_rest_phase_{first}',[(n['start'],n['velocity']) for n in ns]==expected)
    if after-first==7:check(f'7over8_eight_complete_cycles_{first}',len(ns)==40 and len(range((after-first)*8))==8*7)
pulse=layers['three-two-pulse']['notes']
for first,after in arr['pulse_spans']:
    begin=(first-1)*4
    ns=[n for n in pulse if begin<=n['start']<(after-1)*4]
    ticks=[round(n['start']*960) for n in ns]
    check(f'true_3to2_exact_640_ticks_{first}',len(ticks)==24 and all(b-a==640 for a,b in zip(ticks,ticks[1:])))
    check(f'3to2_vs_two_quarter_kicks_{first}',sum(begin<=n['start']<begin+2 for n in ns)==3 and {begin,begin+1}.issubset(kick))
    check(f'pulse_pitch_stable_within_chord_{first}',len({n['pitch'] for n in ns[:12]})==len({n['pitch'] for n in ns[12:]})==1)
check('breakdown_has_only_keys_as_foreground',all(not any(320<=n['start']<384 for n in layers[lid]['notes']) for lid in ('analog-lead','phase-seven-pluck','three-two-pulse','poly-brass')))
check('beatless_breakdown',all(not any(320<=n['start']<384 for n in l['notes']) for l in layers.values() if l['kind']=='drums'))
check('three_release_bars',all(n['start']<644 for l in layers.values() for n in l['notes']))
check('drum_roots_and_channels',all(l['channel']==10 and {n['pitch'] for n in l['notes']}=={60} for l in layers.values() if l['kind']=='drums'))

inventory={}
for lid,l in layers.items():
    p=REV/'MIDI'/f'{lid}.mid'
    midi=mido.MidiFile(p)
    check(f'{lid}_SMF1_single_track_shared_length',midi.type==1 and len(midi.tracks)==1 and midi.ticks_per_beat==960 and sum(m.time for m in midi.tracks[0])==629760)
    check(f'{lid}_no_forbidden_metadata',not any(m.type in {'sysex','program_change','text','marker','key_signature'} or (m.type=='control_change' and m.control in (0,32)) for m in midi.tracks[0]))
    inventory[lid]=dict(notes=len(l['notes']),pitch_min=min(n['pitch'] for n in l['notes']),pitch_max=max(n['pitch'] for n in l['notes']),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
result=subprocess.run(['uv','run','midi-creator','verify',str(REV)],capture_output=True,text=True,encoding='utf8')
verification=json.loads(result.stdout)
(REV/'_internal/final-verification.json').write_text(json.dumps(verification,indent=2)+'\n',encoding='utf8')
check('CLI_verify_pass',result.returncode==0 and verification['ok'] and verification['timing']['on_grid'])
receipt=read(REV/'_internal/serum-bank/receipt.json')
check('seven_native_builds_readback_wire_scan',receipt['ok'] and len(receipt['presets'])==7 and all(all(p['structural_readback'].values()) and not p['wire_type_issues'] for p in receipt['presets']))
for p in receipt['presets']:
    check(f"{p['id']}_native_delivered_hash",hashlib.sha256((REV/'Presets'/f"{p['id']}.SerumPreset").read_bytes()).hexdigest()==p['sha256'])
for path in (HERE/'preset-specs').glob('*.json'):
    target=read(path);base=read(HERE/'baseline-preset-specs'/path.name)
    check(f'{path.stem}_retro_oscillators_filters_routes_preserved',all(target[k]==base[k] for k in ('oscillators','filters','mod_routes','lfos','global','arp')))
check('no_rhythmic_voice_delays',all(not any(f['type']=='FXDelay' for f in read(HERE/'preset-specs'/f'{lid}.json')['fx_chain']) for lid in ('phase-seven-pluck','analog-lead','glass-keys')))

audit=dict(ok=all(checks.values()),checks=checks,inventory=inventory,
    comparison=dict(v002=dict(foreground_gate_competition=competition(old),vertical_semitone_gate_beats=semitone_time(old),melodic_notes=sum(len(l['notes']) for l in old['layers'] if l['kind']=='melodic')),
                    v003=dict(foreground_gate_competition=focus,foreground_with_nominal_releases=release_focus,vertical_semitone_gate_beats=semitone_time(new),melodic_notes=sum(len(l['notes']) for l in new['layers'] if l['kind']=='melodic'))),
    interpretation='Symbolic metrics diagnose written density and clashes only. Triads and one foreground are deliberate choices for this repair, not universal definitions of good music. Amp-release budgets exclude reverb tails and are not rendered audio measurements.',
    status=dict(MIDI_structure='passed',native_structure='passed',plugin_loading='untested',Cubase_import='untested',audio_render='not_performed',actual_listening='not_performed'))
(REV/'_internal/musical-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(ok=audit['ok'],checks=len(checks),comparison=audit['comparison']),indent=2))

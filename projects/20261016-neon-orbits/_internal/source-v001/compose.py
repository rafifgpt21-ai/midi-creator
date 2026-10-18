"""Neon Orbits: deterministic composition and native-preset design sources.

Run with `uv run python <this-file>` from the MIDI Creator workspace.
The native bank is built separately by build_presets.py using serum-mcp's env.
"""
from pathlib import Path
from fractions import Fraction
import json
import random

HERE = Path(__file__).resolve().parent
SEED = 20261016
rng = random.Random(SEED)
BPM, BARS, PPQN = 124, 164, 960
TOTAL = BARS * 4
SCALE = {4, 6, 7, 9, 11, 0, 3}  # E F# G A B C D#
REQUEST = "buatkan musik retro synthwave edm, dengan beat 4 on the floor beat dan menggunakan polyrithm dan polymeter ala deadmau5, dengan mode minor harmonic, gunakan semua skill yang terkait dengan ini, terutama /skill:mc dan skill di dalam repo"

def save(name, value):
    p = HERE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Chord spelling and performance voicings are kept together.
CHORDS = {
    "Emadd9": (28, [52, 59, 66, 67], [64, 71, 78, 79, 83, 78, 76]),
    "Cmaj7": (36, [52, 59, 60, 67], [64, 67, 71, 72, 79, 71, 76]),
    "Amadd9": (33, [52, 59, 60, 69], [69, 76, 71, 72, 83, 76, 81]),
    "B7b9": (35, [51, 57, 60, 66], [66, 71, 75, 78, 81, 75, 83]),
    "F#m7b5": (30, [52, 57, 60, 66], [66, 69, 72, 76, 81, 72, 78]),
    "D#dim7": (39, [51, 57, 60, 66], [63, 66, 69, 72, 78, 69, 75]),
    "Em": (28, [52, 59, 64, 67], [64, 71, 76, 79, 83, 76, 88]),
}

FORM = [
    ("I", "Intro", 1, 16, 3, "repeat", "Filtered pulse, kick enters bar 9; pad opens the space."),
    ("G", "Instrumental", 17, 16, 5, "repeat", "7/8 ostinato enters against established 4/4 drums."),
    ("U1", "Instrumental", 33, 16, 6, "fragment", "Shorten the motif; remove bass for bars 45-48 and stop the final beat."),
    ("D1", "Drop", 49, 32, 8, "vary", "Lead states the full hook; 3:2 pulse enters bar 57; brass answers in gaps."),
    ("B", "Breakdown", 81, 16, 2, "augment", "No drums or bass; glass keys stretch the hook over a new harmonic route."),
    ("U2", "Instrumental", 97, 16, 6, "fragment+sequence", "Rebuild the seventh-note tension; kick returns at bar 105."),
    ("D2", "Drop", 113, 32, 10, "recap+vary", "Dynamic recap: motif returns, higher late answer, more open filter, thinner pad under lead."),
    ("O", "Outro", 145, 16, 4, "contract", "Subtract lead, brass, triplet pulse, then arp and hats; retain a mixable four-floor exit."),
    ("C", "Outro", 161, 4, 1, "augment", "Final Em at bar 161, then three bars with no new attacks for release."),
]

def section_at(bar):
    return next(s for s in FORM if s[2] <= bar < s[2] + s[3])

def harmony_at(bar):
    sid = section_at(bar)[0]
    if sid in {"I", "G", "D1", "D2", "O"}:
        cycle = ["Emadd9", "Emadd9", "Cmaj7", "Cmaj7", "Amadd9", "Amadd9", "B7b9", "B7b9"]
        return cycle[(bar - section_at(bar)[2]) % 8]
    if sid in {"U1", "U2"}:
        local = bar - section_at(bar)[2]
        cycle = ["Amadd9", "Amadd9", "Cmaj7", "Cmaj7", "F#m7b5", "F#m7b5", "B7b9", "B7b9"]
        return "B7b9" if local >= 12 else cycle[local % 8]
    if sid == "B":
        return ["Cmaj7", "Cmaj7", "Amadd9", "Amadd9", "F#m7b5", "F#m7b5", "B7b9", "B7b9", "Emadd9", "Emadd9", "Cmaj7", "Cmaj7", "Amadd9", "Amadd9", "D#dim7", "B7b9"][bar - 81]
    return "Em"

CONFIG = [
    ("mono-bass", "Mono Bass", "bass", 38, 101, 64),
    ("juno-pad", "Juno Pad", "harmony", 89, 77, 64),
    ("phase-seven-pluck", "Phase Seven Pluck", "polymeter", 81, 88, 56),
    ("three-two-pulse", "Three Two Pulse", "polyrhythm", 80, 76, 76),
    ("analog-lead", "Analog Lead", "melody", 81, 95, 64),
    ("poly-brass", "Poly Brass", "chord answers", 62, 81, 60),
    ("glass-keys", "Glass Keys", "breakdown motif", 98, 80, 72),
    ("kick", "Kick", "four on the floor", None, 111, 64),
    ("snare-clap", "Snare Clap", "backbeat", None, 96, 64),
    ("closed-hat", "Closed Hat", "straight subdivision", None, 75, 72),
    ("open-hat", "Open Hat", "offbeat lift", None, 79, 74),
    ("synth-tom", "Synth Tom", "transition fill", None, 86, 52),
    ("crash", "Crash", "section punctuation", None, 77, 54),
]
layers = {}
for lid, name, role, pg, vol, pan in CONFIG:
    layer = dict(id=lid, name=name, role=role, kind="drums" if pg is None else "melodic", channel=10 if pg is None else 1, volume=vol, pan=pan, notes=[])
    if pg is not None:
        layer["program"] = pg
    layers[lid] = layer

def note(lid, pitch, start, duration, velocity):
    start, duration = float(start), float(duration)
    if start < 0 or start + duration > TOTAL + 1e-8:
        raise ValueError((lid, start, duration))
    if layers[lid]["kind"] == "melodic":
        assert pitch % 12 in SCALE, (lid, pitch)
    layers[lid]["notes"].append(dict(pitch=pitch, start=round(start, 9), duration=round(duration, 9), velocity=max(1, min(127, int(velocity)))))

def drum(lid, bar, beat, velocity=90, duration=.10):
    note(lid, 60, (bar - 1) * 4 + beat, duration, velocity)

def chord(lid, pitches, start, duration, vel):
    for n, p in enumerate(pitches):
        note(lid, p, start, duration, vel + (2 if n == len(pitches)-1 else 0))

# The beat establishes a stable frame before the odd-length sequence arrives.
for bar in range(1, 161):
    sid = section_at(bar)[0]
    full = sid in {"G", "D1", "D2", "O"}
    kick_on = full or 9 <= bar <= 44 or 105 <= bar <= 112
    if kick_on:
        for b in range(4):
            if (bar in {48,112} and b == 3):
                continue
            drum("kick", bar, b, 113 if full else 105)
    snare_on = full or 25 <= bar <= 48 or 101 <= bar <= 112
    if snare_on:
        for b in (1,3):
            if bar in {48,112} and b == 3:
                continue
            drum("snare-clap",bar,b,102 if sid in {"D1","D2"} else 88)
    hats_on = 5 <= bar <= 80 or 97 <= bar <= 156
    if hats_on:
        for k in range(8):
            t=k/2
            if bar in {48,112} and t >= 3:
                continue
            # Open and closed articulations do not trigger together.
            opens = (sid in {"D1","D2"} or 25 <= bar <= 44 or 105 <= bar <=112 or 145<=bar<=152) and k%2==1
            if opens:
                drum("open-hat",bar,t,74+(k%4)*2,.25)
            else:
                drum("closed-hat",bar,t,66+(9 if k%2 else 0)+rng.randint(-3,3),.09)
        if sid=="D2" and (bar-113)%8 in {4,5,6}:
            for t in (.25,1.25,2.25,3.25):
                drum("closed-hat",bar,t,48+rng.randint(-3,3),.07)

FILL_BARS=[31,46,48,63,78,103,110,112,127,142,158]
for bar in FILL_BARS:
    end = 3 if bar in {48,112} else 4
    # The selected 1/48 grid supports 16ths; no unrequested 32nd rolls.
    ts=[2,2.5,2.75] if end==3 else [2.5,3,3.5,3.75]
    for i,t in enumerate(ts):
        drum("synth-tom",bar,t,69+i*6,.12)
for bar in [17,49,65,113,129,145]:
    drum("crash",bar,0,87 if bar in {49,113} else 74,.5)

# Mono bass answers the kick on eighth-note offbeats with an occasional 16th pickup.
for bar in range(9,161):
    sid=section_at(bar)[0]
    if sid=="B" or 45<=bar<=48 or 109<=bar<=112:
        continue
    root,_,_=CHORDS[harmony_at(bar)]
    start=(bar-1)*4
    if sid=="I" or (sid=="O" and bar>=153):
        for b in (0.5,2.5):
            note("mono-bass",root,start+b,.38,87)
    else:
        for i,b in enumerate((.5,1.5,2.5,3.5)):
            p=root+12 if i==3 and bar%4==0 else root
            gate=.34 if i<3 else (.20 if bar%8==7 and sid in {"D1","D2"} else .27)
            note("mono-bass",p,start+b,gate,98+(4 if i==0 else -i*2))
        if bar%8==7 and sid in {"D1","D2"}:
            note("mono-bass",root+12,start+3.75,.13,74)

# Two-bar harmonic rhythm, slower than the rhythmic foreground. Upper voicings
# reserve the bass register; final release has three empty bars.
for bar in range(1,161,2):
    sid=section_at(bar)[0]
    if sid in {"U1","U2"} and bar>=section_at(bar)[2]+12:
        continue
    if sid=="O" and bar>=153:
        continue
    # Deliberate holes under lead in each drop's busier second half.
    if sid in {"D1","D2"} and (bar-section_at(bar)[2])%8 in {4,6}:
        continue
    _,voicing,_=CHORDS[harmony_at(bar)]
    chord("juno-pad",voicing,(bar-1)*4,7.35,60 if sid in {"D1","D2"} else 68)
chord("juno-pad",CHORDS["Em"][1],640,3.8,64)

# Polymeter: seven eighth notes = 3.5 beats, grouped 2+2+3.
# The cycle never resets at a 4/4 barline; structural section resets are explicit.
ARP_SPANS=[(17,49),(49,81),(89,97),(97,113),(113,145),(145,153)]
arp_accents=[94,69,86,68,88,72,65]
for first,after in ARP_SPANS:
    begin=(first-1)*4;end=(after-1)*4
    for step in range(int((end-begin)*2)):
        t=begin+step*.5
        if (191<=t<192) or (447<=t<448):
            continue  # Last bar's final beat: stop before the drop.
        bar=int(t//4)+1
        _,_,pattern=CHORDS[harmony_at(bar)]
        # Narrow register under foreground lead, no random transposition.
        p=pattern[step%7]
        if p>83: p-=12
        vel=arp_accents[step%7]
        if 89<=bar<=96:vel-=27
        elif section_at(bar)[0] in {"D1","D2"} and (bar-section_at(bar)[2])%8<4:vel-=9
        note("phase-seven-pluck",p,t,.29,vel)

# Polyrhythm: exactly three equally spaced attacks per TWO quarter-note beats.
# Four-floor kick remains 0,1,2,3; triplet pulse is 0,2/3,4/3,...
for first,after in [(57,73),(121,137)]:
    begin=Fraction((first-1)*4);end=Fraction((after-1)*4)
    count=0;t=begin
    while t<end:
        bar=int(t//4)+1
        _,voicing,_=CHORDS[harmony_at(bar)]
        p=[voicing[-2]+12,voicing[-1]+12,voicing[1]+12][count%3]
        note("three-two-pulse",p,t,Fraction(2,5),82 if count%3==0 else 63)
        count+=1;t=begin+Fraction(2*count,3)

# Original eight-bar lead: E-B-F#-G and the C-D#-E harmonic-minor signature.
# Event positions deliberately leave the seventh/eighth bars room for answers.
HOOK=[
    [(0,76,.65),(.75,71,.40),(1.5,78,.40),(2.25,79,1.15)],
    [(.5,78,.65),(1.5,76,1.5)],
    [(.5,79,.65),(1.25,83,.4),(2,84,.65),(3,83,.6)],
    [(0,79,.75),(1.5,76,1.3)],
    [(.5,81,.65),(1.25,83,.4),(2,84,1.15)],
    [(.5,83,.55),(1.25,81,.55),(2.25,79,.8)],
    [(.5,78,.65),(1.5,75,.65),(2.5,72,.4)],
    [(0,75,1.3),(1.5,78,.6),(3.5,75,.3)],
]
for first,after,second in [(49,81,False),(113,145,True)]:
    for bar in range(first,after):
        local=bar-first
        pattern=HOOK[local%8]
        # Every alternate eight-bar pass makes space for the rhythmic hook.
        if local%16>=8 and local%8 in {1,3,5}:
            pattern=pattern[:1]
        if second and local>=24 and local%8 in {2,4}:
            pattern=([(.5,83,.65),(1.25,84,.4),(2,83,.65),(3,79,.6)] if local%8==2
                     else [(.5,84,.65),(1.25,83,.4),(2,81,1.15)])
        for i,(s,p,d) in enumerate(pattern):
            note("analog-lead",p,(bar-1)*4+s,d,96+(5 if second else 0)-i*3)
    # Changed final cadence in each pass; the final D# resolves to E explicitly.

# Filtered hook fragments in builds; the complete lead only arrives at drop 1.
for bar in [37,39,41,43,101,103,105,107]:
    t=(bar-1)*4
    for s,p in [(0,71),(.75,75),(1.5,78)]:
        note("analog-lead",p,t+s,.38,68+(bar%4)*3)

# Brass answers, rather than duplicating, the principal melody.
for first,after in [(49,81),(113,145)]:
    for bar in range(first,after):
        local=(bar-first)%8
        if local in {1,3,5}:
            _,v,_=CHORDS[harmony_at(bar)]
            chord("poly-brass",[p+12 for p in v[:3]],(bar-1)*4+3,.47,76)
        if local==7:
            _,v,_=CHORDS[harmony_at(bar)]
            chord("poly-brass",[p+12 for p in v[:3]],(bar-1)*4+2.5,.9,81)

# Glassy digital-synth motif in the beatless breakdown, not an acoustic piano.
for bar in range(81,97,2):
    _,v,_=CHORDS[harmony_at(bar)]
    picks=[v[0]+12,v[2]+12,v[3]+12,v[1]+12]
    for i,(at,d) in enumerate([(0,1.3),(1.5,1.4),(3.5,1.7),(6,1.2)]):
        note("glass-keys",picks[i],(bar-1)*4+at,d,72-i*4)
for bar in [4,8,12,16]:
    note("glass-keys",[76,71,75,76][bar//4-1],(bar-1)*4+2,1.1,56)
note("glass-keys",76,640,2.0,66)

# CC1 is explicitly routed to cutoff in each Serum preset. All notes stay on grid.
CURVES={
    "mono-bass":{1:12,9:25,17:40,33:45,44:75,45:10,49:80,65:92,80:35,81:10,97:20,105:65,109:10,113:90,129:100,145:58,153:30,160:10},
    "juno-pad":{1:10,9:25,17:40,33:48,44:60,49:45,65:60,81:20,89:40,97:35,108:62,113:50,129:70,145:35,153:15,161:10},
    "phase-seven-pluck":{1:0,17:15,32:40,33:42,44:85,48:95,49:75,64:65,65:90,80:25,81:0,89:10,97:20,108:88,112:100,113:82,128:68,129:100,144:55,145:40,152:8},
    "three-two-pulse":{1:20,57:45,64:70,72:40,121:55,128:90,136:55},
    "analog-lead":{1:10,37:20,44:50,49:68,65:82,80:40,81:0,101:25,108:58,113:80,129:95,144:45},
    "poly-brass":{1:25,49:45,65:62,80:30,113:55,129:74,144:30},
    "glass-keys":{1:20,16:35,81:25,89:52,96:30,161:15},
}
for lid, curve in CURVES.items():
    points=sorted(((bar-1)*4,val) for bar,val in curve.items())
    events={}
    for (a,va),(b,vb) in zip(points,points[1:]):
        for beat in range(a,b):
            events[beat]=round(va+(vb-va)*(beat-a)/(b-a))
    events[points[-1][0]]=points[-1][1]
    layers[lid]["control_changes"]=[dict(start=t,control=1,value=v) for t,v in sorted(events.items())]

for layer in layers.values():
    layer["notes"].sort(key=lambda n:(n["start"],n["pitch"]))

composition=dict(version=1,title="Neon Orbits",description="Retro synthwave / progressive EDM. E harmonic minor. True 3:2 polyrhythm and a continuous seven-eighth-note 7/8 ostinato over 4/4 drums.",prompt=REQUEST,
    assumptions=["Instrumental, original musical material; artist reference interpreted as evolving layered sequences and gradual filter development, not a copied song.","124 BPM, 4/4, 164 bars including release; E F# G A B C D# throughout.","Strict grid 1/48, 960 PPQN: straight 1/16 and 2/3-beat attacks share a 1/12-beat lattice; no swing or onset jitter.","Seven Serum 2 instruments and six separate drum parts. All drum triggers are pitch 60 / Cubase C3; kit and samples remain the user's choice.","No combined MIDI, audio, or Cubase project requested. Native Serum preset per melodic layer."],
    tempo_bpm=BPM,time_signature=[4,4],bars=BARS,ticks_per_beat=PPQN,timing=dict(mode="strict",grid_division=48),key_signature="Em",
    sections=[dict(name=f"{s[0]} - {s[1]}",start=(s[2]-1)*4) for s in FORM],layers=list(layers.values()))
save("composition.json",composition)
save("harmonic-plan.json",[{"bar":bar,"chord":harmony_at(bar)} for bar in range(1,165)])

# Skill handoff: JSON follows the ARR-SPEC v1 template fields; performance truth is
# composition.json. Harmonic minor has no dedicated ARR-SPEC mode enum.
harmonies={"I":("imadd9 bVImaj7 ivmadd9 V7b9","Emadd9 Cmaj7 Amadd9 B7b9"),"G":("imadd9 bVImaj7 ivmadd9 V7b9","Emadd9 Cmaj7 Amadd9 B7b9"),"U1":("ivmadd9 bVImaj7 iim7b5 V7b9","Amadd9 Cmaj7 F#m7b5 B7b9"),"D1":("imadd9 bVImaj7 ivmadd9 V7b9","Emadd9 Cmaj7 Amadd9 B7b9"),"B":("bVImaj7 ivmadd9 iim7b5 V7b9 imadd9 bVImaj7 ivmadd9 #viidim7 V7b9","Cmaj7 Amadd9 F#m7b5 B7b9 Emadd9 Cmaj7 Amadd9 D#dim7 B7b9"),"U2":("ivmadd9 bVImaj7 iim7b5 V7b9","Amadd9 Cmaj7 F#m7b5 B7b9"),"D2":("imadd9 bVImaj7 ivmadd9 V7b9","Emadd9 Cmaj7 Amadd9 B7b9"),"O":("imadd9 bVImaj7 ivmadd9 V7b9","Emadd9 Cmaj7 Amadd9 B7b9"),"C":("im","Em")}
skills=["mc-workflow","mc-form","mc-arrangement-arch","mc-development","mc-harmony","mc-melody","mc-rhythm-groove","mc-rhythm-section","mc-orchestration","mc-texture-layering","mc-sound-design","mc-mix-intent","mc-render-compile","mc-symbolic-score","mc-style-edm","mc-ai-tell-audit"]
save("arrangement-spec.json",{
    "spec_version":"1.0",
    "meta":{"title":"Neon Orbits","style_layer":"mc-style-edm","style_layers":[],"fusion_note":"Progressive house supplies groove and form; authored retro palette supplies timbre. No synthwave-specific MC skill exists, so the Serum analog guide owns its architecture.","key":"E minor","mode":"minor","meter":"4/4","tempo":124,"target_duration":"5:17","deliverable":["midi"],"upstream":{"brief":REQUEST,"lyrics":{},"picture":{}}},
    "intent":{"one_thing":"Membuat perjalanan malam yang terus bergerak melalui pergeseran siklus synth di atas kick yang stabil.","reference_pair":[{"track":"User's deadmau5 direction (conceptual reference, no recording supplied)","borrow":"Slow additive/subtractive development and interlocking synth sequences; no named melody or transcription."},{"track":"User's retro synthwave direction (palette reference, no recording supplied)","borrow":"Maintained subtractive monosynth bass, DCO-like chorus pad, rounded poly brass."}],"listener_situation":"Extended instrumental for headphones and a melodic dance-floor set; eight/sixteen-bar structural anchors.","emotional_arc":[{"section":s[0],"mood":s[6],"value":s[4]} for s in FORM]},
    "material":{"motif":"E turun kuart ke B lalu naik kuint ke F# dan semiton ke G; onset 0, .75, 1.5, 2.25 beat selama satu bar, diikuti jawaban turun pada bar berikutnya. Signature C-D#-E dipakai untuk tarikan harmonic minor.","motif_abc":"L:1/16\ne3 B2 z ^f2 z g5 z2 | z2 ^f3 z e6 z4 |","character":"Tertahan lalu terbuka","stated_in":["D1"],"development_mode":"加工处理"},
    "form":[{"id":s[0],"name":s[1],"bars":s[3],"start_bar":s[2],"harmony":harmonies[s[0]][0],"harmony_letters":harmonies[s[0]][1],"melody_register":"高" if s[0] in {"D1","D2"} else "中","development":s[5],"energy":s[4],"events":[],"note":s[6]+" Exact per-bar harmony is in harmonic-plan.json; basic chords hold two bars except the final breakdown cadence."} for s in FORM],
    "arrangement":{"roster":[{"id":lid,"instrument":name,"midi":dict(program=pg or 0,bank=0,channel=10 if pg is None else 1),"role":role,"band":"low" if lid in {"kick","mono-bass"} else "high" if "hat" in lid else "mid","entry":section_at(int(layers[lid]["notes"][0]["start"]//4)+1)[0],"exit":"C" if lid=="juno-pad" else "O","note":"Individual note entry/exit and re-entry are explicit in composition.json."} for lid,name,role,pg,_,_ in CONFIG],
        "depth_map":{"analog-lead":"前景","phase-seven-pluck":"中景","three-two-pulse":"中景","juno-pad":"背景","mono-bass":"中景","glass-keys":"前景","poly-brass":"中景"},
        "bass_kick_relation":{"mode":"互答式","detail":"Kick is on integer beats; bass attacks .5,1.5,2.5,3.5 with short gates. Kick remains the 4/4 anchor."},
        "spectrum_budget":[{"band":"sub / low","owner":"mono-bass","competitors":["kick"],"resolution":"Bass attacks offbeats and decays before the next kick."},{"band":"mid / upper mid","owner":"analog-lead","competitors":["juno-pad","poly-brass","phase-seven-pluck"],"resolution":"Brass answers phrase gaps, pad drops alternating two-bar cells; arp velocity recedes under lead."},{"band":"upper","owner":"glass-keys","competitors":["analog-lead"],"resolution":"Separate sections; keys carry the beatless breakdown."}],
        "energy_curve":{s[0]:s[4] for s in FORM},"subtraction_events":[{"at":{"section":"U1","bar_offset":12},"what":"Remove bass","why":"Restore weight when drop lands"},{"at":{"section":"B","bar_offset":0},"what":"Remove all drums and bass","why":"Expose a slower harmonic reading of the motif"},{"at":{"section":"D2","bar_offset":16},"what":"Remove pad cells under lead","why":"Make the brighter recap clear"}],
        "hooks":{"vocal_hook":{},"arrangement_hook":{"what":"Seven-eighth-note 2+2+3 accents rotate over four quarter-note kicks; lead adds an E-B-F#-G contour.","first_at":"G","recurs_at":["D1","U2","D2"]}},
        "groove":{"feel":"straight","push_pull":[{"part":"all","offset_ms":0,"note":"Repo strict timing takes precedence; variation uses velocity, gates, polymeter and polyrhythm."}],"fill_policy":{"bars":FILL_BARS,"rationale":"Uneven phrase punctuation; no automatic fill every fourth bar."}}},
    "vocal":{},"mix_intent":{"mood":"Hangat dan gelap, dengan kick jelas serta urutan synth yang terus bergeser.","sound_stage":[{"id":lid,"pan":round((pan-64)/63*100),"depth":"背景" if lid=="juno-pad" else "前景" if lid in {"analog-lead","glass-keys"} else "中景"} for lid,_,_,_,_,pan in CONFIG],"ducking_map":[{"section":"D1/D2","who_yields":"pad and arp","band":"mid","to":"analog-lead"}],"dynamics":{"target_DR_dB":0,"notes":["No measured DR target for unrendered MIDI. Breakdown should be audibly below drops; verify after sample choice."]},"width_map":{"I":"narrow","D1":"wide","B":"medium","D2":"wide","O":"narrow"},"loudness_target":"No mastered-audio target: MIDI and preset delivery."},
    "render":{"midi":{"instrument_map":{lid:{"name":"Serum 2" if pg is not None else "User sample / Cubase Sampler","program":pg or 0,"bank":0,"channel":10 if pg is None else 1} for lid,_,_,pg,_,_ in CONFIG}}},
    "checks":{"self_audit":["Intent complete; references are conceptual and not claimed as analyzed recordings.","Sections contiguous; 4-bar coda earns its length by tonic release.","Energy falls at breakdown and outro; roster changes and early exits are explicit.","Harmony uses the requested seven-note collection only; leading-tone harmony is intentional.","Fill bars are not a four-bar arithmetic sequence; width is designed per patch and section density, not a claimed DAW automation.","Every section develops the same motif; no uncontrolled new section material.","MIDI backend preserves notes/timing/controllers exactly; sound and mix need actual instruments."],"exemptions":["#9: Do not add scale-external harmony or modulation merely to satisfy an MC heuristic; user requests harmonic minor.","#11: All onsets remain quantized, because AGENTS.md requires strict/no-swing timing; velocity and gates supply expression.","#13: Suno prompt is irrelevant; selected backend is deterministic MIDI.","#15/#16 and vocal audit items: instrumental piece.","ARR-SPEC mode enum lacks harmonic minor; mode=minor with exact pitch collection in composition.json and request.md.","Reference-pair recordings and listening A/B were not supplied/performed; two user concepts used instead." ]},"messages":[]})
save("skill-usage.json",{"MC":skills,"Serum":["serum-sound-design","serum-synthesis","serum-modulation","serum-effects","serum-preset-build","serum-preset-qa"],"not_needed":{"mc-modulation":"No key changes requested; preserve E harmonic minor.","mc-progressions":"Progression authored from harmonic-minor function, no library lookup used.","mc-counterpoint":"No contrapuntal canon/fugue; roles are interlocking ostinatos and phrase answers.","mc-vocal-direction":"Instrumental.","serum-reference-match":"No reference audio or exact preset matching requested."}})

# Native Serum specs. A single simple graph per instrument; all rhythmic notes
# come from MIDI, never a second internal arp.
def osc(table="analog_basic",frame=1,volume=.55,**kw):
    return dict(enabled=True,wavetable=table,table_position=frame,volume=volume,unison=1.0,filter_routing="filter",**kw)
OFF={"enabled":False}
def env(a,d,s,r):return dict(attack=a,decay=d,sustain=s,release=r)
def route(source,destination,amount,**kw):return dict(source=source,destination=destination,amount=amount,**kw)
def fx(kind,wet,**params):return dict(type=kind,wet=wet,params=params,rack=0)
def curve(rate,points,**kw):
    return dict(rate=rate,mode="Free",beat_sync=False,mono=True,curve=[dict(x=x,y=y) for x,y in points],**kw)
TRI=[(0,.5),(.25,1),(.75,0),(1,.5)]
def patch(lid,description,oscillators,amp,cutoff,eg,fxs,mono=False,lfos=None,extra=None,res=12):
    wheel=24 if lid!="mono-bass" else 18
    spec={"name":lid,"description":description,"oscillators":oscillators+[dict(OFF) for _ in range(5-len(oscillators))],"filters":[dict(enabled=True,type="moog_lowpass_24" if mono else "lowpass_24",cutoff=cutoff,resonance=res,drive=8,stereo=50,level_out=.5),dict(enabled=False)],"envelopes":[amp,env(.003,.25,0,.12)],"macros":[dict(name="Tone",value=15),dict(name="Contour",value=20)],"lfos":lfos or [],"fx_chain":fxs,"global":{"master_volume":.48 if mono else .40,"mono":mono,"poly_count":1 if mono else 16,"portamento_time":0,"legato":False,"limit_same_note_polyphony":True,"swing":0},"arp":{"enabled":False},"mod_routes":[route("env1","filter0.cutoff",eg),route("mod_wheel","filter0.cutoff",wheel),route("macro0","filter0.cutoff",10),route("macro1","env1.decay",12),route("velocity","filter0.cutoff",4)]+(extra or [])}
    return spec
chorus=fx("FXChorus",28,kParamRate=.30,kParamDepth=3.8,kParamDelay=7.0,kParamFeedback=2,kParamFilt=4500)
space=lambda wet:fx("FXReverb",wet,kParamType="kVintage",kParamSize=36,kParamDelay=22,kParamWidth=90)
# Eighth-note delay at the fixed song tempo, explicitly free seconds. Synced dial
# units are uncertain; this avoids claiming an unverified note-division mapping.
delay=lambda wet:fx("FXDelay",wet,kParamTimeL=30/BPM,kParamTimeR=30/BPM,kParamBeatSync=0.0,kParamFeedback=23,kParamFreq=5500)
bank={
"mono-bass":patch("mono-bass","Maintained VCO-mono-inspired bass: Mini saw plus rounded low reinforcement, centered, no chorus or long FX.",[osc("analog_mini",0,.59),osc("analog_basic",2,.34,octave=-1)],env(.004,.24,.56,.065),.24,27,[],mono=True,res=17),
"juno-pad":patch("juno-pad","DCO-family approximation: single Juno PWM-table source, no detuned second VCO or pitch drift; slow spectral scan and chorus.",[osc("pwm",56,.55)],env(.55,1.1,.78,1.45),.37,12,[chorus,space(16)],lfos=[curve(.12,TRI)],extra=[route("lfo0","oscillator0.table_position",2.0,bipolar=True)]),
"phase-seven-pluck":patch("phase-seven-pluck","Seven-eighth-note ostinato voice: dry transient from rounded saw, short filter decay, limited tempo echo; external MIDI owns the 7/8 cycle.",[osc("analog_warm",0,.52)],env(.003,.36,0,.12),.29,30,[delay(12),space(8)],res=19),
"three-two-pulse":patch("three-two-pulse","Hollow square/triangle electronic pulse, three attacks over two beats in external MIDI; compact tail and narrow image.",[osc("analog_basic",3,.47),osc("default",2,.29)],env(.006,.30,.10,.10),.43,16,[space(9)],res=8),
"analog-lead":patch("analog-lead","Maintained dual-VCO-inspired lead: saw and pulse offset -2/+2 cents, articulated rather than legato; filtered stereo echo.",[osc("analog_mini",0,.43,fine=-2),osc("analog_basic",3,.29,fine=2)],env(.008,.4,.67,.17),.37,22,[delay(18),space(10)],mono=True,res=12),
"poly-brass":patch("poly-brass","Prophet-family approximation, two distinct saw tables offset -3/+3 cents, brass-like filter swell; phrase-gap answers, modest chorus.",[osc("analog_warm",0,.38,fine=-3),osc("default",0,.28,fine=3)],env(.028,.48,.48,.19),.35,23,[fx("FXChorus",15,kParamRate=.24,kParamDepth=2.2,kParamDelay=6,kParamFeedback=0,kParamFilt=5000),space(10)],res=10),
"glass-keys":patch("glass-keys","Digital glass-synth keys, not acoustic piano: OPL harmonic frame plus Dying Sine body, declining brightness and spacious but bounded tail.",[osc("digital_fm",1,.43),osc("dying_sine",48,.30)],env(.005,1.2,.08,.65),.56,12,[delay(12),space(22)],res=7),
}
# Brass brightness swells more slowly than the plucks.
bank["poly-brass"]["envelopes"][1]=env(.04,.42,.25,.18)
for lid,spec in bank.items():save(f"preset-specs/{lid}.json",spec)
save("bindings.json",{lid:f"Presets/{lid}.SerumPreset" for lid in bank})
save("sound-design.json",{
    "condition":"Maintained instrument-family approximations, not verified hardware emulations.",
    "registers":{lid:{"min":min(n["pitch"] for n in layers[lid]["notes"]),"max":max(n["pitch"] for n in layers[lid]["notes"])} for lid in bank},
    "architecture":"A/B -> Filter 1 -> Main serial FX -> output. Unused sources/Filter 2 disabled; no auxiliary buses or direct paths.",
    "five_analog_techniques":{"voice_calibration":"Not used: native control scales uncalibrated; stable source architecture chosen.","noise_FM":"Off: not needed for clean maintained character.","continuous_drift":"Off: DCO stays stable; VCO layers use documented static fine offsets. Phase randomness is not claimed as drift.","noise_AM":"Off: clean electronic palette.","drive_tape":"Small voice-filter drive only; no tape/wow/fast compression added by default."},
    "limitations":["Juno pad uses a factory sampled PWM wavetable scan, not proof of a DCO circuit or duty-cycle emulation.","Phase memory and voice-priority controls stay at Init; unsupported phase/voice calibration behavior is not claimed.","Cutoff and modulation depths are stored normalized values, not measured Hz/cents endpoints.","Delay time is fixed at 30/124 seconds (eighth note at 124 BPM), explicitly free mode; retime after tempo changes.","Filter changes are CC1 -> mod_wheel routes; macros default to Tone 15 and Contour 20, with usable ranges requiring listening validation.","Native plugin loading, audio renders, stereo/mono response and listening are separate untested steps."],
    "acceptance":["7 real native presets, independent readback and wire-type scan.","All wavetable dependencies resolve and hashes recorded; no custom resources.","Bass and lead mono; pad/brass polyphony budget 16; unused internal arp disabled.","MIDI note ranges and actual gates appropriate to source envelopes; voice-filter and FX intent documented."],
    "macro_ranges":{"Tone":{"default":15,"min":0,"max":100,"effect":"Adds 0..10 percentage points of filter modulation at the stored route scale."},"Contour":{"default":20,"min":0,"max":100,"effect":"Lengthens timbre-envelope decay via 0..12% route; physical seconds need plugin calibration."}}})

print(json.dumps({"bars":BARS,"seconds":TOTAL*60/BPM,"layers":len(layers),"notes":{k:len(v["notes"]) for k,v in layers.items()},"seed":SEED},indent=2))

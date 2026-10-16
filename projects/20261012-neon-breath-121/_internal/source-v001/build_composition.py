"""Deterministic 4-bar synth/disco study. No randomization or swing."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
Q = 60 / 121
LAYERS = []
PRESETS = {}
DESIGNS = {}

def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def layer(ident, name, role, volume=88, pan=64, drums=False):
    item = dict(id=ident, name=name, role=role, kind='drums' if drums else 'melodic',
                volume=volume, pan=pan, notes=[])
    if drums: item['channel'] = 10
    else: item['program'] = 80
    LAYERS.append(item)
    return item

def note(item, pitch, bar, step, length, velocity):
    # bar and step are 1-based; duration is measured in sixteenth-note steps.
    item['notes'].append(dict(pitch=pitch, start=(bar-1)*4+(step-1)*.25,
                             duration=round(length*.25, 6), velocity=velocity))

def chord(item, pitches, bar, step, length, velocity):
    for i,p in enumerate(pitches): note(item,p,bar,step,length,max(1,velocity-i*2))

sub=layer('layer01-sub-bass','01 Sub Bass','low-end foundation',99)
for b,p in enumerate([24,29,32,34],1): note(sub,p,b,1,16,100)
bass=layer('layer02-octave-bass','02 Moroder Octave Bass','rhythmic bass',95)
for b,(lo,hi) in enumerate([(36,48),(29,41),(32,44),(34,46)],1):
    for j in range(16): note(bass,[lo,hi][j%2],b,j+1,.72,[108,84,94,82][j%4])
stabs=layer('layer03-chord-stabs','03 Analog Chord Stabs','offbeat harmony',87,61)
voices=[[48,55,58,63],[48,53,56,63],[48,55,56,63],[55,58,62,65]]
for b,v in enumerate(voices,1):
    for s,vel in [(3,97),(7,87),(10,92),(15,104)]: chord(stabs,v,b,s,1.15,vel)
brass=layer('layer04-synth-brass','04 Synth Brass Accents','chorus lift',79)
for b,v in enumerate([[48,51,55],[48,53,56],[48,51,56],[50,53,58]],1):chord(brass,v,b,1,8,104)
arp=layer('layer05-bright-arp','05 Bright Up Down Arp','main arp',72,72)
index=[0,1,2,3,2,1,0,1,2,3,2,1,0,1,2,1]
for b,v in enumerate([[60,63,67,72],[65,68,72,77],[68,72,75,80],[70,74,77,82]],1):
    for j,i in enumerate(index):note(arp,v[i],b,j+1,.66,[84,65,73,67][j%4])
bell=layer('layer06-glass-bells','06 Glass Bell Counter Arp','high texture',60,52)
for b,v in enumerate([[91,87,84,87,91,96],[89,92,96,92,89,84],[92,96,87,84,87,92],[94,89,86,89,94,84]],1):
    for s,p in zip([2,4,8,10,12,16],v):note(bell,p,b,s,min(1.35,17-s),[62,53,58,57,64,49][[2,4,8,10,12,16].index(s)])
pad=layer('layer07-warm-pad','07 Warm Ambient Pad','background glue',67,64)
padvoices=[[51,55,60],[53,56,60],[51,56,60],[53,58,62]]
# Tie common tones across adjacent harmony changes instead of reattacking them.
for p in sorted(set(sum(padvoices,[]))):
    b=0
    while b<4:
        if p not in padvoices[b]: b+=1;continue
        end=b+1
        while end<4 and p in padvoices[end]:end+=1
        note(pad,p,b+1,1,16*(end-b),70)
        b=end
lead=layer('layer08-main-lead','08 Main Retro Hook','primary hook',94)
phrases=[[(1,60,2),(3,63,1),(4,67,3),(7,70,2),(9,67,3),(12,65,1),(13,63,2),(15,62,2)],
         [(1,60,2),(3,65,2),(5,68,3),(8,67,1),(9,65,2)],
         [(1,63,2),(3,67,2),(5,72,3),(8,70,1),(9,68,3),(12,67,1),(13,63,2),(15,67,2)],
         [(1,62,2),(3,65,2),(5,70,3),(8,68,1),(9,67,2)]]
for b,events in enumerate(phrases,1):
    for i,(s,p,d) in enumerate(events):
        overlap=.28 if i<len(events)-1 else 0
        note(lead,p,b,s,d+overlap,[105,93,100,95][i%4])
answer=layer('layer09-synth-whistle','09 Whistle Response','call and response',78,68)
for b,ps in [(2,[77,80,79]),(4,[74,77,72])]:
    for s,p,vel in zip([11,13,15],ps,[92,86,99]):note(answer,p,b,s,1.7,vel)
fx=layer('layer10-transition-fx','10 Riser and Down Impact','transition accents',66)
note(fx,60,1,1,64,1)
note(fx,48,1,1,4,127)

drum_info=[('drum-kick','Kick',107,64),('drum-snare','Snare',91,64),('drum-clap','Clap',75,64),
           ('drum-closed-hat','Closed Hat',77,58),('drum-open-hat','Open Hat',68,71),
           ('drum-shaker','Shaker',56,82),('drum-crash','Crash',57,60)]
drums={ident:layer(ident,name,'percussion',v,p,True) for ident,name,v,p in drum_info}
for b in range(1,5):
    for j in range(4):note(drums['drum-kick'],60,b,1+j*4,.7,[117,109,113,108][j])
    for s in [5,13]:
        note(drums['drum-snare'],60,b,s,.55,105 if s==5 else 111)
        note(drums['drum-clap'],60,b,s,.55,85 if s==5 else 92)
    for j in range(16):
        if j%4!=2:note(drums['drum-closed-hat'],60,b,j+1,.32,[72,49,0,56][j%4])
        note(drums['drum-shaker'],60,b,j+1,.28,[43,34,61,39][j%4])
    for s in [3,7,11,15]:note(drums['drum-open-hat'],60,b,s,.7,77 if s in [7,15] else 69)
note(drums['drum-crash'],60,1,1,1,94)

def osc(**kw):
    return dict(dict(enabled=True,octave=0,volume=.52,pan=0,unison=1,detune=0,
                wavetable='default',table_position=0,warp_amount=0,filter_routing='filter',filter_balance=0),**kw)
OFF=osc(enabled=False,volume=0,filter_routing='none')
def env(a,d,s,r):return dict(attack=a,hold=0,decay=d,sustain=s,release=r)
def filt(c=.5,typ='moog_lowpass_24',res=10,drive=0,**kw):
    return dict(dict(enabled=True,type=typ,cutoff=c,resonance=res,drive=drive,stereo=50,wet=100,level_out=.5,key_track=False,output_routing='parallel'),**kw)
def route(src,dest,amt,**kw):return dict(source=src,destination=dest,amount=amt,**kw)
def fxunit(typ,wet=100,**params):return dict(type=typ,wet=wet,params=params,rack=0)
def dist(wet=25,drive=18,mode='kTapeSat'):return fxunit('FXDistortion',wet,kParamMode=mode,kParamDrive=drive)
def chorus(wet=22,rate=.25,depth=5):return fxunit('FXChorus',wet,kParamRate=rate,kParamDepth=depth,kParamDelay=7,kParamFeedback=8,kParamFilt=3000)
def delay(wet=12,feedback=22):
    return fxunit('FXDelay',wet,kParamTimeL=Q/2,kParamTimeR=Q/4,kParamBeatSync=0.,kParamMode=1.,kParamFeedback=feedback,kParamFreq=4800)
def reverb(wet=15,size=45,typ='kHall'):return fxunit('FXReverb',wet,kParamType=typ,kParamSize=size,kParamDelay=22,kParamWidth=100)
def comp(ratio=2,makeup=1.5):return fxunit('FXComp',100,kParamThresh=.65,kParamRatio=ratio,kParamAttack=15,kParamRelease=90,kParamMakeup=makeup)
def util(hp=110,lp=15000,width=100):return fxunit('FXUtils',100,kParamHPF=hp,kParamLPF=lp,kParamWidth=width)
def lfo(rate=0,**kw):return dict(dict(rate=rate,mode='Free',beat_sync=True,mono=True),**kw)
def triangle():return [dict(x=0,y=0,tension=.5),dict(x=.5,y=1,tension=.5),dict(x=1,y=0,tension=.5)]
def pump():return [dict(x=0,y=1,tension=.5),dict(x=.075,y=1,tension=.5),dict(x=.45,y=.1,tension=.3),dict(x=.75,y=0,tension=.5),dict(x=1,y=0,tension=.5)]
def preset(ident,a,b,e1,e2,filter1,chain,routes,lfos=None,mono=False,master=.46,extra=None,description=''):
    spec=dict(name=ident,description=description,oscillators=[a,b,OFF.copy(),OFF.copy(),OFF.copy()],
              filters=[filter1,filt(enabled=False)],envelopes=[e1,e2,env(.001,.3,0,.12),env(.001,1,1,.015)],
              lfos=lfos or [lfo(curve=triangle()),lfo(curve=triangle())],
              macros=[dict(name='TONE',value=0),dict(name='SPACE',value=0)],fx_chain=chain,mod_routes=routes,
              global_=None,arp=dict(enabled=False))
    del spec['global_']
    spec['global']=dict(master_volume=master,mono=mono,poly_count=16 if not mono else 8,
                        portamento_time=0,legato=False,porta_always=False,swing=0)
    if extra:extra(spec)
    PRESETS[ident]=spec

def sub_extra(s):
    s['oscillators'][4]=osc(enabled=True,volume=.72,sub_shape='triangle',filter_routing='direct')
    s['global']['direct_volume']=1
    s['macros']=[dict(name='PUMP',value=100),dict(name='LEVEL',value=0)]
preset(sub['id'],OFF,OFF,env(.005,1,1,.045),env(.001,.12,0,.03),filt(.28,'lowpass_24',0,0,enabled=False),[],
       [route('lfo0','oscillator4.volume',-65,aux_source='macro0'),route('macro1','oscillator4.volume',-20)],
       [lfo(curve=pump()),lfo(curve=triangle())],True,.55,sub_extra,
       'Clean triangle Sub Direct. Mandatory host LP 80 Hz; quarter-note pump. C0 F0 Ab0 Bb0 (Cubase).')
preset(bass['id'],osc(wavetable='analog_mini',volume=.55),osc(wavetable='default',volume=.2,fine=3),
       env(.002,.13,.06,.025),env(.001,.072,0,.022),filt(.37,res=19,drive=16),
       [dist(38,25,'kSoftClip'),comp(2.5,1.7),util(95,6500,0)],
       [route('env1','filter0.cutoff',33),route('velocity','filter0.cutoff',7),route('velocity','global.voice_amp',12),
        route('macro0','filter0.cutoff',13),route('macro1','filter0.drive',12)],mono=True,master=.48,
       description='Tight saw octave sequencer; short filter decay; high-pass after saturation separates the sub.')
PRESETS[bass['id']]['macros'][1]['name']='GRIT'
preset(stabs['id'],osc(volume=.36,unison=3,detune=.075),osc(wavetable='analog_mini',volume=.32,unison=2,detune=.045,fine=-4),
       env(.003,.24,0,.095),env(.002,.16,0,.055),filt(.48,res=16,drive=10),
       [dist(16,12),comp(2,1.45),chorus(32,.22,6),reverb(10,35,'kVintage'),util(160,10500)],
       [route('env1','filter0.cutoff',28),route('velocity','filter0.cutoff',8),route('lfo0','oscillator1.fine',1.2,bipolar=True),
        route('macro0','filter0.cutoff',12),route('macro1','fx3.wet',15)],
       [lfo(.27,beat_sync=False,curve=triangle()),lfo(curve=triangle())],master=.40,
       description='Juno/Jupiter-like saw stabs, modest detune and vintage chorus; low-mid space for bass.')
preset(brass['id'],osc(volume=.38,unison=5,detune=.09),osc(volume=.23,unison=3,detune=.055,table_position=128,fine=-3),
       env(.024,.7,.66,.18),env(.035,.48,.42,.14),filt(.46,res=13,drive=17),
       [dist(22,17),comp(2.2,1.6),chorus(15,.18,4),reverb(31,75),util(150,12000)],
       [route('env1','filter0.cutoff',38),route('velocity','filter0.cutoff',8),route('lfo0','oscillator0.fine',1.5,bipolar=True),
        route('macro0','filter0.cutoff',10),route('macro1','fx3.wet',12)],
       [lfo(4.7,beat_sync=False,delay=.12,rise=.2,curve=triangle()),lfo(curve=triangle())],master=.38,
       description='Slow-35-ms brightness swell then broad saw/square brass sustain; large hall accents.')
preset(arp['id'],osc(volume=.4,unison=3,detune=.055),osc(wavetable='pwm',table_position=120,volume=.17,unison=2,detune=.035),
       env(.001,.18,0,.035),env(.001,.085,0,.035),filt(.52,res=9,drive=7),
       [comp(2,1.45),chorus(12,.3,3),delay(13,23),reverb(9,35),util(240,13000)],
       [route('env1','filter0.cutoff',30),route('lfo0','filter0.cutoff',5,bipolar=True),route('lfo1','oscillator1.table_position',4,bipolar=True),
        route('velocity','global.voice_amp',14),route('macro0','filter0.cutoff',9),route('macro1','fx2.wet',14)],
       [lfo(curve=triangle()),lfo(.33,beat_sync=False,curve=triangle())],master=.43,
       description='External-MIDI 16th pluck arp; chorus and asymmetric 1/8 + 1/16 stereo echoes.')
preset(bell['id'],osc(wavetable='analog_basic',volume=.42,warp_mode='fm',warp_amount=.13),
       osc(wavetable='analog_basic',volume=0,semitone=7),env(.004,1.25,0,.38),env(.001,.28,0,.24),
       filt(.73,'lowpass_12',6,0,key_track=True),
       [delay(27,38),reverb(32,69,'kSpace'),util(400,12000)],
       [route('env1','oscillator0.warp_amount',12),route('velocity','oscillator0.warp_amount',7),
        route('lfo0','oscillator0.pan',9,bipolar=True),route('lfo1','oscillator0.fine',.6,bipolar=True),
        route('macro0','oscillator0.warp_amount',8),route('macro1','fx1.wet',15)],
       [lfo(.18,beat_sync=False,curve=triangle()),lfo(.37,beat_sync=False,curve=triangle())],master=.36,
       description='Sine carrier A FM from enabled silent sine B +7 semitones; high glass bell and Space reverb, no pitch-shift shimmer.')
preset(pad['id'],osc(wavetable='analog_mini',volume=.24,unison=5,detune=.065),
       osc(wavetable='pwm',table_position=150,volume=.2,unison=3,detune=.045,fine=-3),
       env(.62,1.4,.85,.65),env(.85,1.8,.62,.6),filt(.54,'moog_lowpass_12',7,5),
       [chorus(37,.19,7),reverb(22,55,'kVintage'),util(230,7500,115)],
       [route('env1','filter0.cutoff',12),route('lfo0','filter0.cutoff',4,bipolar=True),
        route('lfo1','oscillator1.table_position',5,bipolar=True),route('lfo1','oscillator0.pan',5,bipolar=True),
        route('macro0','filter0.cutoff',9),route('macro1','fx1.wet',14)],
       [lfo(.125,beat_sync=False,curve=triangle()),lfo(.08,beat_sync=False,curve=triangle())],master=.38,
       description='Soft analog pad, common-tone ties across Cm/Fm/Ab/Bb; gentle independent brightness/PWM movement.')
def glide(s):s['global'].update(portamento_time=.05,legato=True,porta_always=False)
preset(lead['id'],osc(volume=.43,unison=5,detune=.085),osc(volume=.22,unison=2,detune=.035,table_position=128),
       env(.008,.38,.76,.12),env(.004,.25,.3,.09),filt(.67,'moog_lowpass_12',12,12,key_track=True),
       [dist(32,24),comp(2.4,1.7),chorus(12,.2,3),delay(16,23),reverb(18,60),util(190,12500)],
       [route('env1','filter0.cutoff',18),route('velocity','filter0.cutoff',5),
        route('lfo0','oscillator0.fine',3,bipolar=True,aux_source='mod_wheel'),
        route('lfo0','oscillator1.fine',3,bipolar=True,aux_source='mod_wheel'),
        route('lfo1','oscillator1.warp_amount',2,bipolar=True),route('macro0','filter0.cutoff',10),route('macro1','fx4.wet',14)],
       [lfo(5.2,beat_sync=False,delay=.15,rise=.18,curve=triangle()),lfo(.22,beat_sync=False,curve=triangle())],True,.46,glide,
       'Original four-bar C-minor hook, 50-ms mono legato glide; short overlapping MIDI notes. Wheel adds vibrato.')
preset(answer['id'],osc(wavetable='analog_basic',volume=.49),osc(volume=.11,table_position=128),
       env(.015,.34,.67,.09),env(.018,.24,.28,.09),filt(.66,'lowpass_12',12,0,key_track=True),
       [chorus(12,.3,3),delay(14,20),reverb(19,52),util(380,9500)],
       [route('env1','filter0.cutoff',12),route('lfo0','oscillator0.fine',3,bipolar=True),
        route('lfo0','oscillator1.fine',3,bipolar=True),route('lfo1','oscillator0.pan',3,bipolar=True),
        route('macro0','filter0.cutoff',8),route('macro1','fx2.wet',13)],
       [lfo(5.6,beat_sync=False,delay=.11,rise=.14,curve=triangle()),lfo(.24,beat_sync=False,curve=triangle())],True,.46,
       description='Sine plus soft square disco whistle; delayed vibrato. Answers only at the end of bars 2 and 4.')
def fx_extra(s):
    s['oscillators'][3]=osc(volume=0,noise_type='White',filter_routing='filter')
    s['envelopes'][2]=env(.001,.38,0,.22)
    s['macros']=[dict(name='RISE BRIGHT',value=0),dict(name='SPACE',value=0)]
preset(fx['id'],osc(wavetable='analog_basic',volume=0,octave=-1,filter_routing='master'),OFF,
       env(.001,1,1,.22),env(16*Q,.01,1,.2),filt(.24,'lowpass_24',30,3),
       [dist(18,12),delay(28,37),reverb(38,78,'kSpace'),util(45,15000)],
       [route('env1','oscillator3.volume',70,aux_source='velocity',aux_inverted=True),
        route('env1','filter0.cutoff',66,aux_source='velocity',aux_inverted=True),
        route('env2','oscillator0.volume',65,aux_source='velocity'),
        route('env2','oscillator0.pitch',50,aux_source='velocity'),
        route('lfo0','oscillator3.pan',8,bipolar=True,aux_source='velocity',aux_inverted=True),
        route('lfo1','oscillator3.noise_color',5,bipolar=True,aux_source='velocity',aux_inverted=True),
        route('macro0','filter0.cutoff',5),route('macro1','fx2.wet',10)],
       [lfo(.25,beat_sync=False,curve=triangle()),lfo(3,beat_sync=False,curve=triangle())],False,.42,fx_extra,
       'Velocity-1 four-bar noise rise; velocity-127 sine impact with falling pitch/level. Two simultaneous voices, no hard key split.')

DESIGNS={
 sub['id']:dict(role='sub',register='Cubase C0/F0/Ab0/Bb0 = MIDI 24/29/32/34',acceptance=['Fundamentals 32.70/43.65/51.91/58.27 Hz','Mono centered Direct Sub triangle','Quarter-note pump with macro depth','Host LP80 mandatory because Direct bypasses Serum filters']),
 bass['id']:dict(role='bass',register='MIDI 29-48',acceptance=['64 straight 16th onsets, alternating octaves','72% step gates','No stereo processing; post-distortion highpass 95 Hz']),
 stabs['id']:dict(role='chords',register='MIDI 48-65',acceptance=['Four syncopated chords per bar','Cm7/Fm7/Abmaj7/Bb upper voicing','Polyphony supports chords and releases']),
 brass['id']:dict(role='brass',register='MIDI 48-58',acceptance=['Downbeat half-bar accents','35-ms filter opening swell','Saw/square body and hall space']),
 arp['id']:dict(role='arp',register='MIDI 60-82',acceptance=['64 external MIDI 16ths, internal arp disabled','Up/down triads','Stereo eighth/sixteenth echoes']),
 bell['id']:dict(role='bell',register='Cubase C5-C6 = MIDI 84-96',acceptance=['24 spaced eighth-grid events','A sine FM from silent enabled B','Space reverb; long ring tail']),
 pad['id']:dict(role='pad',register='MIDI 51-62',acceptance=['Harmony changes every bar','Common tones tied across bars','Slow envelopes and restrained low mids']),
 lead['id']:dict(role='lead',register='MIDI 60-72',acceptance=['Original C-minor melody','50-ms portamento with 35-ms overlaps','Silence for responses after beat 3 of bars 2/4']),
 answer['id']:dict(role='counter lead',register='MIDI 72-80',acceptance=['Only bars 2 and 4, beats 3-and/4/4-and','Delayed vibrato','No overlap with main lead MIDI']),
 fx['id']:dict(role='fx',register='MIDI 48 impact; MIDI60 riser',acceptance=['Two voices, one preset/instrument','Riser velocity1, impact127','7.933884-second Env2 rise','No claim of hard split or auditioned pitch sweep'])
}
assumptions=[
 'Four-bar complete loop/study explicitly requested, not full-length song; 121 BPM, Cm, 4/4, straight 1/16, 480 PPQN.',
 'All human note labels in producer README use Cubase C3=MIDI60; raw numeric MIDI pitches are authoritative.',
 'User approved sub C0/F0/Ab0/Bb0, numerical 24/29/32/34, to keep 30-80 Hz register.',
 'Cm7/Fm7/Abmaj7 harmonic colors; bar4 stab Bb/G upper voicing (G Bb D F) above Bb sub behaves as Bb6, not a changed bass progression.',
 'Pad uses whole-note chords each bar with common-tone ties; holding a single chord for all four bars would conflict with the requested progression.',
 'Layer10 is a polyphonic dual gesture preset distinguished by velocity1/127; small carrier leakage at riser velocity1 is possible, no hard switch.',
 'Direct triangle Sub bypasses internal lowpass and FX; mandatory DAW lowpass80 Hz and real kick sidechain described in README.',
 'Native quarter-note amplitude LFO is pumping, not detection of kick audio. Real sidechain is a host insert; native PUMP macro can be set to0.',
 'Stereo delay native times are 1/8 L and 1/16 R at121 BPM. Ping-pong mode and pitched shimmer require UI verification/manual steps.',
 'Drums per file trigger MIDI60/channel10 for separate Cubase Sampler Tracks. User selects concrete samples; none copied.',
 'No randomization, no combined MIDI, no rendered audio requested. Native preset loading and listening remain untested.'
]
composition=dict(version=1,title='Neon Breath — Nu-Disco Synthwave Study',description='10-synth four-bar original loop inspired by retro disco production; separate drum parts.',
                 tempo_bpm=121,time_signature=[4,4],bars=4,ticks_per_beat=480,timing=dict(mode='strict',grid_division=16),key_signature='Cm',
                 sections=[dict(name='Cm',start=0),dict(name='Fm',start=4),dict(name='Ab',start=8),dict(name='Bb',start=12)],
                 assumptions=assumptions,layers=LAYERS)
save('composition.json',composition)
save('preset-specs.json',PRESETS)
save('sound-design.json',DESIGNS)
save('bindings.json',{i:dict(plugin='Serum 2',preset=f'Presets/{i}.SerumPreset') for i in PRESETS})
print(f'Wrote {len(LAYERS)} layers, {sum(len(l["notes"]) for l in LAYERS)} MIDI notes, {len(PRESETS)} native preset specifications.')

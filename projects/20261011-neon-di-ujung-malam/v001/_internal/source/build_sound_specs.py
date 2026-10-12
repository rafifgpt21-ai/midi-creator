"""Seven distinct Serum 2 sounds; factory wavetables only, no external assets."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
def osc(table,volume,pos=0,**kw):
    return dict(enabled=True,wavetable=table,volume=volume,table_position=float(pos),**kw)
def env(a,d,s,r): return dict(attack=a,decay=d,sustain=s,release=r)
def filt(c,type='moog_lowpass_12',res=8,drive=0):
    return dict(enabled=True,type=type,cutoff=c,resonance=float(res),drive=float(drive),stereo=50.0)
def lfo(hz,**kw):
    values=dict(rate=hz,mode='Free',beat_sync=False,mono=True)
    values.update(kw)
    return values
def route(src,dst,amt,bipolar=False):
    return dict(source=src,destination=dst,amount=float(amt),bipolar=bipolar)
def fx(type,wet,**params): return dict(type=type,wet=float(wet),params=params)
def chorus(wet,depth=3):
    return fx('FXChorus',wet,kParamRate=.22,kParamDepth=float(depth),kParamDelay=5.0,kParamFeedback=2.0)
def hall(wet,size):
    return fx('FXReverb',wet,kParamType='kHall',kParamSize=float(size),kParamDelay=22.0,kParamWidth=95.0)
def delay(wet,feedback):
    # 1/8 at the composition's 118 BPM. Explicit free-time switch is essential.
    return fx('FXDelay',wet,kParamBeatSync=False,kParamTimeL=60/118/2,
              kParamTimeR=60/118/2,kParamFeedback=float(feedback),kParamFreq=4200.0)
def patch(id,description,oscillators,filters,envelopes,lfos,macros,effects,routes,volume,mono=False,poly=16,glide=0):
    oscillators += [dict(enabled=False)]*(5-len(oscillators))
    filters += [dict(enabled=False)]*(2-len(filters))
    return dict(name=id,description=description,oscillators=oscillators,filters=filters,
                envelopes=envelopes,lfos=lfos,macros=[dict(name=m,value=0.0) for m in macros],
                fx_chain=effects,mod_routes=routes,
                **{'global':dict(master_volume=volume,mono=mono,poly_count=float(poly),portamento_time=glide)})

SPECS=[]
SPECS.append(patch('pulse-bass','Tight mono analog pulse bass with a clean triangle foundation, short filter snap and restrained tape warmth.',
    [osc('analog_mini',.60,65),osc('warm_sub',.29,24,octave=0.0)],
    [filt(.25,'moog_lowpass_24',10,11)],
    [env(.004,.24,.78,.045),env(.001,.19,0,.035)],[],
    ['OPEN','SNAP','WARMTH','SUB'],
    [fx('FXDistortion',16,kParamMode='kTapeSat',kParamDrive=14.0),
     fx('FXEQ',100,kParamFreq1=180.0,kParamGain1=-1.5,kParamFreq2=4200.0,kParamGain2=-3.0)],
    [route('env1','filter0.cutoff',22),route('velocity','filter0.cutoff',7),
     route('macro0','filter0.cutoff',22),route('macro1','env1.decay',10),
     route('macro2','fx0.wet',28),route('macro3','oscillator1.volume',20)],.46,True,1))

SPECS.append(patch('midnight-pad','Soft Juno-inspired harmony with a contrasting warm oscillator, slow drift and a spacious dark hall.',
    [osc('pwm',.33,75,unison=3.0,detune=.045,fine=-2.0),
     osc('analog_warm',.28,100,unison=3.0,detune=.035,fine=3.0),
     osc('harmonic_smooth',.08,28,octave=1.0)],
    [filt(.33,'moog_lowpass_12',6)],
    [env(.65,1.8,.79,1.7),env(1.1,2.7,.35,1.8)],
    [lfo(.085),lfo(.14),lfo(.21)],['OPEN','DRIFT','SPACE','GLOW'],
    [chorus(22,4),hall(21,48)],
    [route('env1','filter0.cutoff',9),route('lfo0','oscillator0.table_position',5,True),
     route('lfo1','oscillator1.table_position',4,True),route('lfo2','oscillator2.pan',9,True),
     route('lfo0','filter0.cutoff',2.5,True),route('lfo1','oscillator0.fine',.9,True),
     route('velocity','filter0.cutoff',6),route('macro0','filter0.cutoff',20),
     route('macro1','lfo0.rate',1),route('macro2','fx1.wet',22),
     route('macro3','oscillator2.volume',14)],.32))

SPECS.append(patch('neon-chords','Short brass-like polyphonic retro chord stabs with an envelope sweep and restrained stereo chorus.',
    [osc('analog_warm',.42,84,unison=2.0,detune=.032),
     osc('pwm',.24,48,fine=4.0),osc('analog_mini',.12,62,octave=-1.0)],
    [filt(.32,'moog_lowpass_12',12,4)],
    [env(.018,.43,.35,.19),env(.009,.29,0,.16)],
    [lfo(.11),lfo(.18)],['BITE','BODY','WIDTH','ROOM'],
    [chorus(17,2.6),hall(10,29)],
    [route('env1','filter0.cutoff',22),route('velocity','filter0.cutoff',10),
     route('lfo0','oscillator0.table_position',2.5,True),route('lfo1','oscillator1.fine',.7,True),
     route('macro0','filter0.cutoff',20),route('macro1','oscillator2.volume',17),
     route('macro2','fx0.wet',20),route('macro3','fx1.wet',17)],.39))

SPECS.append(patch('glass-arp','Small glassy pluck with a harmonic edge, single-direction timbral decay and tempo-matched eighth-note echoes.',
    [osc('dying_sine',.50,96),osc('digital_fm',.10,36,octave=1.0)],
    [filt(.43,'lowpass_12',9)],
    [env(.002,.21,0,.095),env(.001,.16,0,.08)],
    [lfo(.14)],['GLASS','DECAY','ECHO','HALO'],
    [delay(18,24),hall(13,34)],
    [route('env1','filter0.cutoff',14),route('env1','oscillator0.table_position',9),
     route('lfo0','oscillator1.table_position',3,True),route('velocity','filter0.cutoff',7),
     route('macro0','oscillator1.volume',19),route('macro1','env0.decay',8),
     route('macro2','fx0.wet',20),route('macro3','fx1.wet',18)],.40,False,12))

SPECS.append(patch('night-hook','Singing mono saw-and-pulse lead with delayed gentle vibrato, a softened top and narrow stereo echoes.',
    [osc('analog_mini',.48,95,unison=3.0,detune=.034),
     osc('pwm',.24,61,fine=-3.0)],
    [filt(.43,'moog_lowpass_12',9,3)],
    [env(.022,.7,.78,.24),env(.02,.44,.18,.18)],
    [lfo(5.2,delay=.24,rise=.20,mono=False),lfo(.12)],['OPEN','BODY','ECHO','SPACE'],
    [delay(14,23),hall(12,31)],
    [route('env1','filter0.cutoff',13),route('lfo0','oscillator0.fine',1.0,True),
     route('lfo0','oscillator1.fine',1.0,True),route('lfo1','oscillator1.table_position',2,True),
     route('velocity','filter0.cutoff',8),route('macro0','filter0.cutoff',21),
     route('macro1','oscillator1.volume',20),route('macro2','fx0.wet',18),
     route('macro3','fx1.wet',20)],.47,True,1,0))

SPECS.append(patch('rain-keys','Soft electric bell keys with a warm fundamental, velocity-sensitive brightness and a longer decaying response.',
    [osc('fm_piano',.42,76),osc('warm_sub',.16,16)],
    [filt(.40,'lowpass_12',5)],
    [env(.006,1.15,0,.55),env(.002,.36,0,.19)],
    [lfo(.17)],['TINE','LENGTH','CHORUS','ROOM'],
    [chorus(11,2),hall(18,41)],
    [route('env1','filter0.cutoff',12),route('velocity','filter0.cutoff',17),
     route('velocity','oscillator0.table_position',7),route('lfo0','oscillator0.fine',.6,True),
     route('macro0','oscillator0.table_position',16),route('macro1','env0.decay',12),
     route('macro2','fx0.wet',19),route('macro3','fx1.wet',18)],.41))

SPECS.append(patch('radio-haze','Quiet tonal radio-like haze with filtered brown noise, slow wavetable motion and a wide dark hall.',
    [osc('harmonic_smooth',.22,35,unison=2.0,detune=.03),
     osc('analog_warm',.13,18,octave=-1.0,fine=-4.0),
     dict(enabled=False),dict(enabled=True,noise_type='Brown',volume=.055)],
    [filt(.32,'bandpass_12',17)],
    [env(1.2,2.4,.62,2.1),env(2.0,3.5,.2,2.0)],
    [lfo(.07),lfo(.19),lfo(.11)],['TUNE','DUST','DRIFT','SPACE'],
    [chorus(13,3),hall(34,62)],
    [route('env1','filter0.cutoff',9),route('lfo0','filter0.cutoff',4,True),
     route('lfo1','oscillator0.table_position',7,True),route('lfo2','oscillator0.pan',12,True),
     route('lfo0','oscillator1.fine',1.6,True),route('macro0','filter0.cutoff',13),
     route('macro1','oscillator3.volume',12),route('macro2','lfo0.rate',1),
     route('macro3','fx1.wet',20)],.31))

for spec in SPECS:
    (HERE/(spec['name']+'-preset-spec.json')).write_text(json.dumps(spec,indent=2)+'\n',encoding='utf-8')
(HERE/'preset-spec.json').write_text(json.dumps(SPECS,indent=2)+'\n',encoding='utf-8')
(HERE/'bindings.json').write_text(json.dumps({s['name']:{'plugin':'Serum 2','midi':'MIDI/'+s['name']+'.mid',
    'preset':'Presets/'+s['name']+'.SerumPreset','macros':[m['name'] for m in s['macros']]} for s in SPECS},indent=2)+'\n',encoding='utf-8')
print('Wrote seven preset specifications and MIDI bindings.')

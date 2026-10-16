from pathlib import Path
import hashlib,json
import numpy as np
from serum_mcp.preset.packer import unpack_file
from serum_mcp.preset.wavetable import read_wav_mono

ROOT=Path(__file__).resolve().parent
WORKSPACE=next(p for p in ROOT.parents if (p/'integrations/serum-mcp').is_dir())
config=json.loads((WORKSPACE/'studio.local.json').read_text(encoding='utf-8'))
tables=Path(config['serum_presets']).parent/'Tables'
report={}
for relative in ['Analog/Basic Shapes.wav','S2 Tables/Default Shapes.wav','S2 Tables/Analog/DM - OSCAR.wav','S2 Tables/Digital/Harmonic Series Smooth.wav']:
    path=tables/relative
    samples,sr=read_wav_mono(path)
    frames=np.asarray(samples).reshape(-1,2048)
    info=[]
    for i,frame in enumerate(frames):
        fft=np.abs(np.fft.rfft(frame))
        info.append({'frame':i,'rms':float(np.sqrt(np.mean(frame**2))),
            'harmonics_1_to_8':(fft[1:9]/max(fft[1],1e-9)).round(4).tolist(),
            'fundamental_energy_fraction':float(fft[1]**2/max(np.sum(fft[1:]**2),1e-9))})
    report[relative]={'sample_rate':sr,'frames':len(frames),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'frame_analysis':info[:12]}
PROJECT=next(p for p in ROOT.parents if (p/'v001').is_dir())
native=unpack_file(PROJECT/'v001/Presets/sub-bass.SerumPreset').data
report['v001_sub_native_defaults']={k:v for k,v in native.items() if k in ['Oscillator0','Oscillator1','RoutingSlot0','VoiceFilter0','Global0']}
(ROOT/'source-analysis.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='v001_sub_native_defaults'},indent=2))
print(json.dumps(report['v001_sub_native_defaults'],indent=2))

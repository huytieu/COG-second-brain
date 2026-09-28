#!/usr/bin/env python3
"""Check music candidates before mixing: tempo, beat phase, loudness curve, and repetition.

usage: music_check.py bed-a.mp3 bed-b.mp3 ...
Prints bpm and beat phase (so scene cuts can be placed on beats), RMS per 2 s (so the intro
is quieter than the body), and the max similarity between 2 s windows at least 8 s apart
(high = the track loops; pick the candidate with the lowest value).
"""
import subprocess, numpy as np, sys
def load(f, sr=22050):
    raw = subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32), sr
for f in sys.argv[1:]:
    y,sr=load(f); hop=256; n=1024
    if len(y) < 8*sr or np.abs(y).max() == 0:
        print(f, 'skipped: shorter than 8 s or silent'); continue
    frames=np.lib.stride_tricks.sliding_window_view(y,n)[::hop]*np.hanning(n)
    S=np.abs(np.fft.rfft(frames,axis=1)); S=np.log1p(S*10)
    flux=np.maximum(0,np.diff(S,axis=0)).sum(1); flux=(flux-flux.mean())/(flux.std()+1e-9)
    fps=sr/hop
    ac=np.correlate(flux,flux,'full')[len(flux)-1:]
    lags=np.arange(len(ac))/fps; bpm_range=(lags>60/180)&(lags<60/80)
    lag=lags[bpm_range][np.argmax(ac[bpm_range])]; bpm=60/lag
    # phase: best offset for a 2.0s grid (and beat grid) using mean flux at grid points
    period=lag; best=None
    for off in np.arange(0,period,1/fps):
        idx=((np.arange(off,len(flux)/fps,period))*fps).astype(int); idx=idx[idx<len(flux)]
        s=flux[idx].mean()
        if best is None or s>best[0]: best=(s,off)
    rms=[20*np.log10(np.sqrt(np.mean(y[int(t*sr):int((t+2)*sr)]**2))+1e-9) for t in range(0,int(len(y)/sr),2)]
    print(f, f"bpm={bpm:.2f} beat_period={period:.4f}s phase={best[1]:.3f}s")
    print('  rms/2s:', ' '.join(f"{r:.0f}" for r in rms))
    win=2*sr; segs=[y[i:i+win] for i in range(0,len(y)-win,win)]
    F=[]
    for sg in segs:
        Sp=np.abs(np.fft.rfft(sg*np.hanning(len(sg))))[:6000]; Sp=np.log1p(Sp.reshape(-1,50).mean(1)); F.append((Sp-Sp.mean())/(Sp.std()+1e-9))
    F=np.array(F); C=F@F.T/F.shape[1]; k=len(F)
    far=[C[i,j] for i in range(k) for j in range(k) if j-i>=4]
    if far: print(f"  repetition: max far-similarity {max(far):.3f}, mean {np.mean(far):.3f}")

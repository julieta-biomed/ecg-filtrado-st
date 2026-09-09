import numpy as np
from scipy import signal

def ecg_sintetico(fs=360, dur=10.0, hr=60.0, amp_r=1.10):
    n=int(fs*dur); t=np.arange(n)/fs; rr=60.0/hr; x=np.zeros(n)
    ondas=[(-0.20,0.15,0.025),(-0.035,-0.10,0.008),(0.0,1.10,0.010),
           (0.035,-0.25,0.010),(0.28,0.30,0.045)]
    picos=[]
    for k in range(int(dur/rr)+2):
        tr=0.35+k*rr
        if tr>dur-0.5: break
        picos.append(tr)
        for c,a,s in ondas:
            x+=a*np.exp(-0.5*((t-(tr+c))/s)**2)
    return t, x*(amp_r/1.10), np.array(picos)

def hp(x,fc,fs,orden=2,fase_cero=True):
    sos=signal.butter(orden,fc,'highpass',fs=fs,output='sos')
    return signal.sosfiltfilt(sos,x) if fase_cero else signal.sosfilt(sos,x)

def nivel_st(x,picos,fs,offset=0.06):
    v=[]
    for tr in picos:
        i=int(tr*fs)
        base=np.mean(x[i-int(0.080*fs):i-int(0.060*fs)])
        j=int((tr+0.040)*fs)
        v.append(np.mean(x[j+int(offset*fs)-2:j+int(offset*fs)+3])-base)
    return np.array(v)

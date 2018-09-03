#!/usr/bin/python

import numpy as np
from scipy.signal import resample_poly, filtfilt, butter, freqz_zpk, freqz, lfilter


def backtoint16(play):
    if play.max() > 2**15 - 1:
        play = play / play.max() * (2**15 - 1)
    if play.min() < -2**15 - 1:
        play = -play / play.min() * (2**15 + 1)
    return play
# #############################################################################1
def speedx(sound_array, factor):
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int),: ]


# --------------------------------------------------------------------------

def Phaseshifting_Timestretching(frame, vp, ts, leng):
    ppp = float(leng)
    leng = int(leng)
    Frame = np.fft.rfft(frame, leng, axis=0)
    phase = np.arctan2(Frame.imag, Frame.real)
    Frame = np.abs(Frame)
    ps = leng + vp
    if ps < leng:
        Frame = Frame =  speedx(Frame, ppp/ps)[0:ps//2+1]#resample_poly(Frame, ps, ppp, window=('kaiser', 1))[0:ps//2+1]
        phase = speedx(phase, ppp/ps)[0:ps//2+1]#resample_poly(phase, ps, ppp, window=('kaiser', 1))
    else:
        Frame =  speedx(Frame, ppp/ps)[0:ps//2+1]#resample_poly(Frame, ps, ppp, window=('kaiser', 1))[0:ps//2+1]#speedx(Frame, ppp/ps)
        phase = speedx(phase, ppp/ps)[0:ps//2+1]
    #Frame[np.abs(Frame) < abs(Frame).max()/50] = 0
    play = np.fft.irfft(Frame*np.exp(1j*phase), ps, axis=0).real
    if ts is False:
        play = resample_poly(play, leng, ps, window=('kaiser', 1))[0:leng]
    return play


def Phaseshifting_Timestretching2(frame, vp, ts, leng=1000):
    #f = speedx(frame, 1/ (2**(-2/12)))
    vp = vp/200
    vp = 2**(vp/12)
    leng = frame.shape[0]
    F = np.fft.rfft(frame, axis=0)
    F = resample_poly(F, int(vp*1000), 1000, axis=0, window=('kaiser', 2))#speedx(F, 1/ (2**(-vp/12)))
    
    f = np.fft.irfft(F, axis=0)
    if ts is False:
        f = resample_poly(f, 1000, int(vp*1000), axis=0, window=('kaiser', 2))[0:leng]

    #f = np.fft.ifft(F,axis=0).real
    #if ts is False:
    #    f = speedx(f, 1/ (2**(vp/12)))
    return f
# ###############################################################################2

def Reverb(reverb_zp=2, reverb_length=2500):
    reverba = np.array([-reverb_zp] + [0]*reverb_length + [-1])
    reverbb = np.array([1] + [0]*reverb_length +  [-reverb_zp])

    _,reverbator = freqz(reverba, reverbb, 5000, whole=True)
    reverbator = reverbator / np.abs(reverbator).max()*2
    reverbator = np.vstack((reverbator, reverbator)).T
    return reverbator, reverb_zp, reverb_length

# ---------------------------------------------------------------
def SimpleReverb(frame, reverbator, leng=1000):
    Frame = np.fft.fft(frame, axis=0)
    Frame *= reverbator
    frame = np.fft.ifft(Frame,axis=0).real
    return frame[4000::,:]

# ---------------------------------------------------------------
def reverb_repeat(w, i, fs, delay, repeats, attenuation):
    repeat_delay = (fs * delay)/1000.0
    play = w[1000*i:1000*(i+1),:].copy()
    for repeating in range(1, repeats):
        scale = 1*attenuation**repeating
        if i > repeat_delay * repeating:
            play += scale * (w[1000*(i-int(repeating * repeat_delay)):1000*(i+1-int(repeating * repeat_delay)),:].copy().astype(np.double))
        
    return play
        
        
# ################################################################3
def Flanging_params(fs,flanging_time=20,flange_max_delay=0.002,flanging_gain=0.9):
    flange_half_period = int(flanging_time * fs/1)
    flange_delay = flange_max_delay * flange_half_period *(np.cos(np.pi*np.arange(0, 2*flange_half_period)*1.0/flange_half_period)) 
    flange_delay = flange_delay.astype(int)
    rem = int(flange_half_period//1000)
    return flange_delay, rem


# ----------------------------------------------------------------
def flanging_effect(frame, flanging_gain, frame_delayed):
    #FF = w[index]*1 + flanging_gain*w[index - flange_delay[1000*(i%rem):1000*(i%rem+1)]]
    FF = frame + flanging_gain * frame_delayed
    return FF

# ##############################################################4
def remove_centered_voice(frame):
    frame[::,0] = frame[::,0] - frame[::,1]
    frame[::,1] = frame[::,0]
    return frame


# ###############################################################5
def phasing_effect(w, TF):
    W = np.fft.rfft(w, axis=0)
    W = W + W * TF
    f = np.fft.irfft(W, axis=0).real
    
    return f[9000::,:]

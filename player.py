#!/user/bin/python


import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import argparse
import pyaudio
from scipy.io import wavfile
import numpy as np
from scipy.signal import resample_poly, filtfilt, butter, freqz_zpk, freqz, lfilter



parser = argparse.ArgumentParser(prog='python3 cur.py', conflict_handler='resolve',description='Flare Player || ver. 1.0')
parser.add_argument('--help',action='store_true',dest='exit', help='show full help of usage')
parser.add_argument('Name', metavar='Name', type=str, nargs='?', help='File name by wave extension')


HELP = '''
##this is a help documentatation of **Flare Player**. 
______________________________________________________________________
usage: python[3] cur.py filename.wav.
requirements are python-curses, pyauio, scipy and numpy.
**curses** manages the player window on the commandline 
environment.
**scipy.io.wavfile** loads the **.wav** files as numpy array, so
 there is no support for other audio formats [yet]. 
**numpy** module calculate the FFT of loaded audio. STFT was driven
by non-overlap windowing signal and performing the FFT on each window.
the length of each window sets on 1000 samples, so it means each window
has a duration equals to 1000/fs seconds.
-----------------------------------------------------------------------
###[Controls on audio effets]:
* up/down keys:  : increase or decrease audio volume.
* left/right keys: step back/forwward by 100/fs seconds.
* r:             : reverse the audio and play it from end to begin!
* v:             : try to reomve voice from the audio
* p/P:           : move forward/backward pitch (if time stretching is false, its change the pitch, when time stretching is true, it changes the playing time)
* s:             : time compress or stretch, try p/P keys.
* f:             : enable or disable time flanging, three keys g/G, h/H, j/J are the control option. this option won't work with repeat or reverbation effects.
** g/G:          : increase/decrease time period of flanging effects. time period is on second scale.
** h/H:          : increase/decrease max delay time of flanging effects.
** j/J:          : increase/decrease flanging gain. flanging gain changes between 0.1~0.9 by 0.1 step.
* z:             : enable/disable reverb effect. this effect won't work alongside the flanging effects.
** b/B:          : literaly, changes position of zero/pole of transfer function. But, in practice, it effects on visibility of effect.
** n/N:          : change the reverbation delay.
* c/C            : increase number of repeat/increase delay between each repeat.
* x/X            : decrease number of repeat/decrease delay between each repeat.
* E:             : Enable/disable filter.
** 0~9:          : change filter magnitude in 10 frequency intervals.
* Space:         : Pause/resume 

------------------------------------------------------------------------
###[Technical issues]:
#### reversing the audio:
Imagine the digital audio as an array like this: [1, 2, 3, 4 ,5]. Normally, playing reads the array from left to right. in revese mode, it read from right to left. it seem useless, don't is?  

#### voice removal:
This is not very perfect. Some of **stereo audios** are recording by **voice cenered** mode, then by subtracting the left and right channels, it is possible to remove (in practice reduce) voice by a little degradation as drawback. Nowadays voice removal is an open topic in both of commercial and academic research.  

#### changing pitch and time stretching:  
Pitch shifting and time stretching are two similar topics. Simple expression, if you digitally **recorded** a sound by sample rate **fs** for example 4000 Hz and **play** it by  **different sample rate**, it causes that playing time changes. in the example if we play the signal by 5000 Hz sample rate, the time was compressed. because, originally it plays 4000 samples in one second of time. But, the second player by 5000 Hz sample rate, plays 5000 samples in one second. so 4000 samples are lower than on second. this works for lower sample rate, too. time stretching is not the only effect when you change the player sample rate. it also changes the sound pitch. But, what is **pitch**? they call it fundemental frequency. when you say a vovel non-stoply on one breath, for example <i> and you say iiiiiiiiiiiiiiiiiiiiiiiii, Technically, your voice is a peridioc signal. this period is a fundemental for <i> in your vocal organs. changing the sample rate not only changes the time duration, but also it changes the pitches. Maybe you seen before on the movies, when the time goes slowly, the pepole sounds turn to lower start of human hearing frequency, Bass. Anf When it goes fast, the sound goes to treble ie. higher end of human hearing.
Don't forget to read wikipeida for pitch and time stretching.
Here to implement both pitch shifting and time stretching systems, I used the numpy.fft on the following structure: each **frame** has a 1000 samples that sampled by **fs**. So, the fourier transform on frame, **Frame**, normally has 1000 samples too. then I do a **resampling** in **frequency domain** and calculate the inverse fourier transform, by new sample number. This means I change the **playing sample rate** aka **time stretching/compressing**, without causing effect on the signal pitch; [if you want to change them together try to change configuration of your player, in my case I use **pyaudio** and audio streamer has a sample rate in its settings].
To change the pitch, I do another **resampling** but in **time domain** and return back the sammple number to 1000. The following graph show the structure:


> [Time Domain]   ======>  [Frequency Domain] : (Resampling) =======> [Time Domain] : Time Stretching =====> [Time Domain] : (Resampling) : Pitch Shifting
you can see the code under pitch shifting section for better undderstanding.

#### Flanging effect:
Flanging effect is kind of delay. But the delay amount changes over a period. the priodic signal can be sinusiod or triagle function, let call that **M[n]**, then Flanging effect derived by this equation:

> M[n] = D/2 * (1 - cos(2 * &pi; * F_flange * n))
> X_Flanging[n] = X[n] + g * X[M[n]]

#### reverbation:
When a sound plays in a room, there are many direct or indirect passible way, that hearer can recieve the sound. direct way is the original sound that comes through the air right into hearer ears. But, sound propagates omnidirectional, so in some direction it goes to the walls and reflected into hearer. The reflected sound spend longgest way than direct sound, so this is hears some amounts of time after the direct one. If we call sound source as "S" and hearer as "h", then following graph show some ways that hearer can hear a sound.

-----------------------
|          /\         |
|         /  \        |
|         h---S       |
|          \  /       |
|           \/        |
-----------------------

Remeber, due to sound propagation speed, the delay may be under 0.3 miliseconds, and attenuation of reflection is considerable, so we can't experience this in usual room we have, but in bathrooms we can try!
In commercial softwares or even hardwares, there are many implementation of reverb effect by many parameters, such as size of room, number of walls and etc. Here is use a very simple allpass transfer function to filter sound signal by reverb filter (generaly to search over internet try reverb convolution) like this:

>                       -D
>             -a  +    z 
>Rev-F[z] = ----------------
>                       -D
>              1  -  a z 

#### Repeat:
very simple;y, I just add delayed signal to original signal. this delay amount is fixed over time. 

#### Filter:
 > TODO

'''


args = parser.parse_args()

if args.exit:
    print(HELP)
    exit()
else:
    print(args)
FILE_NAME = args.Name
print(FILE_NAME)

# ########################### Fucntion: # ##########################
def makeI(c, width, pos=1):
	N = c.shape[0]
	I = [0]*N
	idx = int(N*pos / width)
	chars = ['#'] * N
	for i in range(N):
		value = np.floor(c[i]*N).astype(np.int)
		I[i] = value
		if i <= idx:
			chars[i] = '#'
		else:
			chars[i] = '@'
	return I, chars


# ########time:
def return_time(i, fs=None, s=1000):
	if fs is not None:
		t = i*s  /fs
	else:
		t = i
	h = int(t // 3600)
	if h > 0:
		m = int((t - h*3600)//60)
		text = str(h) + ':' + str(m) + ':' + str((t - h*3600 - m*60))[0:2]
	else:
		m = int(t // 60)
		text = str(m) + ':' + str((t - m*60))[0:4]
	return text


# #### upsampleing
def speedx(sound_array, factor):
	""" Multiplies the sound's speed by some `factor` """
	indices = np.round( np.arange(0, len(sound_array), factor) )
	indices = indices[indices < len(sound_array)].astype(int)
	return sound_array[ indices.astype(int),: ]


## #### Reverb
def Reverb(reverb_zp=2, reverb_length=2500):
	reverba = np.array([-reverb_zp] + [0]*reverb_length + [-1])
	reverbb = np.array([1] + [0]*reverb_length +  [-reverb_zp])

	_,reverbator = freqz(reverba, reverbb, 5000, whole=True)
	reverbator = reverbator / np.abs(reverbator).max()*2
	reverbator = np.vstack((reverbator, reverbator)).T
	return reverbator, reverb_zp, reverb_length


# #### set flanging parameters:
def Flanging_params(fs,flanging_time=20,flange_max_delay=0.002,flanging_gain=0.9):
	flange_half_period = int(flanging_time * fs/1)
	flange_delay = flange_max_delay * flange_half_period *(np.cos(np.pi*np.arange(0, 2*flange_half_period)/flange_half_period)) 
	flange_delay = flange_delay.astype(int)
	rem = int(flange_half_period//1000)
	return flange_delay, flanging_gain, rem, flanging_time, flange_max_delay
	



## init the TUI: ######
curses.initscr()
win = curses.newwin(36, 50,0,0)
win.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(0)
curses.start_color()

win.border(0)
win.nodelay(True)
win.addstr(0, 2, '.::' + FILE_NAME[0:30] + '::. ')
win.addstr(1, 1, '='*48)
key = 0




###############init player:
fs, w = wavfile.read(FILE_NAME)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=2, rate=fs, frames_per_buffer=100, output=True)


i = 0
M = w.shape[0] * w.max() * 50 / ((w.sum(1)/2)**2).sum()**0.5 / 2**0.5

pause = False

MONO = False if w.shape[-1] == 2 else True
TIME = w.shape[0]/fs

mag = 0

width = w.shape[0] / 1000
B, A = butter(5, 0.5, btype='low', analog=False)

vol = 100
pitch_shift = 0
time_stretch = False
voice = True
reverse = False
EQ = False
Equalizer = np.array([20, 18, 16, 14, 12, 10, 12, 14, 16, 18], np.int)
Eqbins = np.linspace(0, np.pi, 12)[1:-1]


reverbator, reverb_zp, reverb_length = Reverb()

reverb = False

repeat_scale = 0
repeat_delay = int(fs/10000) + 1
repeat_delay_base = 1

flanging = False ##TODO
flange_delay, flanging_gain, rem, flanging_time, flange_max_delay = Flanging_params(fs=fs,flanging_time=20, flange_max_delay=0.002, flanging_gain=0.9)



phasing = False ##TODO
phasing_freq = np.arange(-5000, 5000)/10000 ##TODO
phaser_TF = 1
for k in [0.1]*0 + [0.2]*0 + [0.9]*0 + [0.32]*0 +[0.5]*100:
	phaser_TF = phaser_TF * ((k + 1 * np.exp(-1j*2*np.pi*phasing_freq*1))/((1 + k * np.exp(-1j*2*np.pi*phasing_freq*1))))##TODO
phaser_TF = 1 *0 + np.vstack((phaser_TF, phaser_TF)).T

test = False

#### MAIN LOOP: ###############

while key != 27 and i < width - 1:
	win.border(0)
	win.addstr(0, 2, '.::' + FILE_NAME[0:30] + '::.')
	win.timeout(0)
	
##############################

	if not pause:
		if reverse:
			frame = (w[::-1,:][1000*i:1000*(i+1),:].astype(np.double) * vol / 100)
		else:
			frame = (w[1000*i:1000*(i+1),:].astype(np.double) * vol / 100)

		#### processors:
		# voice reduction:
		if i > 5:
			play = frame
			if not voice and not MONO:
				#frame[::,0] = frame[::,0] - frame[::,1]
				#frame[::,1] = frame[::,0]
				a = 1 * frame[::,0] + 1 * frame[::,1]
				b = 0.8 * frame[::,0] + 0.2* frame[::,1]
				frame[::,0] = a
				frame[::,1] = b
				
			if reverb:
				if reverse:
					FF = (w[::-1,:][1000*i-4000:1000*(i+1),:].astype(np.double) * vol / 100)
				else:
					FF = (w[1000*i-4000:1000*(i+1),:].astype(np.double) * vol / 100)
				if not voice and not MONO:
					FF[::,0] = FF[::,0] - FF[::,1]
					FF[::,1] = FF[::,0]
				Frame = np.fft.fft(FF, axis=0)
				Frame = Frame*reverbator
				play = np.fft.ifft(Frame, axis=0).real# + FF
				#FF = (w[1000*i-2000:1000*(i+1),:].astype(np.double) * vol / 100)
				#FF = play
				#play = lfilter(reverbb, reverba, FF, axis=0) #+ FF
				play = play[4000::,:]

			###TODO
			if test:
				FF = w[1000*i:1000*(i+1),:].astype(np.double)
				FF_i1 = w[::-1,:][1000*(i):1000*(i+1),:].astype(np.double)
				#FF_i2 = w[1000*i-4000:1000*(i+1)-4000,:].astype(np.double)
				#FF[::,1] = FF[::,0]*0.5 + FF[::,1]*0.5
				#FF[::,0] = FF_i2[::,1]*0.5 + FF_i1[::,0]*0.5
				ch0 = FF[::,0]#+FF_i2[::,1]*0.5 #+ FF[::,1]/3
				ch1 = FF_i1[::,1]#FF_i1[::,1]#*0.5+FF_i1[::,1] #+ FF[::,0]/3
				FF[::,0] = ch0
				FF[::,1] = ch1
				play = FF
			
			if phasing and i > 10:
				if reverse:
					FF = (w[::-1,:][1000*i-9000:1000*(i+1),:].astype(np.double) * vol / 100)
				else:
					FF = (w[1000*i-9000:1000*(i+1),:].astype(np.double) * vol / 100)
				if not voice and not MONO:
					FF[::,0] = FF[::,0] - FF[::,1]
					FF[::,1] = FF[::,0]
					
				Frame = np.fft.fft(FF)
				Frame = Frame*0 + Frame * phaser_TF
				FF = np.fft.ifft(Frame).real
				
				
				play = FF[9000::,:]
				#play[::,:] = play[::,:] + FF[49000 - flang_index[0:1000][::-1]]
				
				#play = FF[49000::,:] + 0.5*FF[49000-2000::3,:] + 0.25*FF[49000-4000::5,:] + 0.1*FF[49000-8000::9,:] #+ FF[]#FF[50000-2-flang_index,:] * 1
				#play = FF[49000::,:]
				
			### Flanging:
			if flanging:# and i > fs * flanging_time /1000:
				index = np.arange(1000*i, 1000 * (i+1)).astype(np.int)
				if reverse:
					FF = w[::-1][index]*1 + flanging_gain*w[::-1][index - flange_delay[1000*(i%rem):1000*(i%rem+1)]]
				else:
					FF = w[index]*1 + flanging_gain*w[index - flange_delay[1000*(i%rem):1000*(i%rem+1)]]
					
				if not voice and not MONO:
					FF[::,0] = FF[::,0] - FF[::,1]
					FF[::,1] = FF[::,0]
					
				play = FF.astype(np.double)

					
			if repeat_scale != 0:
				repeats = np.exp(-1 * np.arange(0, repeat_delay, repeat_delay/(1 +  repeat_scale))/repeat_delay)
				for repeating in range(1, len(repeats)):
					scale = repeats[repeating]
					if i > repeat_delay * repeating:
						if reverse:
							play += scale * (w[::-1,:][1000*(i-repeating * repeat_delay):1000*(i+1-repeating * repeat_delay),:].astype(np.double) * vol / 100)
						else:
							play += scale * (w[1000*(i-repeating * repeat_delay):1000*(i+1-repeating * repeat_delay),:].astype(np.double) * vol / 100)
				if not voice and not MONO:
					play[::,0] = play[::,0] - play[::,1]
					play[::,1] = play[::,0]
			
			# pitch shiftting and time stretching
			if pitch_shift != 0:
				ppp = 1000
				FF = play#FF = (w[1000*i-(ppp-1000):1000*(i+1),:].astype(np.double) * vol / 100)
				Frame = np.fft.rfft(FF, ppp, axis=0)
				phase = np.arctan2(Frame.imag, Frame.real)
				#phase = np.vstack((phase[0:-1,:], phase[1::,:][::-1,:]))
				Frame = np.abs(Frame)
				ps = ppp + pitch_shift
				if ps < ppp:
					Frame = Frame =  speedx(Frame, ppp/ps)[0:ps//2+1]#resample_poly(Frame, ps, ppp, window=('kaiser', 1))[0:ps//2+1]
					phase = speedx(phase, ppp/ps)[0:ps//2+1]#resample_poly(phase, ps, ppp, window=('kaiser', 1))
				else:
					Frame =  speedx(Frame, ppp/ps)[0:ps//2+1]#resample_poly(Frame, ps, ppp, window=('kaiser', 1))[0:ps//2+1]#speedx(Frame, ppp/ps)
					phase = speedx(phase, ppp/ps)[0:ps//2+1]
				#Frame[np.abs(Frame) < abs(Frame).max()/50] = 0
				play = np.fft.irfft(Frame*np.exp(1j*phase), ps, axis=0).real
				if time_stretch is False:
					if ps > ppp*100:
						play = resample_poly(play, ppp, ps, window=('kaiser', 1))
					else:
						play = speedx(play, ps/ppp)
					play = play[(ppp-1000)::,:]
					
				#play = 0.01*play - 0.99* filtfilt(B, A, play, axis=0)
				
				play = play
				
			#else:
			#	play = frame
				
			if EQ:
				Frame = np.fft.rfft(play, axis=0)
				#E = np.array([Equalizer[0]]*100+[Equalizer[1]]*100+[Equalizer[2]]*100+[Equalizer[3]]*100+[Equalizer[4]]*100+[Equalizer[5]]*100+[Equalizer[6]]*100+[Equalizer[7]]*100+[Equalizer[8]]*100+[Equalizer[9]]*100)
				#E = freqz(1, Equalizer, Frame.shape[0]//2)[1]
				
				#E = freqz_zpk((20 - Equalizer)*np.exp(1j*Eqbins), Equalizer*np.exp(1j*Eqbins), 1 , Frame.shape[0]//2+1,whole=False)[1]
				E = freqz_zpk([],(Equalizer)/10*np.exp(1j*Eqbins), 1 , Frame.shape[0],whole=False)[1]
				E = E / E.max()
				#E = np.hstack((E, E[::-1]))
				E = np.vstack((E,E)).T
				Frame *= E
				#play = np.fft.ifft(Frame, axis=0).real
				'''
				L = Frame.shape[0]
				L10 = int(L + L*0.1)
				a = np.int(L10/10)
				y = np.array([-i/a + 1 for i in range(a)])
				f0 = np.hstack((y, np.zeros((L - a))))
				f0 = np.vstack((f0,f0)).T
				yi = y[::-1]
				##f = [f0]
				E = 0 + f0 * Equalizer[0]/10
				for eindex in range(1, 10):
					l = np.hstack((np.zeros((eindex-1)*a), yi, y, np.zeros(L10 - (2+eindex-1)*a)))[0:L]
					l = np.vstack((l, l)).T
					E = E + l * Equalizer[eindex]/10
				E = E / 1.02
				'''
				
				play = np.fft.irfft(Frame * E, axis=0).real
				
				
		##################

			if play.max() > 2**15 - 1:
				play = play / play.max() * (2**15 - 1)
			if play.min() < -2**15 - 1:
				play = -play / play.min() * (2**15 + 1)
		else:
			play = frame
		###############

		stream.write(play.astype(np.int16).tostring())
		i += 1
	else:
		win.addstr(10, 10, 'Paused.')
		frame = np.zeros((1000,2))

	frame = frame.sum(1)/2 * 100 / vol##TODO
	
	mag = 0.1 * np.abs(np.fft.fft(frame[0:-1:20]))/M + mag * (0.9)
	mag[mag > 1] = 1

	spec, ind = makeI(mag[0:25], width, i)



	
	key = win.getch()
	if key == ord(' '):
		pause = not pause
	elif key == KEY_LEFT and i > 100:
		i -= 100
	elif key == KEY_RIGHT and i <= width:
		i += 100
	elif key == KEY_UP and vol < 100:
		vol += 1
	elif key == KEY_DOWN and vol > 1:
		vol -= 1
	elif key == ord('p') and pitch_shift < 800:
		pitch_shift += 10
	elif key == ord('P') and pitch_shift > -800:
		pitch_shift -= 10
	elif key == ord('s'):
		time_stretch = not time_stretch
	elif key == ord('r'):
		reverse = not reverse
	elif key == ord('v'):
		voice = not voice
	## EQ: ''' """"""""""""""""""""""" '''
	elif key == ord('e'):
		EQ = not EQ
	# increase :
	elif key == ord('1') and Equalizer[0] < 20:
		Equalizer[0] += 1
	elif key == ord('2') and Equalizer[1] < 20:
		Equalizer[1] += 1
	elif key == ord('3') and Equalizer[2] < 20:
		Equalizer[2] += 1
	elif key == ord('4') and Equalizer[3] < 20:
		Equalizer[3] += 1
	elif key == ord('5') and Equalizer[4] < 20:
		Equalizer[4] += 1
	elif key == ord('6') and Equalizer[5] < 20:
		Equalizer[5] += 1
	elif key == ord('7') and Equalizer[6] < 20:
		Equalizer[6] += 1
	elif key == ord('8') and Equalizer[7] < 20:
		Equalizer[7] += 1
	elif key == ord('9') and Equalizer[8] < 20:
		Equalizer[8] += 1
	elif key == ord('0') and Equalizer[9] < 20:
		Equalizer[9] += 1
	# decrease :
	elif key == ord('!') and Equalizer[0] > 0:
		Equalizer[0] -= 1
	elif key == ord('@') and Equalizer[1] > 0:
		Equalizer[1] -= 1
	elif key == ord('#') and Equalizer[2] > 0:
		Equalizer[2] -= 1
	elif key == ord('$') and Equalizer[3] > 0:
		Equalizer[3] -= 1
	elif key == ord('%') and Equalizer[4] > 0:
		Equalizer[4] -= 1
	elif key == ord('^') and Equalizer[5] > 0:
		Equalizer[5] -= 1
	elif key == ord('&') and Equalizer[6] > 0:
		Equalizer[6] -= 1
	elif key == ord('*') and Equalizer[7] > 0:
		Equalizer[7] -= 1
	elif key == ord('(') and Equalizer[8] > 0:
		Equalizer[8] -= 1
	elif key == ord(')') and Equalizer[9] > 0:
		Equalizer[9] -= 1
    ######## reverb:
	elif key == ord('z'):
		reverb = not reverb
		reverbator, reverb_zp, reverb_length = Reverb(reverb_zp, reverb_length)
		
	elif key == ord('b'):
		reverb_zp += 0.1 if reverb_zp < 5 else 0
		reverb_zp = reverb_zp if reverb_zp < 5 else 5
		reverb = False
	
	elif key == ord('B'):
		reverb_zp -= 0.1 if reverb_zp > 1.1 else 0
		reverb_zp = reverb_zp if reverb_zp > 1.1 else 1.1
		reverb = False
		
	elif key == ord('n'):
		reverb_length += 100 if reverb_length < 2500 else 0
		reverb_length = reverb_length if reverb_length < 2500 else 2500
		reverb = False
		
	elif key == ord('N'):
		reverb_length -= 100 if reverb_length > 100 else 0
		reverb_length = reverb_length if reverb_length > 100 else 100
		reverb = False
		
	# repeat:
	elif key == ord('x'):
		repeat_scale = repeat_scale - 1 if repeat_scale > 0 else 0
	elif key == ord('c'):
		repeat_scale = repeat_scale + 1 if repeat_scale < 5 else 5
	elif key == ord('X'):
		repeat_delay //= repeat_delay_base
		repeat_delay_base = repeat_delay_base - 1 if repeat_delay_base > 1 else 1
		repeat_delay *= repeat_delay_base
	elif key == ord('C'):
		repeat_delay //= repeat_delay_base
		repeat_delay_base = repeat_delay_base + 1 if repeat_delay_base < 10 else 10
		repeat_delay *= repeat_delay_base
	### Flanging:
	elif key == ord('f'):
		flanging = not flanging
		if flanging:
			flange_delay, flanging_gain, rem, flanging_time, flange_max_delay = Flanging_params(fs=fs,flanging_time=flanging_time, flange_max_delay=flange_max_delay, flanging_gain=flanging_gain)
	elif key == ord('g'):
		flanging_time += 0.1 if flanging_time < 30 else 0
		flanging_time = flanging_time if flanging_time < 30 else 30
		flanging = False
	elif key == ord('G'):
		flanging_time -= 0.1 if flanging_time > 0.1 else 0
		flanging_time = flanging_time if flanging_time > 0.1 else 0.1
		flanging = False
	elif key == ord('h'):
		flange_max_delay += 0.001 if flange_max_delay < 0.1 else 0
		flange_max_delay = 0.1 if flange_max_delay > 0.1 else flange_max_delay
		flanging = False
	elif key == ord('H'):
		flange_max_delay -= 0.001 if flange_max_delay > 0.0001 else 0
		flange_max_delay = 0.0001 if flange_max_delay < 0.0001 else flange_max_delay
		flanging = False
	elif key == ord('j'):
		flanging_gain += 0.1 if flanging_gain < 0.9 else 0
		flanging_gain = 0.9 if flanging_gain > 0.9 else flanging_gain
		flanging = False
	elif key == ord('J'):
		flanging_gain -= 0.1 if flanging_gain > 0.1 else 0
		flanging_gain = 0.1 if flanging_gain < 0.1 else flanging_gain
		flanging = False
	elif key == ord('l'):
		test = not test
	########
	else:
		pass
    


	for line in range(2, 27):
		win.addstr(line, 1, ' '*48)
	
	curses.curs_set(0)
	for line in range(2,27):
		win.addstr(line,1, '|' + ind[line-2]*(spec[line-2]*2))
	
	k = int(34*i/width)
	win.addstr(27, 1, '='*48)
	win.addstr(28, 7, '['+'='*k+' '*(34-k))
	win.addstr(28, 42, ']' + return_time(TIME - i*1000/fs)[0:7])
	win.addstr(28, 1,  return_time(i, fs)[0:7])
	win.addstr(29, 1, '|-|vol:%3d'%(vol) + '|pitch shift:%4d'%(pitch_shift)+'|time stretching:'+str(time_stretch)[0]+'|-|')
	win.addstr(30, 1, '|'+'-'*14 + '|voice:' + str(voice)[0] + '|reverse:'+str(reverse)[0]+'|'+'-'*13+'|')
	win.addstr(31, 1, '|'+'-'*3+'|'+''.join(['%2d|'%(k) for k in Equalizer])+'|Filter:'+str(EQ)[0]+'|'+'-'*2+'|')
	win.addstr(32, 1, '|flange:'+str(flanging)[0]+ '|time:%2.1f'%(flanging_time) +'(s)|Delay:%1.4f'%(flange_max_delay)+'(s)|gain:%1.1f'%(flanging_gain)+'|')
	win.addstr(33, 1, '|'+ '-'*6 +'|reverb:'+str(reverb)[0]+' | z/p: %1.1f'%(reverb_zp)+' | depth:%4d'%(reverb_length)+'|'+'-'*6+'|')
	win.addstr(34, 1, '|' +'-'*2 + '|repeat:'+str(repeat_scale != 0)[0]+ '|repeat number:' + str(int(repeat_scale)) + '|delay : %1.2f'%(repeat_delay*1000/fs)+' (s)'+'-'  * 2+'|')
	
	win.addstr(35, 1, '='*48)
	win.refresh()

win.erase()
win.clear()
win.refresh()
curses.endwin()

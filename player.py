#1/user/bin/python


import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import argparse
import pyaudio
from scipy.io import wavfile
import numpy as np
from scipy.signal import resample_poly, filtfilt, butter, freqz_zpk, freqz



parser = argparse.ArgumentParser(description='Flare Player || ver. 1.0')
parser.add_argument('Name', metavar='Name', type=str, nargs='+', help='File name by wave extension')

args = parser.parse_args()

FILE_NAME = args.Name[0]
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








## init the TUI: ######
curses.initscr()
win = curses.newwin(30, 50,0,0)
win.keypad(True)
curses.noecho()
curses.cbreak()
curses.curs_set(0)
curses.start_color()

win.border(0)
win.nodelay(True)
win.addstr(0, 2, '.::Now Playing: ' + FILE_NAME + '::. ')

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

reverba = np.array([-1.9, 0, 1])
reverbb = np.array([1    , 0, -1.9])

#reverbb = np.array([1,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.2])
_,reverbator = freqz(reverba, reverbb, 1000, whole=True)
reverbator = reverbator / np.abs(reverbator).max()
reverbator = np.vstack((reverbator, reverbator)).T
reverb = False

#### MAIN LOOP: ###############

while key != 27 and i < width - 1:
	win.border(0)
	win.addstr(0, 2, '.::Now Playing: ' + FILE_NAME + '::.')
	win.timeout(0)
	
##############################

	if not pause:
		if reverse:
			frame = (w[::-1,:][1000*i:1000*(i+1),:].astype(np.double) * vol / 100)
		else:
			frame = (w[1000*i:1000*(i+1),:].astype(np.double) * vol / 100)

		#### processors:
		# voice reduction:
		if not voice and not MONO:
			frame[::,0] = frame[::,0] - frame[::,1]
			frame[::,1] = frame[::,0]
		# pitch shiftting and time stretching
		if pitch_shift != 0:
			Frame = np.fft.rfft(frame, 1000, axis=0)
			ps = 1000 + pitch_shift
			if ps < 1000:
				Frame = resample_poly(Frame, ps, 1000, window=('kaiser', 1))
			else:
				Frame = speedx(Frame, 1000/ps)
			#Frame[np.abs(Frame) < abs(Frame).max()/50] = 0
			play = np.fft.irfft(Frame, ps, axis=0).real
			if time_stretch is False:
				if ps < 2000:
					play = resample_poly(play, 1000, ps, window=('kaiser', 1))
				else:
					play = speedx(play, ps/1000)
		
			play = 0.01*play - 0.99* filtfilt(B, A, play, axis=0)
            
			play = play
		else:
			play = frame

		if EQ:
			Frame = np.fft.rfft(play)
			#E = np.array([Equalizer[0]]*100+[Equalizer[1]]*100+[Equalizer[2]]*100+[Equalizer[3]]*100+[Equalizer[4]]*100+[Equalizer[5]]*100+[Equalizer[6]]*100+[Equalizer[7]]*100+[Equalizer[8]]*100+[Equalizer[9]]*100)
			#E = freqz(1, Equalizer, Frame.shape[0]//2)[1]
			E = freqz_zpk((20 - Equalizer)*np.exp(1j*Eqbins), Equalizer*np.exp(1j*Eqbins), 1 , Frame.shape[0]//2)[1]
			E = E / E.max()
			E = np.hstack((E, E[::-1]))
			E = np.vstack((E,E)).T
			Frame *= np.abs(E)
			play = np.fft.irfft(Frame).real
        
		if reverb:
			Frame = np.fft.fft(play)
			Frame = Frame*reverbator
			play = np.fft.ifft(Frame).real

			#play = filtfilt(reverbb, reverba, play, axis=0)/(3.5*10**25)

		###############

		stream.write(play.astype(np.int16).tostring())
		i += 1
	else:
		win.addstr(10, 10, 'Paused.')
		frame = np.zeros((1000,2))

	frame = frame.sum(1)/2 * 100 / vol
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
	elif key == ord('o') and pitch_shift > -800:
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
    ########
	elif key == ord('z'):
		reverb = not reverb
	else:
		pass
    


	for line in range(1, 26):
		win.addstr(line, 1, ' '*48)
	
	curses.curs_set(0)
	for line in range(1,26):
		win.addstr(line,1, ind[line-1]*spec[line-1]*2)
	
	k = int(34*i/width)
	win.addstr(26, 8, '='*k+' '*(34-k))
	win.addstr(26, 43,  return_time(TIME - i*1000/fs)[0:7])
	win.addstr(26, 1,  return_time(i, fs)[0:7])
	win.addstr(27, 1, '|vol:' + str(vol) + '|pitch shift:'+str(pitch_shift)+'|time stretching:'+str(time_stretch)+'|')
	win.addstr(28, 1, '|voice:' + str(voice) + '|reverse:'+str(reverse)+'|' + ' '*18 + '|')
	win.addstr(29, 1, '|'+''.join(str(k)[0:3] + '|' for k in Equalizer)+'|EQ:'+str(EQ)[0]+'|')
	
	win.refresh()

win.erase()
win.clear()
win.refresh()
curses.endwin()

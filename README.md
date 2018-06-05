# Spectrogram-Wav-Player
Simple Spectrogram based on wav player

### Spectogram Wav Player:
this is very simple audio player that supports only **wav** formats, that can show [**Spectogram**][1] simultaneusly.
the structure is quite simple, **scipy** packages can handle *wav* file by *scipy.io.wavfile*. 
to calculate *Spectrogram* you need separate audio into some local windows, and then, in each window just calculate [**FFT**][2] by module **numpy.fft.fft**.
In this simple example I just choose windows by 1000 point samples from input audio, and resampling into 100 point to decreasing calculation time. 

#### requirements for this version:
* opencv2: since *cv2.imshow* is fast I use this module
* nmupy:  to create image of spectogram and calculation of *fft*
* scipy: to load wav file
* pyaudio: to stream wav file on the output channel

#### forward looking:
here I must try python *PIL* and *pyqt* to investigation of showing speed.

[1]: https://en.wikipedia.org/wiki/Spectrogram
[2]: https://en.wikipedia.org/wiki/Fast_Fourier_transform

***

<p style="dir=rtl;text-align=right"> <h3> طیف نگار صوتی </h3></p>

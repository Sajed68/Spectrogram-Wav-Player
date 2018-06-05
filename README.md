# Spectrogram-Wav-Player
Simple Spectrogram based on wav player

### Spectogram Wav Player:
this is very simple audio player that supports only **wav** formats, that can show [**Spectogram**][1] simultaneusly.
the structure is quite simple, **scipy** packages can handle *wav* file by *scipy.io.wavfile*. 
to calculate *Spectrogram* you need separate audio into some local windows, and then, in each window just calculate [**FFT**][2] by module **numpy.fft.fft**.
In this simple example I just choose windows by 1000 point samples from input audio, and resampling into 100 point to decreasing calculation time. 

[1]: https://en.wikipedia.org/wiki/Spectrogram
[2]: https://en.wikipedia.org/wiki/Fast_Fourier_transform

# Spectrogram-Wav-Player
Simple Spectrogram based on wav player

### Spectogram Wav Player:
this is very simple audio player that supports only **wav** formats, that can show [**Spectogram**][1] simultaneusly.
the structure is quite simple, **scipy** packages can handle *wav* file by *scipy.io.wavfile*. 
to calculate *Spectrogram* you need separate audio into some local windows, and then, in each window just calculate [**FFT**][2] by module **numpy.fft.fft**.
In this simple example I just choose windows by 1000 point samples from input audio, and resampling into 100 point to decreasing calculation time. 

#### requirements for this version:
* opencv2: since *cv2.imshow* is fast I use this module
* numpy:  to create image of spectogram and calculation of *fft*
* scipy: to load wav file
* pyaudio: to stream wav file on the output channel

#### looking forward:
here I must try python *PIL* and *pyqt* to investigation of showing speed.



***
<p style="direction:rtl;text-align:right"> <h3> طیف نگار صوتی </h3> </p>

**[طیف نگار][1]**
نمایش محتوای فرکانسی یک سیگنال صوتی یا به طور کلی هر سیگنال در زمان‌های مختلف است. برای این منظور به طور معمول از 
[تبدیل فوریه زمان کوتاه][3]
استفاده می‌شود.
روش کار به این صورت است که فایل صوتی به تکه‌های کوچک شامل ۱۰۰۰ نمونه تقسیم می‌شود. سپس در هر پنجره به طور مجزا تبدیل فوریه استخراج می‌شود.
برای محاسبه تبدیل فوریه، در هر پنجره نمونه برداری با نرخ ۰/۱ فقط برای کاهش زمان محاسبه انجام می‌شود. 
 


[1]: https://en.wikipedia.org/wiki/Spectrogram
[2]: https://en.wikipedia.org/wiki/Fast_Fourier_transform
[3]: https://fa.wikipedia.org/wiki/%D8%AA%D8%A8%D8%AF%DB%8C%D9%84_%D9%81%D9%88%D8%B1%DB%8C%D9%87_%D8%B2%D9%85%D8%A7%D9%86_%DA%A9%D9%88%D8%AA%D8%A7%D9%87

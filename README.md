# Spectrogram-Wav-Player
Simple Spectrogram based on wav player

### Spectogram Wav Player:
this is very simple audio player that supports only **wav** formats, that can show [**Spectogram**][1] simultaneusly.
the structure is quite simple, **scipy** packages can handle *wav* file by *scipy.io.wavfile*. 
to calculate *Spectrogram* you need separate audio into some local windows, and then, in each window just calculate [**FFT**][2] by module **numpy.fft.fft**.
In this simple example I just choose windows by 1000 point samples from input audio, and resampling into 100 point to decreasing calculation time. 

#### requirements for this version:
* python curses ( I think this is a default madule!)
* ~~opencv2: since *cv2.imshow* is fast I use this module~~
* ~~numpy:  to create image of spectogram and calculation of *fft*~~
* scipy.io: to load wav file
* scipy.signal to do some filters
* pyaudio: to stream wav file on the output channel

#### looking forward:
here I must try ~~python *PIL* and~~ *pyQt* to investigation of showing speed.

#### keyboard usage:
* press 0~9 key to costumize the equalizer
* E to toggle equalizer filter
* v to remove voice by dividing left and right channel
* p and o for pitch shifting
* s to time stretching
* r to revese the sound!
* left/right arrow to move forward and backward
* up/down arrow keys to change volume

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


----------------------------------------------------------------------

## this is a help documentatation of **Player**. 
---------------------------------------------------------------------

usage: python3 cur.py filename.wav.
requirements are python-curses, pyauio, scipy and numpy.
**curses** manages the player window on the commandline 
environment.
**scipy.io.wavfile** loads the **.wav** files as numpy array, so
 there is no support for other audio formats \[yet]. 
**numpy** module calculate the FFT of loaded audio. STFT was driven
by non-overlap windowing signal and performing the FFT on each window.
the length of each window sets on 1000 samples, so it means each window
has a duration equals to 1000/fs seconds.

-----------------------------------------------------------------------
### [Controls on audio effets]:
* up/down keys:  : increase or decrease audio volume.
* left/right keys: step back/forwward by 100/fs seconds.
* r:             : reverse the audio and play it from end to begin!
* v:             : try to reomve voice from the audio
* p/P:           : move forward/backward pitch (if time stretching is false, its change the pitch, when time stretching is true, it changes the playing time)
* s:             : time compress or stretch, try p/P keys.
* f:             : enable or disable time flanging, three keys g/G, h/H, j/J are the control option. this option won't work with repeat or reverbation effects.
  * g/G:         : increase/decrease time period of flanging effects. time period is on second scale.
  * h/H:         : increase/decrease max delay time of flanging effects.
  * j/J:         : increase/decrease flanging gain. flanging gain changes between 0.1~0.9 by 0.1 step.
* z:             : enable/disable reverb effect. this effect won't work alongside the flanging effects.
  * b/B:         : literaly, changes position of zero/pole of transfer function. But, in practice, it effects on visibility of effect.
  * n/N:         : change the reverbation delay.
* c/C            : increase number of repeat/increase delay between each repeat.
* x/X            : decrease number of repeat/decrease delay between each repeat.
* E:             : Enable/disable filter.
  * 0~9:         : change filter magnitude in 10 frequency intervals.
* Space:         : Pause/resume 

------------------------------------------------------------------------

### [Technical issues]:
#### reversing the audio:
Imagine the digital audio as an array like this: \[1, 2, 3, 4 ,5]. Normally, playing reads the array from left to right. in revese mode, it read from right to left. it seem useless, don't is?  

#### voice removal:
This is not very perfect. Some of **stereo audios** are recording by **voice cenered** mode, then by subtracting the left and right channels, it is possible to remove (in practice reduce) voice by a little degradation as drawback. Nowadays voice removal is an open topic in both of commercial and academic research.  

#### changing pitch and time stretching:  
Pitch shifting and time stretching are two similar topics. Simple expression, if you digitally **recorded** a sound by sample rate **fs** for example 4000 Hz and **play** it by  **different sample rate**, it causes that playing time changes. in the example if we play the signal by 5000 Hz sample rate, the time was compressed. because, originally it plays 4000 samples in one second of time. But, the second player by 5000 Hz sample rate, plays 5000 samples in one second. so 4000 samples are lower than on second. this works for lower sample rate, too. time stretching is not the only effect when you change the player sample rate. it also changes the sound pitch. But, what is **pitch**? they call it fundemental frequency. when you say a vovel non-stoply on one breath, for example <i> and you say iiiiiiiiiiiiiiiiiiiiiiiii, Technically, your voice is a peridioc signal. this period is a fundemental for <i> in your vocal organs. changing the sample rate not only changes the time duration, but also it changes the pitches. Maybe you seen before on the movies, when the time goes slowly, the pepole sounds turn to lower start of human hearing frequency, Bass. Anf When it goes fast, the sound goes to treble ie. higher end of human hearing.
Don't forget to read wikipeida for pitch and time stretching.
Here to implement both pitch shifting and time stretching systems, I used the numpy.fft on the following structure: each **frame** has a 1000 samples that sampled by **fs**. So, the fourier transform on frame, **Frame**, normally has 1000 samples too. then I do a **resampling** in **frequency domain** and calculate the inverse fourier transform, by new sample number. This means I change the **playing sample rate** aka **time stretching/compressing**, without causing effect on the signal pitch; [if you want to change them together try to change configuration of your player, in my case I use **pyaudio** and audio streamer has a sample rate in its settings].
To change the pitch, I do another **resampling** but in **time domain** and return back the sammple number to 1000. The following graph show the structure:


> [Time Domain] ====>  [Frequency Domain] : (Resampling) ====> [Time Domain] : Time Stretching ====> [Time Domain] : (Resampling) : Pitch Shifting  

you can see the code under pitch shifting section for better undderstanding.

#### Flanging effect:
Flanging effect is kind of delay. But the delay amount changes over a period. the priodic signal can be sinusiod or triagle function, let call that **M[n]**, then Flanging effect derived by this equation:

> M[n] = D/2 * (1 - cos(2 * &pi; * F_flange * n))  
> X_Flanging[n] = X[n] + g * X[M[n]]

#### reverbation:
When a sound plays in a room, there are many direct or indirect passible way, that hearer can recieve the sound. direct way is the original sound that comes through the air right into hearer ears. But, sound propagates omnidirectional, so in some direction it goes to the walls and reflected into hearer. The reflected sound spend longgest way than direct sound, so this is hears some amounts of time after the direct one. If we call sound source as "S" and hearer as "h", then following graph show some ways that hearer can hear a sound.

 \-----------------------  
 \|          /\         |  
 \|         /  \        |  
 \|         h---S       |  
 \|          \  /       |  
 \|           \/        |  
 \-----------------------

Remeber, due to sound propagation speed, the delay may be under 0.3 miliseconds, and attenuation of reflection is considerable, so we can't experience this in usual room we have, but in bathrooms we can try!
In commercial softwares or even hardwares, there are many implementation of reverb effect by many parameters, such as size of room, number of walls and etc. Here is use a very simple allpass transfer function to filter sound signal by reverb filter (generaly to search over internet try reverb convolution) like this:

                        -D  
              -a  +    z  
 Rev-F[z] = \----------------  
                        -D  
               1  -  a z  

#### Repeat:
very simple, I just add delayed signal to original signal. this delay amount is fixed over time. 

#### Filter:
 > TODO

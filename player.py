#!/usr/bin/python


import argparse
import numpy as np
import cv2
import pyaudio
from scipy.io import wavfile

parser = argparse.ArgumentParser(description='Wav Player by spectrogram')
parser.add_argument('Name', metavar='Name', type=str, nargs='+', help='input file name by wav extension')

args = parser.parse_args()
print(args.Name[0])
FILE_NAME = args.Name[0]

def makeI(c):
         I = np.zeros((200, 500, 3), np.uint8)
         b = I.shape[0]//100
         a = I.shape[1]//c.shape[0]
         for i in range(c.shape[0]):
                 v = np.floor(c[i]*100).astype(np.int)
                 j = v
                 #for j in range(v):
                 if v < 33:
                     I[0:(j+1)*b, i*a:(i+1)*a, :] = (100, 255, 10)
                 elif v < 66:
                     I[0:(j+1)*b, i*a:(i+1)*a, :] = (255, 100, 10)
                 else:
                     I[0:(j+1)*b, i*a:(i+1)*a, :] = (10, 100, 255)
         I = np.flipud(I)
         return I



def nothing(x):
    pass


def return_time(i, fs, s=1000):
     t = i*s  /fs
     h = int(t // 3600)
     if h > 0:
         m = int((t - h*3600)//60)
         text = str(h) + ':' + str(m) + ':' + str((t - h*3600 - m*60))
     else:
         m = int(t // 60)
         text = str(m) + ':' + str((t - m*60))[0:5]
     return text


fs , w = wavfile.read(FILE_NAME)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=2, rate=fs, frames_per_buffer=100, output=True)



cv2.namedWindow(FILE_NAME)
cv2.createTrackbar('', FILE_NAME, 0, w.shape[0]//1000, nothing)
i = 0
M = w.max() *1000**0.5
#for i in range(int(w.shape[0]/1000)+1):
while i < w.shape[0]/1000:
     b = w[1000*i:1000*(i+1), :]
     stream.write(b.tostring())
     b = b.sum(1)/2
     c = np.abs(np.fft.fft(b[0:-1:10]/1))
     mc = c.max()
     M = mc if M < mc else M
     c = c / M
     m = c.shape[0]
     i = cv2.getTrackbarPos('', FILE_NAME)
     i+=1
     cv2.setTrackbarPos('', FILE_NAME, i)
     #time.sleep(0.001)
     if i % 4 == 0:
         I = makeI(c[0:m//2]).astype(np.uint8)
         cv2.putText(I, return_time(i, fs), (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2, cv2.LINE_AA)
         cv2.imshow(FILE_NAME, I)
         cv2.waitKey(1)
cv2.destroyAllWindows()


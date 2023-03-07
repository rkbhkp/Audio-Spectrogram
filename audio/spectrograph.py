#!/usr/bin/env python
# -*- charset utf8 -*-

import pyaudio
import numpy
import math
import matplotlib.pyplot as plt
import matplotlib.animation
import time

RATE = 44100
BUFFER = 882
p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paFloat32,
    channels = 1,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = BUFFER
)

SECONDS = 2
t_end = time.time() + SECONDS
fig = plt.figure()
line1 = plt.plot([],[])[0]
line2 = plt.plot([],[])[0]

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

def init_line():
        line1.set_data(r, [-1000]*l)
        line2.set_data(r, [-1000]*l)
        return (line1,line2,)

def update_line():
    try:
        data = numpy.fft.rfft(numpy.fromstring(
            stream.read(BUFFER), dtype=numpy.float32)
        )
    except IOError:
        pass
    data = numpy.log10(numpy.sqrt(
        numpy.real(data)**2+numpy.imag(data)**2) / BUFFER) * 10
    data_point = data
    #line1.set_data(r, data)
    #line2.set_data(numpy.maximum(line1.get_data(), line2.get_data()))
    return data
    #return (line1,line2,)



'''
plt.xlim(0, RATE/2+1)
plt.ylim(-60, 0)
plt.xlabel('Frequency')
plt.ylabel('dB')
plt.title('Spectrometer')
plt.grid()
'''
#line_ani = matplotlib.animation.FuncAnimation(
#    fig, update_line, init_func=init_line, interval=0, blit=True
#)
all_data = []
while time.time() < t_end:
    data = update_line()
    if len(all_data) == 0:
        all_data = data
    else: 
        all_data = numpy.append(all_data, data)
#plt.show(all_data)
null_values = numpy.where(numpy.isinf(all_data))[0]
print(len(null_values))
for point in null_values:
    if point == 0:
        all_data[point] = all_data[point + 1]
    all_data[point] = all_data[point - 1]
plt.subplot(212)
powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(all_data, Fs=800, cmap="rainbow")
print(frequenciesFound)
plt.title('Spectrogram while snapping Fingers')
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.show()


#plt.show()

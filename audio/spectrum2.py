import numpy as np
from scipy import signal
from scipy.fft import fftshift
from matplotlib import mlab
import matplotlib.pyplot as plt
import pyaudio
import wave
import sys
import random
import datetime
import schedule
import time
import multiprocessing
import gzip
import pickle
import requests
import json
import serial
fs = 44100#10e3
N = 1e5
NFFT = 1024
amp = 2 * np.sqrt(2)
noise_power = 0.01 * fs / 2
time_u = np.arange(N) / float(fs)
mod = 500*np.cos(2*np.pi*0.25*time_u)
carrier = amp * np.sin(2*np.pi*3e3*time_u + mod)
noise = np.random.normal(scale=np.sqrt(noise_power), size=time_u.shape)
noise *= np.exp(-time_u/5)
x = carrier + noise

class spectrogram():
    def __init__(self,**kwargs):
        self.settings={"name":"audio"}
        self.settings.update(kwargs)
        self.data=[]
    def read(self):
        raw={}
        self.data.append(raw)
        print(raw)
    def report(self):
        now=datetime.datetime.now()
        time_ustamp=now.strftime("{}-%d%b%%Y-%H:%M:%S:%f".format(self.settings["name"]))
        self.settings["manager"].data.put({time_ustamp:self.data})
        self.data=[]
        return



class audioManager():
    def __init__(self, **kwargs):
        self.settings = {"filename":"audio-%d%b%%y-%H:%M:%S:%f.gz"}
        self.settings.update(kwargs)
        self.data=multiprocessing.Queue()
    def export(self):
        results={}
        for _ in range(self.data.qsize()):  # only pull as many items as exist right now. new stuff that comes in while this is running will wait for next time_u
            results.update(self.data.get())
        now = datetime.datetime.now()
        print(results)
        #f = gzip.open(now.strftime(self.settings["filename"]), 'wb')
        #pickle.dump(results,f)
        #f.close



def specgram2d(y, srate=44100, ax=None, title=None):
    if ax:
        ax = plt.axes()
        ax.set_title(title, loc='center', wrap=True)
        spec, freqs, t, im = ax.specgram(y, Fs=fs, scale='dB', vmax=0)
        ax.set_xlabel('time_u (s)')
        ax.set_ylabel('frequencies (Hz)')
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Amplitude (dB)')
        cbar.minorticks_on()
        return spec, freqs, t, im
    else:
        print("not ax")

def specgram3d(y, srate=44100, ax=None, title=None):
    if ax:
        ax = plt.axes(projection='3d')
        ax.set_title(title, loc='center', wrap=True)
        spec, freqs, t = mlab.specgram(y, Fs=srate)
        X, Y, Z = t[None, :], freqs[:, None],  20.0 * np.log10(spec)
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_ylabel('frequencies (Hz)')
        ax.set_ylabel('frequencies (Hz)')
        ax.set_zlabel('amplitude (dB)')
        ax.set_zlim(-140, 0)
        return X, Y, 
    else:
        print("not ax")

def generate_audio(seconds: int = 5, CHUNKSIZE: int = 1024, RATE=44100):
    # initialize portaudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=CHUNKSIZE)
    # do this as long as you want fresh samples
    numpydata = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    """for i in range(0, int(fs / CHUNKSIZE * seconds)):
        data = stream.read(CHUNKSIZE)
        numpydata.append(data)"""
    frames = [] # A python-list of chunks(numpy.ndarray)
    for _ in range(0, int(RATE / CHUNKSIZE * seconds)):
        data = stream.read(CHUNKSIZE)
        frames.append(np.frombuffer(data, dtype=np.int16))
    numpydata = np.hstack(frames)
    print(type(numpydata))
    # close stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open("out.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(numpydata))
    wf.close()
    return numpydata
"""plt.figure(figsize=(10,12))
plt.plot(x)
plt.show()

f, t, Sxx = signal.spectrogram(x, fs)
plt.figure(figsize=(8,10))
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('time_u [sec]')
plt.show()
"""
"""fig, (ax1, ax2) = plt.subplots(nrows=2)
ax1.plot(time_u, x)
Pxx, freqs, bins, im = ax2.specgram(x, NFFT=NFFT,Fs=fs, noverlap=900)
plt.show()"""
if __name__=="__main__":
    name="data"
    duration=10
    audio_queue = audioManager()
    audio_queue.settings["filename"]="{:}-%d%b%%Y-%H:%M:%S:%f.gz".format(name)
    sensors={"spectrogram":spectrogram(manager=audio_queue)}
    schedule.every(duration).seconds.do(audio_queue.export)
    schedule.every(1.).seconds.do(sensors["spectrogram"].read)
    schedule.every(5.).seconds.do(sensors["spectrogram"].report)
    for i in range(duration*1000):
        schedule.run_pending()
        time.sleep(0.001)
    """x = generate_audio()
    fig1, ax1 = plt.subplots()
    specgram2d(x, srate=fs, ax=ax1)
    plt.show()
    fig2, ax2 = plt.subplots(subplot_kw={'projection': '3d'})
    specgram3d(x, srate=fs, ax=ax2)
    plt.show()"""

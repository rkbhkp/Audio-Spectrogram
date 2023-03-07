import pyaudio
import wave
import sys
import argparse

def main(chunk=1024, sample_format=pyaudio.paInt16, channels=2, fs=44100, seconds=5,filename="output.wav"):
    # chunk: Record in chunks of 1024 samples
    # sample_format: 16 bits per sample
    # fs: Record at 44100 samples per second
    # seconds: how long to record
    # filename: default file save name

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
if __name__=='__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", type=str, default="output.wav", required=False, help="filename for .wav file. Must include .wav")
    ap.add_argument("-t", "--time", type=int, default=5, required=False, help="How long the recording should be in seconds, defaults to 5 seconds")
    args = vars(ap.parse_args())
    main(filename=args["filename"], seconds=args["time"])
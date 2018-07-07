
import pyaudio
import struct
import numpy as np

CHUNK = 1024
#CHUNK = 512
CHUNK = 10
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH), channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

print("* running...")

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    buff = stream.read(CHUNK, exception_on_overflow=False)
    freq_as_list = np.frombuffer(buff, dtype='B')
    cancellation_freq = map(lambda x: x * -1, freq_as_list)
    cancellation_buff = np.fromiter(cancellation_freq, dtype=np.int).tobytes()
    stream.write(cancellation_buff)

print("* done")

stream.stop_stream()
stream.close()

p.terminate()


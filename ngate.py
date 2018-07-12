
import pyaudio
import numpy as np
from functools import reduce 

CHUNK = 1024
WIDTH = 2 
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
THRESHOLD = 60 

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH), channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

print("* recording")

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #data = stream.read(CHUNK)
    #stream.write(data, CHUNK)

    buff = stream.read(CHUNK, exception_on_overflow=False)
    freqs = np.frombuffer(buff, dtype='B')
    freqs_total = freqs.size
    freqs_sum = reduce(lambda x, y : x + y, freqs)
    freqs_avg = (freqs_sum / freqs_total) * 1000
    print("Average Freq => " + str(freqs_avg))
    if freqs_avg > THRESHOLD:
        stream.write(buff, CHUNK)
    else:
        print('Muted!')

print("* done")

stream.stop_stream()
stream.close()

p.terminate()


import numpy as np

data = [1,2,3,4]

sampling_length = 50
f_s = #sampling frequency in hz

 = 1.0/sampling_length  
n = len(data)

freq = np.fft.fftfreq(n, d = sampling_length)



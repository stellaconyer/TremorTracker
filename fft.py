import numpy as np

f_s = 20.0 # hz

for x in x_fft_array:
	if len(x) == 20:
		fft_x = np.fft.fft(x)
		n = len(fft_x)
		freq = np.fft.fftfreq(n, 1/f_s)

		#Calculate absolute value of fft_x
		fft_x_abs = np.abs(fft_x)

		#Take first half of FFT array UNSCALED?
		half_n = np.ceil(n/2.0)
		freq_half = freq[:half_n]
		fft_x_half = fft_x_abs[:half_n]

		# Square magnitude of FFT to find PSD
		PSD_x = np.power(fft_x_half, 2)


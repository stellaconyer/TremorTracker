import numpy as np

def combined_fft(samples): 

	f_s = 20.0 # hz

	# list of all recorded samples from the session to be charted on heatmap
	all_recorded_samples = []

	for timestamp, sample in samples.iteritems():
		x = sample["x"]
		fft_x = np.fft.fft(x)
		n = len(fft_x)
		freq = np.fft.fftfreq(n, 1/f_s)
		# print "freq:", freq

		#Calculate absolute value of fft_x
		fft_x = np.abs(fft_x)

		#Take first half of FFT array  + 1 to access 10th element?
		half_n = np.ceil(n/2.0) + 1
		freq_half = freq[:half_n]
		fft_x_half = fft_x[:half_n]

		# Square magnitude of FFT to find PSD
		PSD_x_total = np.power(fft_x_half, 2)

		y = sample["y"]
		fft_y = np.fft.fft(y)
		n = len(fft_y)
		freq = np.fft.fftfreq(n, 1/f_s)
		# print "freq:", freq

		#Calculate absolute value of fft_y
		fft_y = np.abs(fft_y)

		#Take first half of FFT array  + 1 to access 10th element?
		half_n = np.ceil(n/2.0) + 1
		freq_half = freq[:half_n]
		fft_y_half = fft_y[:half_n]

		# Square magnitude of FFT to find PSD
		PSD_y_total = np.power(fft_y_half, 2)

		z = sample["z"]
		fft_z = np.fft.fft(z)
		n = len(fft_z)
		freq = np.fft.fftfreq(n, 1/f_s)

		#Calculate absolute value of fft_z
		fft_z = np.abs(fft_z)

		#Take first half of FFT array  + 1 to access 10th element?
		half_n = np.ceil(n/2.0) + 1
		freq_half = freq[:half_n] 
		fft_z_half = fft_z[:half_n]

		# Square magnitude of FFT to find PSD
		PSD_z_total = np.power(fft_z_half, 2)

		# Combine PSDs for x, y, and z axes
		PSD_total_1hz = PSD_x_total[1] + PSD_y_total[1] + PSD_z_total[1]
		PSD_total_3hz = PSD_x_total[3] + PSD_y_total[3] + PSD_z_total[3]
		PSD_total_6hz = PSD_x_total[6] + PSD_y_total[6] + PSD_z_total[6]
		PSD_total_10hz = PSD_x_total[10] + PSD_y_total[10] + PSD_z_total[10]

	#Create dictionary of timestamp and total PSDs for each one second interval
		PSD_one_sec_sample_dict = {}

		PSD_one_sec_sample_dict["timestamp"]= timestamp
		PSD_one_sec_sample_dict["data"] = [PSD_total_1hz, PSD_total_3hz, PSD_total_6hz, PSD_total_10hz]

		#Append dictionary to master list of samples for charting
		all_recorded_samples.append(PSD_one_sec_sample_dict)

	return all_recorded_samples
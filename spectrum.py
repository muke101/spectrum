#load in music file, take 1024 samples in array, average channels, calculate FFT, take magnitude, plot, repeat with next buffer with 100 sample overlap

#your graphs are fucky

from scipy.io.wavfile import read
import numpy as np 
import matplotlib.pyplot as plt 


class spectrum():
	def __init__(self): #TODO: see if you can replace the scipy wav read function
		self.sampleRate, self.audio = read("/mnt/New_Volume/music/Aphex Twin/SAW1/01 Xtal.wav")
		print(self.sampleRate)
		self.frame = 0
		self.bufferSize = 1024 
		self.overlap = 0
		print(len(self.audio))
		self.audio = np.mean(self.audio, axis=1)[40000:] #average channels
		self.audioBuffer = np.zeros(1024, dtype=float)
		self.FFT()
		self.plotting()

	def fillBuffer(self): #TODO: window audio, convert power to dB
		self.audioBuffer = np.zeros(1024, dtype=float) #flush out buffer
		frameSize = (self.frame*self.bufferSize)-self.overlap #keep track of how  many frames in each iteration
		for c, i in enumerate(range(frameSize, frameSize+self.bufferSize)):
			try:
				self.audioBuffer[c] = self.audio[i]
			except IndexError:
				return 1
		self.overlap = 100 #first frame isn't incorrectly cut back by 100 bytes (feels hacky lol)
		self.frame+=1
		return 0

	def FFT(self):
		power = np.abs(np.fft.fft(self.audioBuffer)) #abs calculates the complex magnitude, for some reason
		freqs = np.fft.fftfreq(self.bufferSize, 1/self.sampleRate)
		freqs = freqs[:int(len(freqs)/2)] #remove symetric negative frequencies
		power = power[:int(len(power)/2)]
		return freqs, power

	def plotting(self):
		while self.fillBuffer() != 1:
			freqs, power = self.FFT()
			plt.plot(freqs,power)
			plt.show()


spectrum()

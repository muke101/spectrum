#load in music file, take 1024 samples in array, average channels, calculate FFT, take magnitude, plot, repeat with next buffer with 100 sample overlap

from scipy.io.wavfile import read
import numpy as np 
import matplotlib.pyplot as plt 

class spectrum():
	def __init__(self):
		self.samples, self.audio = read("/mnt/New_Volume/music/Aphex Twin/SAW1/01 Xtal.wav")
		self.frame = 0
		self.bufferSize = 1024
		self.overlap = 0
		self.audio = np.mean(self.audio, axis=1) #average channels
		self.audioBuffer = np.zeros(1024, dtype=float)
		self.plotting()

	def fillBuffer(self): #TODO: window audio
		self.audioBuffer = np.zeros(1024, dtype=float) #flush out buffer
		frameSize = (self.frame*self.bufferSize)-self.overlap #keep track of how  many frames in each iteration
		for c, i in enumerate(range(frameSize, frameSize+self.bufferSize)):
			try:
				print(i,c)
				self.audioBuffer[c] = self.audio[i]
			except IndexError:
				return 1
		self.overlap = 100 #feels hacky lol
		self.frame+=1
		return 0

	def FFT(self):
		power = np.abs(np.fft.fft(self.audioBuffer)) #abs calculates the complex magnitude, for some reason
		freqs = np.fft.fftfreq(self.bufferSize, 1/self.samples)
		return freqs, power

	def plotting(self):
		while self.fillBuffer() != 1:
			freqs, power = self.FFT()
			plt.plot(freqs,power)
			plt.show()


spectrum()

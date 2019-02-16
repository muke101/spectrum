#load in music file, take 1024 samples in array, average channels, calculate FFT, take magnitude, plot, repeat with next buffer with 100 sample overlap

from scipy.io.wavfile import read
import numpy as np 
import matplotlib.pyplot as plt 

class spectrum():
	def __init__(self):
		self.samples, self.audio = read("test.wav")
		self.frame = 1
		self.bufferSize = 1024
		self.overlap = 0
		self.audioBuffer = np.zeros(1024, dtype=float)
		self.plotting()

	def fillBuffer(self): #TODO: window audio
		self.audioBuffer = np.zeros(1024, dtype=float) #flush out buffer
		frameSize = (self.frame*self.bufferSize)-self.overlap #keep track of how  many frames in each iteration
		for i in range(frameSize, frameSize+bufferSize+1):
			self.audioBuffer.append(self.audio[i])
			if self.audio[i] == self.audio[-1]: #if at end of file before buffer fills
				return 1
		self.overlap = 100 #feels hacky lol
		self.frames+=1
		return 0

	def FFT(self):
		self.audioBuffer = np.mean(self.audioBuffer, axis=1) #average channels
		power = np.abs(np.ftt.ftt(self.audioBuffer)) #abs calculates the complex magnitude, for some reason
		freqs = np.ftt.fttfreq(self.bufferSize, 1/self.samples)
		return freqs, power

	def plotting(self):
		while self.fillBuffer() != 1:
			freqs, power = self.FFT()
			plt.plot(freqs,power)
			plt.show()




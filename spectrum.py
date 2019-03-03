#load in music file, take 1024 samples in array, average channels, calculate FFT, take magnitude, plot, repeat with next buffer with 100 sample overlap
from scipy.io.wavfile import read
import numpy as np 
import matplotlib.pyplot as plt
#TODO: manually implenent as many numpy algorithim functions in C as possible and import with ctypes

class spectrum():
	def __init__(self): #TODO: see if you can replace the scipy wav read function
		self.sampleRate, self.audio = read("/mnt/New_Volume/music/Aphex Twin/SAW1/01 Xtal.wav")
		print(self.sampleRate)
		self.slice = 0
		self.bufferSize = 1024 
		self.overlap = 0
		print(len(self.audio))
		self.audio = np.mean(self.audio, axis=1)[40000:] #average channels
		self.audioBuffer = np.zeros(1024, dtype=float)
		self.plotting()

	def fillBuffer(self):
		self.audioBuffer = np.zeros(1024, dtype=float) #flush out buffer
		sliceSize = (self.slice*self.bufferSize)-self.overlap #keep track of how  many frames in each iteration
		for c, i in enumerate(range(sliceSize, sliceSize+self.bufferSize)):
			try:
				self.audioBuffer[c] = self.audio[i]
			except IndexError: #towards end of audio data, last point probably won't fall on 1024 exactly. Need to break out of loop with whatever data is there
				return 1
		self.overlap = 100 #first slice isn't incorrectly cut back by 100 bytes (feels hacky lol)
		self.slice+=1
		return 0

	def FFT(self):
		win = np.kaiser(self.bufferSize, 7) #windowing function
		power = np.abs(np.fft.fft(self.audioBuffer * win)) #abs calculates the complex magnitude, for some reason
		freqs = np.fft.fftfreq(self.bufferSize, 1/self.sampleRate)
		freqs = freqs[:int(len(freqs)/2)] #slice out symetric negative frequencies
		power = power[:int(len(power)/2)] #slice out corrosponding powers
		if power.max() != 0:
			power = 20*np.log10(power/power.max()) #convert to dB
		return freqs, power

	def plotting(self):
		while self.fillBuffer() != 1:
			freqs, power = self.FFT()
			plt.plot(freqs,power)
			plt.show()
		freqs, power = self.FFT() #wish Python had a do-while loop lol
		plt.plot(freqs,power)
		plt.show()
import os

import pyaudio
import wave
import contextlib

import random
import threading
from time import time, sleep

class ImaginaryLandscape:
	def __init__(self):
		self.startTime = time() #time will be used to make descisons at various points in the program
		self.done = False #determines if program will stop after x-minutes

		self.makeThreads()
		self.readInAudioFiles()
		self.perform()

	#creates an array of threads that will be use to play the sound files
	def makeThreads(self):
		self.threads = []
		for each in range (0,3):
			self.threads.append(threading.Thread())

	#place all the audio files in an array to be used later
	def readInAudioFiles(self):
		self.audioFiles = []
		count = 0
		for entry in os.scandir(): 
			if(".wav" in entry.name):
   				self.audioFiles.append(Music(entry))
   				print(self.audioFiles[count].getName())
   				#print(os.path.realpath(self.audioFiles[count]))
   				count = count + 1

	def decideIfThreadShouldBeStarted(self, threadNumber):
		if threadNumber == 0 and random.randrange(0, 2, 1) == 0 or threadNumber == 1 and random.randrange(0, 4, 1) == 0 or threadNumber == 2 and random.randrange(0, 9, 1) == 0:
			self.startThread(threadNumber)

	def startThread(self, threadNumber):
		self.threads[threadNumber] = threading.Thread(target=self.play, 
			args = (self.audioFiles[random.randrange(0, len(self.audioFiles) - 1, 1)].name,))
		self.threads[threadNumber].start() 

	def play(self, music):
		chunk = 1024
		openFile = wave.open(music.getName(), "rb")
		p = pyaudio.PyAudio()
		stream = p.open(format = p.get_format_from_width(openFile.getsampwidth()),
					input_device_index = 4,  
               		channels = openFile.getnchannels(),  
                	rate = openFile.getframerate(),  
                	output = True)  
		data = openFile.readframes(chunk)

		#skip unwanted frames
		n_frames = int(music.getStart() * openFile.getframerate())
		openFile.setpos(n_frames)

		# write desired frames to audio buffer
		n_frames = int(music.getEnd * openFile.getframerate())
		frames = openFile.readframes(n_frames)
		stream.write(frames)

		stream.close()
		p.terminate()
		f.close()

	def perform(self):
		i = 0
		while not self.done:
			print("begin") 
			i += 1
			if i == 10:
				self.done = True

			if ((self.threads[0].is_alive() is False) and (random.randrange(0, 2, 1) == 0)):
				print("here0")
				self.threads[0] = threading.Thread(target=self.play, 
					args = (self.audioFiles[random.randrange(0, len(self.audioFiles) - 1, 1)].name,))
				self.threads[0].start() 
			if ((self.threads[1].is_alive() is False) and (random.randrange(0, 4, 1) == 0)):
				print("here1")
				self.threads[1] = threading.Thread(target=self.play, 
					args = (self.audioFiles[random.randrange(0, len(self.audioFiles) - 1, 1)].name,))
				self.threads[1].start() 
			if ((self.threads[2].is_alive() is False) and (random.randrange(0, 9, 1) == 0)):
				print("here2")
				self.threads[2] = threading.Thread(target=self.play, 
					args = (self.audioFiles[random.randrange(0, len(self.audioFiles) - 1, 1)].name,))
				self.threads[2].start()

			sleep(1)

class Music:
	def __init__(self, file):
		self.sourceFile = file
		self.name = file.name
		self.openFile = wave.open(self.name, "rb")

		self.length = self.getLength()

		self.openFile.close()

	#find and return length of audio file in seconds
	def getLength(self):
		return ((self.openFile.getnframes()) / (float(self.openFile.getframerate())))

	#randomly choose where audio file will start 
	def getStart(self):
		return (random.randrange(0, int(self.length), 1))

	#randomly choose how long audio while will play
	def getEnd(self):
		return random.randrange(0, 60, 1)

	def getName(self):
		return self.name

il = ImaginaryLandscape()
print("done")
import pyaudio
import wave
import os
import random
import threading
import contextlib
from time import time, sleep

class ImaginaryLandscape:
	def __init__(self, numberOfTracks, divisionConstant):
		self.startTime = time() #time will be used to make descisons at various points in the program
		self.done = False #determines if program will stop after x-minutes

		self.makeThreads(numberOfTracks, divisionConstant)
		self.readInAudioFiles()
		#self.perform()

	#creates an array of threads that will be use to play the sound files
	def makeThreads(self, numberOfTracks, divisionConstant):
		threadProbability = 100 / divisionConstant #threadProbability for first thread (see note below at divisionConstant decleration)
		self.threads = [] #array of threadObjects that will be used
		for each in range(0, numberOfTracks): #making one Thread object for each possible numberOfTracks that will play at one time
			self.threads.append(Thread((threading.Thread()), (threadProbability)))
			#First parameter for Thread() - a new thread
			#Second parameter - the probability that the thread will play when it is checked, calculated on the next line
			threadProbability = (self.threads[each].getProbability() / 2) #to be used for the next thread to be created
		return

	#place all the audio files in an array to be used later
	def readInAudioFiles(self):
		self.audioFiles = []
		count = 0
		for entry in os.scandir(): 
			if(".wav" in entry.name):
   				self.audioFiles.append(entry)
   				print(self.audioFiles[count].name)
   				#print(os.path.realpath(self.audioFiles[count]))
   				count = count + 1

	def decideIfThreadShouldBeStarted(self, threadNumber):
		if threadNumber == 0 and random.randrange(0, 2, 1) == 0 or threadNumber == 1 and random.randrange(0, 4, 1) == 0 or threadNumber == 2 and random.randrange(0, 9, 1) == 0:
			self.startThread(threadNumber)

	def play(self, fileName):
		chunk = 1024
		f = wave.open(fileName, "rb")
		p = pyaudio.PyAudio()
		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
					input_device_index = 4,  
               		channels = f.getnchannels(),  
                	rate = f.getframerate(),  
                	output = True)  
		data = f.readframes(chunk)

		#find length of audio file in seconds
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate)
		print(duration)

		start = random.randrange(0, int(duration), 1)
		length = random.randrange(0, 60, 1)

		#skip unwanted frames
		n_frames = int(start * f.getframerate())
		f.setpos(n_frames)

		# write desired frames to audio buffer
		n_frames = int(length * f.getframerate())
		frames = f.readframes(n_frames)
		stream.write(frames)

		stream.close()
		p.terminate()
		f.close()

	def perform(self):
		i = 0
		while not self.done:
			print("begin") 
			i += 1
			if i == 180:
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

#The class "Thread" is used to hold not only the threads, as well as the probability that they will play that is associated with them
class Thread:
	def __init__(self, thread, probability):
		self.thread = thread
		self.probability = int(probability)
		print(self.probability)

	def getThread(self):
		return self.thread

	def getProbability(self):
		return self.probability

numberOfTracks = 3 #maximum number of tracks that can be playing at one time
divisionConstant = 2 #constant by which each threads range of probability will be determined
#put in README:
#Ex: with 2, we start with 100, then divide it by 2, and get 50
#for the next thread, we take that 50, and divide it by 2, and get 25
#for the next thread, we take that 25, and divide it by 2, and get 12 (through integer division)
#etc...
il = ImaginaryLandscape(numberOfTracks, divisionConstant)
print("done")
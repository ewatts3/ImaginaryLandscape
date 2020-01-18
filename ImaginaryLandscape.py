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
		self.perform()

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

   	#determines if each thread will start are not
   	#recusively calls subsequent threads
   	#returns if thread does not start
	def decideIfThreadShouldBeStarted(self, index):
		#if the current index of threads it is checking is NOT playing, it will then choose a number to decide if it will start or not
		#ex: if probabiilty is 50, the second statement will return "true" if a number between 0 and 49 is picked (a 50% chance)
		#there are two "if" statements to account for the case where the thread is being checked is NOT playing and DOES NOT start
		if ((self.threads[index].getThread().is_alive() is False) 
			and (random.randrange(0, 100, 1) < self.threads[index].getProbability())):
			#start thread
			self.threads[index].setThread(
				threading.Thread(target=self.play, 
				args = (self.audioFiles[random.randrange(0, len(self.audioFiles) - 1, 1)].name,))
				)
			self.threads[index].getThread().start()
			print('start' + str(index))
			#begins to check next thread if current thread is not the last one
			index += 1
			if(index < len(self.threads)):
				self.decideIfThreadShouldBeStarted(index)
		elif (self.threads[index].getThread().is_alive() is True):
			index += 1
			if(index < len(self.threads)):
				self.decideIfThreadShouldBeStarted(index)
		return

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
		#print(duration)

		start = random.randrange(0, int(duration), 1)
		length = random.randrange(0, 15, 1)

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
		print("end")
		return

	def perform(self):
		while not self.done:
			print("begin")

			self.decideIfThreadShouldBeStarted(0)

			if (time() - self.startTime > 60):
				self.done = True

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

	def setThread(self, threadStart):
		self.thread = threadStart

numberOfTracks = 3 #maximum number of tracks that can be playing at one time
divisionConstant = 2 #constant by which each threads range of probability will be determined
#put in README:
#Ex: with 2, we start with 100, then divide it by 2, and get 50
#for the next thread, we take that 50, and divide it by 2, and get 25
#for the next thread, we take that 25, and divide it by 2, and get 12 (through integer division)
#etc...
il = ImaginaryLandscape(numberOfTracks, divisionConstant)
print("done")
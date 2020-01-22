import pyaudio
import wave
import os
import random
import threading
from time import time, sleep
from datetime import datetime

class ImaginaryLandscape:
	def __init__(self, parameters):
		self.parameters = parameters #parameters set by the user
		self.startTime = time() #time will be used to make descisons at various points in the program
		self.done = False #determines if program will stop after x-minutes

		self.makeThreads(self.parameters.getNumberOfTracks(), self.parameters.getDivisionConstant())
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
			and (random.randrange(0, 100, 1) < self.threads[index].getProbability()) ):
			#start thread
			self.threads[index].setThread(
				threading.Thread(target=self.play, 
				args = (self.selectRandomAudioFile(),))
				)
			self.threads[index].getThread().start()
			print('start' + str(index))
			#begins to check next thread, if current thread is not the last one
			index += 1
			if(index < len(self.threads)):
				self.sleep()
				self.decideIfThreadShouldBeStarted(index)
		elif (self.threads[index].getThread().is_alive() is True):
			index += 1
			if(index < len(self.threads)):
				self.sleep()
				self.decideIfThreadShouldBeStarted(index)
		return

	def selectRandomAudioFile(self):
		return self.audioFiles[random.randrange(0, len(self.audioFiles) - 1, 1)].name

	def sleep(self):
		sleep(random.randrange(
			self.parameters.getMinimumTimeBetweenChecks(),
			self.parameters.getMaximumTimeBetweenChecks(), 
			1)) 
		return

	def play(self, fileName):
		try:
			chunk = 1024
			f = wave.open(fileName, "rb")
			p = pyaudio.PyAudio()
			stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
						input_device_index = 4,  
	               		channels = f.getnchannels(),  
	                	rate = f.getframerate(),  
	                	output = True)  
			#data = f.readframes(chunk) 	does this do anything????

			#find length of audio file in seconds
			frames = f.getnframes()
			rate = f.getframerate()
			duration = int(frames / float(rate))
			#print(duration)

			start = random.randrange(0, duration, 1)
			length = random.randrange(self.parameters.getMinimumLengthOfSample(), 
				self.parameters.getMaximumLengthOfSample(), 1)

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
			print("endTrack")
			return
		#I've been having an issue with sometimegetting an error 
		#"OSError: [Errno -9996] Invalid output device (no default output device)"
		#at line 75, so I've input this try/except so the program can continue
		except:
			print("Errno -9996")
			return

	def perform(self):
		while not self.done:
			print("beginLoop")

			self.decideIfThreadShouldBeStarted(0)

			if (time() - self.startTime > self.parameters.getMinimumLengthOfPiece()):
				if(time() - self.startTime > self.parameters.getMaximunLengthOfPiece()):
					#kill all threads
					self.done = True
					return
				elif(random.randrange(0, 10, 1) == 0):
					self.done = True
					return

			self.sleep()

#class of parameters set by the user
class Parameters:
	def __init__ (self, numberOfTracks, divisionConstant, 
		minimumTimeBetweenChecks, maximumTimeBetweenChecks,
		minimunLengthOfPiece, maximumLengthOfPiece,
		minimumLengthOfSample, maximumLengthOfSample):
		self.numberOfTracks = numberOfTracks
		self.divisionConstant = divisionConstant
		self.minimumTimeBetweenChecks = minimumTimeBetweenChecks
		self.maximumTimeBetweenChecks = maximumTimeBetweenChecks
		self.minimunLengthOfPiece = minimunLengthOfPiece
		self.maximumLengthOfPiece = maximumLengthOfPiece
		self.minimumLengthOfSample = minimumLengthOfSample
		self.maximumLengthOfSample = maximumLengthOfSample

	def getNumberOfTracks(self):
		return self.numberOfTracks

	def getDivisionConstant(self):
		return self.divisionConstant

	def getMinimumTimeBetweenChecks(self):
		return self.minimumTimeBetweenChecks

	def getMaximumTimeBetweenChecks(self):
		return self.maximumTimeBetweenChecks

	def getMinimumLengthOfPiece(self):
		return self.minimunLengthOfPiece

	def getMaximunLengthOfPiece(self):
		return self.maximumLengthOfPiece

	def getMinimumLengthOfSample(self):
		return self.minimumLengthOfSample

	def getMaximumLengthOfSample(self):
		return self.maximumLengthOfSample

#The class "Thread" is used to hold not only the threads, but the probability that they will play that is associated with them as well
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

#maximum number of tracks that can be playing at one time
numberOfTracks = 3

#constant by which each threads range of probability will be determined
divisionConstant = 2
#put in README:
#Ex: with 2, we start with 100, then divide it by 2, and get 50
#for the next thread, we take that 50, and divide it by 2, and get 25
#for the next thread, we take that 25, and divide it by 2, and get 12 (through integer division)
#etc...

#time between each check for if the program should play a thread or not
minimumTimeBetweenChecks = 1
maximumTimeBetweenChecks = 5
#length of the the whole performance
minimunLengthOfPiece = 60 * (1)
maximumLengthOfPiece = 60 * (1)
#range of length for each individual sample
minimumLengthOfSample = 0
maximumLengthOfSample = 15

parameters = Parameters(
	numberOfTracks, 
	divisionConstant, 
	minimumTimeBetweenChecks,
	maximumTimeBetweenChecks,
	minimunLengthOfPiece, 
	maximumLengthOfPiece,
	minimumLengthOfSample,
	maximumLengthOfSample)

il = ImaginaryLandscape(parameters)
print("done")
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
		self.m = Music() #public class to do operations relating to playing samples

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
   				count = count + 1

   	def perform(self):
		while not self.done:
			print("beginLoop")

			self.decideIfThreadShouldBeStarted(0)
			self.sleep()
			self.done = self.decideIfPieceShouldEnd()
		return

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
				threading.Thread(target=self.m.play, 
				args = (self.selectRandomAudioFile(),
					self.parameters.getMinimumLengthOfSample(),
					self.parameters.getMaximumLengthOfSample(),))
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
		return self.audioFiles[random.randrange(0, len(self.audioFiles) - 1, 1)]

	def sleep(self):
		sleep(random.randrange(
			self.parameters.getMinimumTimeBetweenChecks(),
			self.parameters.getMaximumTimeBetweenChecks(), 
			1)) 
		return

	def decideIfPieceShouldEnd(self):
		if (time() - self.startTime > self.parameters.getMinimumLengthOfPiece()):
			if(time() - self.startTime > self.parameters.getMaximunLengthOfPiece()):
				#implement kill all threads
				self.done = True
				return True
			elif(random.randrange(0, 10, 1) == 0):
				self.done = True
				return True

		return False

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

	def setNumberOfTracks(self, input):
		self.numberOfTracks = input
		return

	def getNumberOfTracks(self):
		return self.numberOfTracks

	def setDivisionConstant(self, input):
		self.divisionConstant = input
		return

	def getDivisionConstant(self):
		return self.divisionConstant

	def setMinimumTimeBetweenChecks(self, input):
		self.minimumTimeBetweenChecks = input
		return

	def getMinimumTimeBetweenChecks(self):
		return self.minimumTimeBetweenChecks

	def setMaximumTimeBetweenChecks(self, input):
		self.maximumTimeBetweenChecks = input
		return

	def getMaximumTimeBetweenChecks(self):
		return self.maximumTimeBetweenChecks

	def setMinimumLengthOfPiece(self, input):
		self.minimunLengthOfPiece = input
		return

	def getMinimumLengthOfPiece(self):
		return self.minimunLengthOfPiece

	def setMaximumLengthOfPiece(self, input):
		self.maximumLengthOfPiece = input
		return

	def getMaximunLengthOfPiece(self):
		return self.maximumLengthOfPiece

	def setMinimumLengthOfSample(self, input):
		self.minimumLengthOfSample = input
		return

	def getMinimumLengthOfSample(self):
		return self.minimumLengthOfSample

	def getMaximumLengthOfSample(self, input):
		self.maximumLengthOfSample = input
		return

	def getMaximumLengthOfSample(self):
		return self.maximumLengthOfSample

#The class "Thread" is used to hold not only the threads, but the probability that they will play that is associated with them as well
class Thread:
	def __init__(self, thread, probability):
		self.thread = thread
		self.probability = int(probability)
		#print(self.probability)

	def getThread(self):
		return self.thread

	def getProbability(self):
		return self.probability

	def setThread(self, threadStart):
		self.thread = threadStart

#public class to do all the operations relating to playing the file
class Music:
	#performs all necessary operations to play a file
	def play(self, musicFile, min, max):
		file = wave.open(musicFile.name, "rb")
		p = pyaudio.PyAudio()
		stream = self.openStream(p, file)

		durationOfTrack = self.getDuration(file)
		start = self.decideStart(durationOfTrack)
		length = self.decideLength(min, max)
		file.setpos(self.setPosition(start, file))
		stream.write(self.getFramesToWrite(length, file))

		stream.close()
		p.terminate()
		file.close()
		print("endTrack")
		return

	#open audio output stream
	def openStream(self, pyaudio, file):
		return pyaudio.open(format = pyaudio.get_format_from_width(file.getsampwidth()),
					input_device_index = 4,  
	               	channels = file.getnchannels(),  
	                rate = file.getframerate(),  
	                output = True)  

	#find length of audio file in seconds
	def getDuration(self, file):
		return int(file.getnframes() / float(file.getframerate()))

	#decide starting position of sample
	def decideStart(self, duration):
		return random.randrange(0, duration, 1)

	#decide total length of sample
	def decideLength(self, min, max):
		return random.randrange(min, max, 1)

	#set position of open audio file to correct starting point
	def setPosition(self, start, file):
		return int(start * file.getframerate())

	#calculate which frames to write to the audio buffer
	def getFramesToWrite(self, length, file):
		return file.readframes(int(length * file.getframerate()))

#maximum number of tracks that can be playing at one time
numberOfTracks = 3

#constant by which each threads range of probability will be determined
divisionConstant = 2
#put in README:
#Ex: with 2, we start with 100, then divide it by 2, and get 50
#for the next thread, we take that 50, and divide it by 2, and get 25
#for the next thread, we take that 25, and divide it by 2, and get 12 (through integer division)
#etc...

#time in seconds between each check for if the program should play a thread or not
minimumTimeBetweenChecks = 1
maximumTimeBetweenChecks = 2
#length of the the whole performance in seconds
minimunLengthOfPiece = 60 * (1)
maximumLengthOfPiece = 60 * (1)
#range of length for each individual sample in seconds
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
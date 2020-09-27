from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
import decimal
import shutil
import pyaudio
from pydub import AudioSegment
import wave
import os
import random
import threading
from time import time, sleep

from ReadInAudioFiles import readInAudioFiles
from Thread import Thread
from Music import Music

class ImaginaryLandscape:
	def __init__(self, parameters):
		self.parameters = parameters #parameters set by the user

		self.readInAudioFiles()
		self.makeThreads(self.parameters.getNumberOfTracks(), self.parameters.getDivisionConstant())
		self.perform()
		print('done')

	#place all the audio files in an array to be used later
	def readInAudioFiles(self):
		riaf = readInAudioFiles()
		self.audioFiles = riaf.getArrayOfAudioFiles(self.parameters.getDirectoryForFiles(), self.parameters)
		return

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

	def perform(self):
		startTime = time() #time will be used to decide when the piece will end
		done = False #determines if program will stop
		m = Music() #public class to do operations relating to playing samples
		while not done:
			print("beginLoop")
			self.decideIfThreadShouldBeStarted(0, m)
   			#self.sleep()
			done = self.decideIfPieceShouldEnd(startTime)
		return

   	#determines if each thread will start are not
   	#recusively calls subsequent threads
   	#returns if thread does not start
	def decideIfThreadShouldBeStarted(self, index, m):
		#if the current index of threads it is checking is NOT playing, it will then choose a number to decide if it will start or not
		#ex: if probabiilty is 50, the second statement will return "true" if a number between 0 and 49 is picked (a 50% chance)
		#there are two "if" statements to account for the case where the thread is being checked is NOT playing and DOES NOT start
		if ((self.threads[index].getThread().is_alive() is False) 
			and (random.randrange(0, 100, 1) < self.threads[index].getProbability()) ):
			#start thread
			self.threads[index].setThread(
				threading.Thread(target=m.play, 
				args = (self.selectRandomAudioFile(),
					self.parameters.getMinimumLengthOfSample(),
					self.parameters.getMaximumLengthOfSample()))
				)
			self.threads[index].getThread().start()
			print('start' + str(index))
			#begins to check next thread, if current thread is not the last one
			index += 1
			if(index < len(self.threads)):
				self.sleep()
				self.decideIfThreadShouldBeStarted(index, m)
		elif (self.threads[index].getThread().is_alive() is True):
			index += 1
			if(index < len(self.threads)):
				self.sleep()
				self.decideIfThreadShouldBeStarted(index, m)
		if index == 0:
			self.sleep()
		return

	def selectRandomAudioFile(self):
		return self.audioFiles[random.randrange(0, len(self.audioFiles) - 1, 1)]

	def sleep(self):
		sleep(random.randrange(
			self.parameters.getMinimumTimeBetweenChecks(),
			self.parameters.getMaximumTimeBetweenChecks(), 
			1)) 
		return

	def decideIfPieceShouldEnd(self, startTime):
		if (time() - startTime > self.parameters.getMinimumLengthOfPiece()):
			if(time() - startTime > self.parameters.getMaximunLengthOfPiece()):
				#implement kill all threads
				return True
			elif(random.randrange(0, 10, 1) == 0):
				return True

		return False
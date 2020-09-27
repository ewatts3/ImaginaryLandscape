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

#reads in and converts audio files, then places into array
class readInAudioFiles:
	def getArrayOfAudioFiles(self, directoryGivenByUser, parameters):
		self.cwd = os.getcwd()

		needsConverting = self.checkIfNeedsConverting(directoryGivenByUser)
		performingDirectory = self.getPerformingDirectory(needsConverting, 
			directoryGivenByUser)
		audioFiles = self.putAudioFilesInArray(performingDirectory)
		#parameters.createStream(os.path.realpath(audioFiles[0]))
		return audioFiles 

	def checkIfNeedsConverting(self, directoryGivenByUser):
		convert = False
		self.numberOfFiles = 0
		for entry in os.scandir(directoryGivenByUser):
			if(".mp3" in entry.name):
				convert = True
			self.numberOfFiles += 1
		return convert

	def getPerformingDirectory(self, needsConverting, directoryGivenByUser):
		if needsConverting is True:
			performingDirectory = self.convertAndCopyFiles(directoryGivenByUser)
		elif needsConverting is False:
			performingDirectory = directoryGivenByUser
		return performingDirectory

	def convertAndCopyFiles(self, directoryGivenByUser):
		outputDirectory = self.createOutputDirectory()
		os.makedirs(outputDirectory)
		os.chdir(outputDirectory)

		threads = self.createThreads()
		index = 0

		for entry in os.scandir(directoryGivenByUser):
			print(index) 
			if(".wav" in entry.name):
				threads[index] = threading.Thread(target=self.copyFile, args=(entry,outputDirectory,))
			elif(".mp3" in entry.name):
				#threads[index] = threading.Thread(target=self.convertFile, args=(entry,))
				print("converting...")
				sound = AudioSegment.from_mp3(os.path.realpath(entry))
				sound.export((entry.name[:-4] + ".wav"), format="wav")
			threads[index].start()
			index += 1
		return outputDirectory

	def createOutputDirectory(self):
		now = datetime.now()
		folderName = now.strftime("%d-%m-%Y %H.%M.%S")
		return self.cwd + "\\" + folderName

	def createThreads(self):
		array = []
		for each in range(0, self.numberOfFiles):
			thread = threading.Thread()
			array.append(thread)
		return array

	def copyFile(self, file, outputDirectory):
		print("copying...")
		shutil.copy2(os.path.realpath(file), outputDirectory)
		return

	def convertFile(self, file):
		print("converting...")
		sound = AudioSegment.from_mp3(os.path.realpath(file))
		sound.export((file.name[:-4] + ".wav"), format="wav")
		return

	def putAudioFilesInArray(self, performingDirectory):
		os.chdir(self.cwd)
		array = []
		count = 0
		for entry in os.scandir(performingDirectory): 
			if(".wav" in entry.name):
   				array.append(entry)
   				print(array[count].name)
   				count = count + 1
		return array
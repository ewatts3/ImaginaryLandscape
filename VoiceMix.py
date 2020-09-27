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

class VoiceMix:
	def __init__(self, lengthOfSamples, lengthOfMix, directory):
		self.readInAudioFiles(directory)
		self.createMix(lengthOfSamples, lengthOfMix)

	def readInAudioFiles(self, directory):
		riaf = readInAudioFiles()
		self.audioFiles = riaf.getArrayOfAudioFiles(directory)
		return

	def getNumberOfDecimalPoints(self, lengthOfSamples):
		numberOfDecimalPoints = len(str(lengthOfSamples).split('.')[1])
		decimalConstant = '1'
		print(numberOfDecimalPoints)
		for each in range(0, numberOfDecimalPoints): 
			decimalConstant += '0'
		print(decimalConstant)
		return decimalConstant

	def selectRandomAudioFile(self):
		return self.audioFiles[random.randrange(0, len(self.audioFiles) - 1, 1)]

	def createMix(self, lengthOfSamples, lengthOfMix):
		print("begin mix")
		self.outputFile = wave.open('outputFile.wav','w')
		self.outputFile.setnchannels(1) # mono
		self.outputFile.setsampwidth(2)
		self.outputFile.setframerate(44100.0 * 2)

		numberOfDecimalPoints = 1
		if(int(lengthOfSamples) % 1) is not 0:
			print("here")
			numberOfDecimalPoints = int(self.getNumberOfDecimalPoints(lengthOfSamples))

		for each in range(0, numberOfDecimalPoints * lengthOfMix):
			currentFile = wave.open(os.path.realpath(self.selectRandomAudioFile()), "rb")
			p = pyaudio.PyAudio()
			stream = p.open(format = p.get_format_from_width(currentFile.getsampwidth()),
						input_device_index = 4,  
	               		channels = currentFile.getnchannels(),  
	                	rate = currentFile.getframerate(),  
	                	output = True)

			#find length of audio file in seconds
			frames = currentFile.getnframes()
			rate = currentFile.getframerate()
			duration = int(frames / float(rate))

			#decide where to start
			start = random.randrange(0, int(duration) - 1, 1)

			#skip unwanted frames
			n_frames = int(start * currentFile.getframerate())
			currentFile.setpos(n_frames)

			n_frames = int(lengthOfSamples * currentFile.getframerate())
			frames = currentFile.readframes(n_frames)

			self.outputFile.writeframes(frames)

			stream.close()
			p.terminate()
			currentFile.close()

		self.outputFile.close()
		print("done")
		return
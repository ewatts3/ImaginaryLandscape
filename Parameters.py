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
import json

#class of parameters set by the user
class Parameters:
	def __init__(self):
		#file = open("Parameters.json")
		#data = json.load(file)
		#self.setDirectoryForFiles()
		#print('hi')
		return

	def setDirectoryForFiles(self, input):
		self.directoryForFiles = input
		return

	def getDirectoryForFiles(self):
		return self.directoryForFiles

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

	def setMaximumLengthOfSample(self, input):
		self.maximumLengthOfSample = input
		return

	def getMaximumLengthOfSample(self):
		return self.maximumLengthOfSample

	#def createStream(self, firstFile):
	#	file = wave.open(firstFile, "rb")
	#	p = pyaudio.PyAudio()
	#	self.stream = p.open(
	#		format = pyaudio.get_format_from_width(file.getsampwidth()),
	#		rate = file.getframerate(),
	#		channels = file.getnchannels(),
	#		input = False,
	#		output = True,
	#		output_device_index = 3)
	#	return

	#def getStream(self):
	#	return self.stream
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

#class to do all the operations relating to playing the file
class Music:
	#performs all necessary operations to play a file
	def play(self, musicFile, min, max):
		#try:
			file = wave.open(os.path.realpath(musicFile), "rb")
			p = pyaudio.PyAudio()
			stream = self.openStream(file, p)

			durationOfTrack = self.getDuration(file)
			start = self.decideStart(durationOfTrack)
			length = self.decideLength(min, max)
			file.setpos(self.setPosition(start, file))
			stream.write(self.getFramesToWrite(length, file))

			#file.close()
			print("endTrack")
			self.finish(stream, p, file)
			return
		#except:
		#	print("error")
		#	return

	#open audio output stream
	def openStream(self, file, p):
		return p.open(format = pyaudio.get_format_from_width(file.getsampwidth()),
	               	channels = file.getnchannels(),  
	                rate = file.getframerate(),
	                output = True,
	                output_device_index = 4)  

	#find length of audio file in seconds
	def getDuration(self, file):
		return int(file.getnframes() / float(file.getframerate()))

	#decide starting position of sample
	def decideStart(self, duration):
		return random.randrange(0, duration, 1)

	#decide total length of sample to be played
	def decideLength(self, min, max):
		return random.randrange(min, max, 1)

	#set position of open audio file to correct starting point
	def setPosition(self, start, file):
		return int(start * file.getframerate())

	#calculate which frames to write to the audio buffer
	def getFramesToWrite(self, length, file):
		return file.readframes(int(length * file.getframerate()))

	def finish(self, s, p, f):
		s.close()
		p.terminate()
		f.close()
		print("endTrack")
		return
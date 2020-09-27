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

#the class "Thread" is used to hold not only the threads, 
#but the probability that they will play that is associated with them as well
class Thread:
	def __init__(self, thread, probability):
		self.thread = thread
		self.probability = int(probability)
		#print(self.probability)

	def setThread(self, threadStart):
		self.thread = threadStart

	def getThread(self):
		return self.thread

	def getProbability(self):
		return self.probability
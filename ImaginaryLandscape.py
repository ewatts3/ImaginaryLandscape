import pyaudio
from pydub import AudioSegment
import wave
import os
import shutil
import random
import threading
from time import time, sleep
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

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
		self.audioFiles = riaf.getArrayOfAudioFiles(self.parameters.getDirectoryForFiles())
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
					self.parameters.getMaximumLengthOfSample(),))
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

#class of parameters set by the user
class Parameters:
	#def __init__ (self, directoryForFiles,
	#	numberOfTracks, divisionConstant, 
	#	minimumTimeBetweenChecks, maximumTimeBetweenChecks,
	#	minimunLengthOfPiece, maximumLengthOfPiece,
	#	minimumLengthOfSample, maximumLengthOfSample):
	#	self.directoryForFiles= directoryForFiles
	#	self.numberOfTracks = numberOfTracks
	#	self.divisionConstant = divisionConstant
	#	self.minimumTimeBetweenChecks = minimumTimeBetweenChecks
	#	self.maximumTimeBetweenChecks = maximumTimeBetweenChecks
	#	self.minimunLengthOfPiece = minimunLengthOfPiece
	#	self.maximumLengthOfPiece = maximumLengthOfPiece
	#	self.minimumLengthOfSample = minimumLengthOfSample
	#	self.maximumLengthOfSample = maximumLengthOfSample

	def __init__(self):
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

class readInAudioFiles:
	def getArrayOfAudioFiles(self, directoryGivenByUser):
		self.cwd = os.getcwd()

		needsConverting = self.checkIfNeedsConverting(directoryGivenByUser)
		performingDirectory = self.getPerformingDirectory(needsConverting, 
			directoryGivenByUser)
		audioFiles = self.putAudioFilesInArray(performingDirectory)
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

#class to do all the operations relating to playing the file
class Music:
	#performs all necessary operations to play a file
	def play(self, musicFile, min, max):
		file = wave.open(os.path.realpath(musicFile), "rb")
		p = pyaudio.PyAudio()
		stream = self.openStream(p, file)

		durationOfTrack = self.getDuration(file)
		start = self.decideStart(durationOfTrack)
		length = self.decideLength(min, max)
		file.setpos(self.setPosition(start, file))
		stream.write(self.getFramesToWrite(length, file))
		self.finish(stream, p, file)

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

#####################################################################

class UI:
	def __init__(self):
		self.createMainWindow()
		self.createTabs()
		self.mainWindow.mainloop()
		return

	def createMainWindow(self):
		self.mainWindow = Tk()
		self.mainWindow.title("Imaginary Landscape")
		self.mainWindow.iconbitmap(r'C:\Users\ericw\Documents\Python\ImgainaryLandscape\assests\ILicon.ico')
		self.mainWindow.geometry('500x500')
		return

	def createTabs(self):
		self.font = "Falling Sky"
		self.tab_control = ttk.Notebook(self.mainWindow)
		self.createPerformTab()
		self.createInformationTab()
		return

	def createPerformTab(self):
		self.performTab = ttk.Frame(self.tab_control)
		self.tab_control.add(self.performTab, text='Perform')
		self.tab_control.pack(expand=1, fill="both")
		self.createAllFramesForPerformTab()
		return

	def createInformationTab(self):
		self.informationTab = ttk.Frame(self.tab_control)
		self.tab_control.add(self.informationTab, text='Information')
		self.tab_control.pack(expand=1, fill="both")
		return

	def createAllFramesForPerformTab(self):
		self.createNumberOfTracksFrame()
		self.createLengthOfPieceFrame()
		self.createLengthOfSampleFrame()
		self.createTimeBetweenChecksFrame()
		self.createFileDirectoryFrame()
		self.createPerformButton()
		return

	def createNumberOfTracksFrame(self):
		numberOfTracksLabelFrame = LabelFrame(self.performTab, text="Number of Tracks", font=(self.font, 10), bd=8)
		self.numberOfTracksSpinbox = Spinbox(numberOfTracksLabelFrame, from_=0, to=1000, width=5)

		numberOfTracksLabelFrame.pack(fill="both", expand="no")
		self.numberOfTracksSpinbox.pack()
		return

	def createLengthOfPieceFrame(self):
		lengthOfPieceFrame = LabelFrame(self.performTab, text="Length of Piece", font=(self.font, 10), bd=8)

		minimumFrame = LabelFrame(lengthOfPieceFrame, text="Minimum", font=(self.font, 10))
		minimumMinutesText = Label(minimumFrame, text="Minutes", font=(self.font, 10))
		self.minimumMinutesSpinbox = Spinbox(minimumFrame, from_=0, to=1000)
		minimumSecondsText = Label(minimumFrame, text="Seconds", font=(self.font, 10))
		self.minimumSecondsSpinbox = Spinbox(minimumFrame, from_=0, to=1000)

		maximumFrame = LabelFrame(lengthOfPieceFrame, text="Maximum", font=(self.font, 10))
		maximumMinutesText = Label(maximumFrame, text="Minutes", font=(self.font, 10))
		self.maximumMinutesSpinbox = Spinbox(maximumFrame, from_=0, to=1000)
		maximumSecondsText = Label(maximumFrame, text="Seconds", font=(self.font, 10))
		self.maximumSecondsSpinbox = Spinbox(maximumFrame, from_=0, to=1000)

		lengthOfPieceFrame.pack(fill="both", expand="no")

		minimumFrame.pack(fill="both", expand="no")
		minimumMinutesText.pack(side = LEFT)
		self.minimumMinutesSpinbox.pack(side = LEFT)
		minimumSecondsText.pack(side = LEFT)
		self.minimumSecondsSpinbox.pack(side = LEFT)

		maximumFrame.pack(fill="both", expand="no")
		maximumMinutesText.pack(side = LEFT)
		self.maximumMinutesSpinbox.pack(side = LEFT)
		maximumSecondsText.pack(side = LEFT)
		self.maximumSecondsSpinbox.pack(side = LEFT)
		return

	def createLengthOfSampleFrame(self):
		lengthOfSampleFrame = LabelFrame(self.performTab, text="Length of Sample", font=(self.font, 10), bd=8)
		minimumText = Label(lengthOfSampleFrame, text="Minimum", font=(self.font, 10))
		self.minimumLengthOfSampleSpinbox = Spinbox(lengthOfSampleFrame, from_=0, to=1000)
		maximumText = Label(lengthOfSampleFrame, text="Maximum", font=(self.font, 10))
		self.maximumLengthOfSampleSpinbox = Spinbox(lengthOfSampleFrame, from_=0, to=1000)

		lengthOfSampleFrame.pack(fill="both", expand="no")
		minimumText.pack(side = LEFT)
		self.minimumLengthOfSampleSpinbox.pack(side = LEFT)
		maximumText.pack(side = LEFT)
		self.maximumLengthOfSampleSpinbox.pack(side = LEFT)
		return

	def createTimeBetweenChecksFrame(self):
		timeBetweenChecksFrame = LabelFrame(self.performTab, text="Time Between Checks", font=(self.font, 10), bd=8)
		minimumText = Label(timeBetweenChecksFrame, text="Minimum", font=(self.font, 10))
		self.minimumTimeBetweenChecksSpinbox = Spinbox(timeBetweenChecksFrame, from_=0, to=1000)
		maximumText = Label(timeBetweenChecksFrame, text="Maximum", font=(self.font, 10),)
		self.maximumTimeBetweenChecksSpinbox = Spinbox(timeBetweenChecksFrame, from_=0, to=1000)

		timeBetweenChecksFrame.pack(fill="both", expand="no")
		minimumText.pack(side = LEFT)
		self.minimumTimeBetweenChecksSpinbox.pack(side = LEFT)
		maximumText.pack(side = LEFT)
		self.maximumTimeBetweenChecksSpinbox.pack(side = LEFT)
		return

	def openFileDirectory(self):
		self.directoryChosen = filedialog.askdirectory()
		self.setDirectoryTextBox(self.directoryChosen)
		return

	def setDirectoryTextBox(self, directory):
		self.filePathTextBox.config(state='normal')
		self.filePathTextBox.delete(0, END)
		self.filePathTextBox.insert(0, directory)
		self.filePathTextBox.config(state='disabled')
		return

	def createFileDirectoryFrame(self):
		fileDirectoryFrame = LabelFrame(self.performTab, text="Choose Directory for Files", font=(self.font, 10), bd=8)
		openFileExplorerButton = Button(fileDirectoryFrame, text="Choose...", font=(self.font, 10),
			bg="black", fg="white", command=self.openFileDirectory)
		self.filePathTextBox = Entry(fileDirectoryFrame, width=65, state='disabled')
		fileDirectoryFrame.pack(fill="both", expand="no")
		openFileExplorerButton.pack(side = LEFT, padx=5, pady= 5)
		self.filePathTextBox.pack(side = LEFT, padx=10)
		return

	def perform(self):
		parameters = Parameters()
		parameters.setNumberOfTracks(int(self.numberOfTracksSpinbox.get()))
		parameters.setMinimumLengthOfPiece((int(self.minimumMinutesSpinbox.get()) * 60) + int(self.minimumSecondsSpinbox.get()))
		parameters.setMaximumLengthOfPiece((int(self.maximumMinutesSpinbox.get()) * 60) + int(self.maximumSecondsSpinbox.get()))
		parameters.setMinimumLengthOfSample(int(self.minimumLengthOfSampleSpinbox.get()))
		parameters.setMaximumLengthOfSample(int(self.maximumLengthOfSampleSpinbox.get()))
		parameters.setMinimumTimeBetweenChecks(int(self.minimumTimeBetweenChecksSpinbox.get()))
		parameters.setMaximumTimeBetweenChecks(int(self.maximumTimeBetweenChecksSpinbox.get()))
		parameters.setDirectoryForFiles(self.directoryChosen)
		parameters.setDivisionConstant(2)
		il = ImaginaryLandscape(parameters)
		return

	def createPerformButton(self):
		#performButtonFrame = LabelFrame(self.performTab, text="perform", bd = 8)
		performButton = Button(self.performTab, text="Perform", font=(self.font, 10),
			bg = "black", fg="white", height=1, width=30, command=self.perform)
		#performButtonFrame.pack(fill="both", expand="no")
		performButton.pack(side = TOP)
		return

############################################################################################################################
#put in README for divisionConstant:
#Ex: with 2, we start with 100, then divide it by 2, and get 50
#for the next thread, we take that 50, and divide it by 2, and get 25
#for the next thread, we take that 25, and divide it by 2, and get 12 (through integer division)
#etc...

#parameters = Parameters(
#	directoryForFiles,
#	numberOfTracks, 
#	divisionConstant, 
#	minimumTimeBetweenChecks,
#	maximumTimeBetweenChecks,
#	minimunLengthOfPiece, 
#	maximumLengthOfPiece,
#	minimumLengthOfSample,
#	maximumLengthOfSample)

ui = UI()
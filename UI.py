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

from Parameters import Parameters
from ImaginaryLandscape import ImaginaryLandscape

class UI:
	def __init__(self):
		self.parameters = Parameters()
		self.createMainWindow()
		self.createTabs()
		self.mainWindow.mainloop()
		return

	def createMainWindow(self):
		self.mainWindow = Tk()
		self.mainWindow.title("Imaginary Landscape")
		#self.mainWindow.iconbitmap(r'icon.ico')
		self.mainWindow.geometry('500x370')
		return

	def createTabs(self):
		self.font = "Falling Sky"
		self.tab_control = ttk.Notebook(self.mainWindow)
		self.createPerformTab()
		#self.createVoiceMixTab()
		#self.createInformationTab()
		self.tab_control.pack(expand=1, fill="both")
		return

	def createPerformTab(self):
		self.performTab = ttk.Frame(self.tab_control)
		self.tab_control.add(self.performTab, text='Perform')
		self.createAllFramesForPerformTab()
		return

	#def createVoiceMixTab(self):
		#self.voiceMixTab = ttk.Frame(self.tab_control)
		#self.tab_control.add(self.voiceMixTab, text='Voice Mix')
		#self.createAllFramesForVoiceMixTab()
		#return

	#def createInformationTab(self):
		#self.informationTab = ttk.Frame(self.tab_control)
		#self.tab_control.add(self.informationTab, text='Information')
		#return

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
		#self.numberOfTracksSpinbox = Spinbox(numberOfTracksLabelFrame, from_=1, to=1000, textVariable=self.parameters.getNumberOfTracks(), width=5)
		self.numberOfTracksSpinbox = Spinbox(numberOfTracksLabelFrame, from_=1, to=1000, width=5)

		numberOfTracksLabelFrame.pack(fill="both", expand="no")
		self.numberOfTracksSpinbox.pack()
		return

	def createLengthOfPieceFrame(self):
		lengthOfPieceFrame = LabelFrame(self.performTab, text="Length of Piece", font=(self.font, 10), bd=8)

		minimumFrame = LabelFrame(lengthOfPieceFrame, text="Minimum", font=(self.font, 10))
		minimumMinutesText = Label(minimumFrame, text="Minutes", font=(self.font, 10))
		self.minimumMinutesSpinbox = Spinbox(minimumFrame, from_=0, to=1000)
		minimumSecondsText = Label(minimumFrame, text="Seconds", font=(self.font, 10))
		self.minimumSecondsSpinbox = Spinbox(minimumFrame, from_=1, to=1000)

		maximumFrame = LabelFrame(lengthOfPieceFrame, text="Maximum", font=(self.font, 10))
		maximumMinutesText = Label(maximumFrame, text="Minutes", font=(self.font, 10))
		self.maximumMinutesSpinbox = Spinbox(maximumFrame, from_=0, to=1000)
		maximumSecondsText = Label(maximumFrame, text="Seconds", font=(self.font, 10))
		self.maximumSecondsSpinbox = Spinbox(maximumFrame, from_=1, to=1000)

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
		self.minimumLengthOfSampleSpinbox = Spinbox(lengthOfSampleFrame, from_=1, to=1000)
		maximumText = Label(lengthOfSampleFrame, text="Maximum", font=(self.font, 10))
		self.maximumLengthOfSampleSpinbox = Spinbox(lengthOfSampleFrame, from_=1, to=1000)

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
		self.parameters.setNumberOfTracks(int(self.numberOfTracksSpinbox.get()))
		self.parameters.setMinimumLengthOfPiece((int(self.minimumMinutesSpinbox.get()) * 60) + int(self.minimumSecondsSpinbox.get()))
		self.parameters.setMaximumLengthOfPiece((int(self.maximumMinutesSpinbox.get()) * 60) + int(self.maximumSecondsSpinbox.get()))
		self.parameters.setMinimumLengthOfSample(int(self.minimumLengthOfSampleSpinbox.get()))
		self.parameters.setMaximumLengthOfSample(int(self.maximumLengthOfSampleSpinbox.get()))
		self.parameters.setMinimumTimeBetweenChecks(int(self.minimumTimeBetweenChecksSpinbox.get()))
		self.parameters.setMaximumTimeBetweenChecks(int(self.maximumTimeBetweenChecksSpinbox.get()))
		self.parameters.setDirectoryForFiles(self.directoryChosen)
		self.parameters.setDivisionConstant(2)
		il = ImaginaryLandscape(self.parameters)
		return

	def createPerformButton(self):
		#performButtonFrame = LabelFrame(self.performTab, text="perform", bd = 8)
		performButton = Button(self.performTab, text="Perform", font=(self.font, 10),
			bg = "black", fg="white", height=1, width=30, command=self.perform)
		#performButtonFrame.pack(fill="both", expand="no")
		performButton.pack(side = TOP)
		return

	#def createAllFramesForVoiceMixTab(self):
		#self.createLengthOfSampleFrameVM()
		#self.createLengthOfMixFrameVM()
		#self.createFileDirectoryFrameVM()
		#self.createCreateMixButtonVM()
		#return

	#def createLengthOfSampleFrameVM(self):
		#lengthOfSampleFrameVM = LabelFrame(self.voiceMixTab, text="Length of Each Sample", font=(self.font, 10), bd=8)
		#self.lengthOfSampleEntryVM = Entry(lengthOfSampleFrameVM, text ='3', width=5)

		lengthOfSampleFrameVM.pack(fill="both", expand="no")
		self.lengthOfSampleEntryVM.pack()
		return

	#def createLengthOfMixFrameVM(self):
		#lengthOfMixFrameVM = LabelFrame(self.voiceMixTab, text="Length of Mix", font=(self.font, 10), bd=8)
		#self.lengthOfMixEntryVM = Entry(lengthOfMixFrameVM, width=5)

		#lengthOfMixFrameVM.pack(fill="both", expand="no")
		#self.lengthOfMixEntryVM.pack()
		#return

	def openFileDirectoryVM(self):
		self.directoryChosenVM = filedialog.askdirectory()
		self.setDirectoryTextBoxVM(self.directoryChosenVM)
		return

	def setDirectoryTextBoxVM(self, directory):
		self.filePathTextBoxVM.config(state='normal')
		self.filePathTextBoxVM.delete(0, END)
		self.filePathTextBoxVM.insert(0, directory)
		self.filePathTextBoxVM.config(state='disabled')
		return

	def createFileDirectoryFrameVM(self):
		fileDirectoryFrameVM = LabelFrame(self.voiceMixTab, text="Choose Directory for Files", font=(self.font, 10), bd=8)
		openFileExplorerButtonVM = Button(fileDirectoryFrameVM, text="Choose...", font=(self.font, 10),
			bg="black", fg="white", command=self.openFileDirectoryVM)
		self.filePathTextBoxVM = Entry(fileDirectoryFrameVM, width=65, state='disabled')
		fileDirectoryFrameVM.pack(fill="both", expand="no")
		openFileExplorerButtonVM.pack(side = LEFT, padx=5, pady= 5)
		self.filePathTextBoxVM.pack(side = LEFT, padx=10)
		return

	#def createMix(self):
		#cm = VoiceMix(float(self.lengthOfSampleEntryVM.get()),
			#int(self.lengthOfMixEntryVM.get()),
			#self.directoryChosenVM)
		#return

	#def createCreateMixButtonVM(self):
		#createCreateMixButtonVM = Button(self.voiceMixTab, text="Create Mix", font=(self.font, 10),
			#bg = "black", fg="white", height=1, width=30, command=self.createMix)
		#createCreateMixButtonVM.pack(side = TOP)
		#return
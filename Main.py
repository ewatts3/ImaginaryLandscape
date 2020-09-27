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

from ImaginaryLandscape import ImaginaryLandscape
from Music import Music
from Parameters import Parameters
from ReadInAudioFiles import readInAudioFiles
from Thread import Thread
from UI import UI

try:
    run = UI()
except:
    print("crash")

print("done")
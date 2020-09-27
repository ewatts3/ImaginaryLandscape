import moviepy.editor as mp
from pygame import *
import random
import threading
import os
from time import time, sleep

class Video:
    def __init__(self, sourceClip):
        self.sourceClip = sourceClip
        self.clipDuration = self.findClipDuration(sourceClip)
        return

    def findClipDuration(self, sourceClip):
        return int(sourceClip.duration)

    def createClip(self):
        tempSourceClipCopy = self.sourceClip
        start = self.decideClipStartTime()
        end = self.decideClipEndTime()
        self.clip = tempSourceClipCopy.subclip(t_start=4,t_end=8)

        print(self.sourceClip)
        print(self.clip)
        return 

    def decideClipStartTime(self):
        self.clipStart = random.randrange(0, self.clipDuration - 1, 1)
        return self.clipStart

    def decideClipEndTime(self):
        clipEnd = random.randrange(self.clipStart, self.clipDuration, 1)
        return clipEnd

    def getClip(self):
        returnClip = self.clip
        return returnClip

    def setNextVideo(self, nextVideo):
        self.nextVideo = nextVideo
        self.nextVideo.createClip()
        return

    def getNextVideo(self):
        return self.nextVideo
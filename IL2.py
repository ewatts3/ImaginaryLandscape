import os
import winsound
import random
from time import time, sleep

startTime = time()
audioFiles = [] #array of all audio files
done = False #determines if program will stop (after x minutes)

#scan in all the audio files that will be used in store them in an array
count = 0
for entry in os.scandir():  
    audioFiles.append(entry)
    print(audioFiles[count].name)
    count = count + 1
    #print(os.path.realpath(audioFiles[count])

#this loop performs it's actions for *at least* x minutes,
#then has a 10% chance of stopping, at which point the program stops.
#it selects a random index in the array soundFiles, plays that sound file,
#pauses for a random amount of time, then repeats.
while not done:
    if random.randrange(0, 2, 1) == 0:
        winsound.PlaySound(audioFiles[random.randrange(0, len(audioFiles) - 1, 1)].name, winsound.SND_ASYNC)
        if (time() - startTime) > 60:
            if random.randrange(0, 5, 1) == 0: #change to 10 later
                done = True
        sleep(random.randrange(0, 20, 1))

print('Here')
winsound.PlaySound(None, winsound.SND_FILENAME)
sleep(random.randrange(0, 60, 1))
k = random.randrange(2, 10, 1)
for i in range(k):
    winsound.PlaySound('9-16', winsound.SND_FILENAME)
            
winsound.PlaySound(None, winsound.SND_FILENAME)
print('Done')

#problems:
#can't play more than one at a time
#can't start at random place
#pause between some of them?
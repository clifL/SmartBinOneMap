import time
from time import sleep
import RPi.GPIO as GPIO

def GetUltrasonicData():
    #The bindepth is a mean value after several trials
    binDepth = 13.5
    dataset = []
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    trig = 18
    echo = 16
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    GPIO.output(trig, True)
    time.sleep(0.50)
    GPIO.output(trig, False)
    while GPIO.input(echo) == 0:
        pulseStart = time.time()
    while GPIO.input(echo) == 1:
        pulseEnd = time.time()
    timeLapsed = pulseEnd - pulseStart
    #calculating distance based on time elasped
    distance = round(((timeLapsed * 34000)/2), 2)
    # raw cm of current distance detected by wave
    fullness = binDepth - distance
    #converting distance measured into percentage
    fullnessPercent = round(fullness/binDepth * 100)
    if fullness <= 0:
        fullnessPercent = 0
    if fullness > 100:
        fullnessPercent = 100
    #store the data into an array and return it 
    dataset.insert(0, distance)
    dataset.insert(1, fullnessPercent)
    return dataset
    
 
import time
from time import sleep
import datetime
from smbus2 import SMBus
import RPi.GPIO as GPIO
import sys
import multiprocessing
import os
import paho.mqtt.client as mqtt
import json
from RouteManager import *
import Connect
import TelegramBot
import Thingsboard
from Prediction import *
from BluetoothController import *
from ctypes import *
import threading
from ServoMotor import *
from Ultrasonic import *
from Infrared import *
from Helper import *

class BinData:
    def __init__(self, Location, TimeDateFull, Confidence):
        self.Location = Location
        self.TimeDateFull = TimeDateFull
        self.Confidence = Confidence


def Main():
    try:
        temperatureLog = []
        TurnServoMotor(False)
        currentObjectTemperatue = GetIRTemperature()
        Thingsboard.SendTemperature(currentObjectTemperatue)
        timerInterupt = threading.Timer(5.0, PrintStatus)
        timerInterupt.start()
        while True:
            sum = 0.0
            currentObjectTemperatue = GetIRTemperature()
            temperatureLog.append(currentObjectTemperatue)
            for temperature in temperatureLog:
                sum += temperature
            average = sum / len(temperatureLog)
            if ((currentObjectTemperatue > (average + 0.35)) or (currentObjectTemperatue < (average - 0.35))):
                temperatureLog.pop()
                TurnServoMotor(True)
                isContact = True
                while isContact:
                    currentObjectTemperatue = GetIRTemperature()
                    if ((currentObjectTemperatue > (average + 0.35)) or (currentObjectTemperatue < (average - 0.35))):
                        sleep(3)
                    else:
                        TurnServoMotor(False)
                        isContact = False
            if (len(temperatureLog) > 50):
                del temperatureLog[0]
            sleep(0.2)
    except:
        pass


def Coroutine(numberOfDevices):
    previousTrashLevel = -1.0
    trashThrown = 0.0
    location = GetPiLocation()
    USDataset = []
    alertLevel = 70
    while True:
        hibernationDuration = GetHibernationDuration()
        if hibernationDuration > 90:
            sleep((hibernationDuration - 90))
            numberOfDevices.value = GetBluetoothDevices()
            sleep(GetHibernationDuration())
        else:
            numberOfDevices.value = GetBluetoothDevices()
            sleep(hibernationDuration)

        USDataset = GetUltrasonicData()
        if previousTrashLevel == 1.0:
            previousTrashLevel = USDataset[1]
        else:
            trashThrown = USDataset[1] - previousTrashLevel
            previousTrashLevel = USDataset[1]
        currentObjectTemperatue = GetIRTemperature()
        Connect.CreateData(location, currentObjectTemperatue, USDataset[0], USDataset[1], numberOfDevices.value, GetTimeIndex(), trashThrown)
        if (USDataset[1] >= alertLevel):
            binDataSet = []
            timeIndex = GetTimeIndex()
            binDatasetTwo = Connect.GetBinData()
            for x in range(len(binDatasetTwo)):
                binPrediction = GetPrediction(binDatasetTwo[x].location, binDatasetTwo[x].numberOfDevice, timeIndex, binDatasetTwo[x].numberOfDevice)
                dateTimeObject = datetime.datetime.strptime(binPrediction.TimeDateFull, '%d-%m-%Y %H:%M:%S')
                binDataSet.append(BinData(binDatasetTwo[x].location, dateTimeObject, binPrediction.Confidence))        
            binPrediction = GetPrediction(location + "-ML-1", USDataset[1], timeIndex, numberOfDevices.value)
            dateTimeObject = datetime.datetime.strptime(binPrediction.TimeDateFull, '%d-%m-%Y %H:%M:%S')
            binDataSet.append(BinData(location+"-ML-1", dateTimeObject, binPrediction.Confidence))
            binDataSet.sort(key=lambda x: x.TimeDateFull)
            routeResult = FindShortestPath()
            availableTime = binDataSet[0].TimeDateFull.timestamp() - datetime.datetime.now().timestamp()
            if (availableTime > int(routeResult[1])):
                message = routeResult[0]
            else:
                message = "Priority Routing from SembWaste (Sequential Order):"
                for i in range(len(binDataSet)):
                    message = message + "\n" + str(i+1) + ". " + binDataSet[i].Location + "\nEstimated Bin Full at: " + str(binDataSet[i].TimeDateFull) + "\n"
                        
            TelegramBot.SendTelegramMessage("Alert - Bin at " + location + " reaches Ready-To-Collection Level" 
                                            + "\n\nCurrent Bin Capacity: " + str(USDataset[1]) + "%")
            TelegramBot.SendTelegramMessage(message)
            Thingsboard.SendUltrasonicPercentage(USDataset[1])
            Thingsboard.SendTemperature(currentObjectTemperatue)



def GetBinStatus(numberOfDevices):
    USDataset = GetUltrasonicData()
    location = GetPiLocation()
    hour = int(datetime.datetime.now().strftime("%H"))
    minute = int(datetime.datetime.now().strftime("%M"))
    timeIndex = (hour * 6)
    if minute != 0:
        timeIndex = timeIndex + (minute // 10)
    print("Bin Location: " + location)
    #print("Current Time Index: " + str(timeIndex))
    print("Current Capacity (+-5%): " + str(USDataset[1]) + "%")
    schedule = GetPrediction(
        location + "-ML-1", USDataset[1], timeIndex, numberOfDevices.value)
    print("Bin will be Full Capacity at: " +
          schedule.TimeDateFull + " (Estimated)")
    confidentLevel = schedule.Confidence * 100
    formattedLevel = "{:.2f}".format(confidentLevel)
    print("Confident Level of the Estimation: " + formattedLevel + "%")


def PrintStatus():
    print("Ready")


#Main Process
print("Please stay clear of the bin for 10 seconds while it initialise.")
os.system("vcgencmd display_power 0")
os.system("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/bind")
os.system("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind")
numberOfDevices = multiprocessing.Value("i", 0)
p1 = multiprocessing.Process(target=Main, daemon=True)
p2 = multiprocessing.Process(
    target=Coroutine, args=(numberOfDevices,), daemon=True)
p1.start()
p2.start()
while True:
    try:
        if p1.is_alive() != True:
            p1 = multiprocessing.Process(target=Main, daemon=True)
            p1.start()
        if p2.is_alive() != True:
            p2 = multiprocessing.Process(
                target=Coroutine, args=(numberOfDevices,), daemon=True)
            p2.start()
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        try:
            p1.terminate()
            p2.terminate()
            p1.join()
            p2.join()
            print("")
            TurnServoMotor(False)
            GetBinStatus(numberOfDevices)
            userInput = input("Enter 1 to resume the program: ")
            if userInput != "1":
                break
            print("Please stay clear of the bin for 10 seconds while it resume its service.")
        except KeyboardInterrupt:
            break



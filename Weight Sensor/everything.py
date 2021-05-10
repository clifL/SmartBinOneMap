import time
import sys
import setup
from ctypes import *
from setuptools import setup
from ctypes import *
import random
import csv


SterilizeData_so = "/Users/lamzh/Desktop/test.so"
SterilizeData = CDLL(SterilizeData_so)
dataValue = []

name='hx711',
version='0.1',
description='HX711 Python Library for Raspberry Pi',
py_modules=['hx711'],
install_requires=['Rpi.GPIO', 'numpy'],

EMULATE_HX711 = False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711


def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()


def getMeasurement():
    for i in range(100):
        try:
            val = hx.get_weight(5)
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
            dataValue.append(val)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


def get_weight(self):
    try:
        time.sleep(0.1)
        hx.power_up
        val = hx.get_weight(5)
        hx.power_down
        return val

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


def write_csv(self, choice):
    fileName = ""
    if choice == 1:
        fileName = "CapturedData.csv"
    with open(fileName, mode='w', newline='') as calibration_file:
        wr = csv.writer(calibration_file,  quoting=csv.QUOTE_ALL, lineterminator='\n')
        wr.writerow(dataValue)


hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Tare done! Add weight now...")
print('Enter weight: ')
weight = input()
print('Enter times data capture: ')
capture = input()
dataValue.append(capture)
getMeasurement(capture)
write_csv()
i = 0
while i == 0:
    print('Press 1 for calibration')
    print('Press 2 to get measurement in grams')
    print('Press 0 to exit')
    inputChoice = input()
    if inputChoice == 1:
        print('Enter weight')
        weight = input()
        get_weight()
        write_csv(1)









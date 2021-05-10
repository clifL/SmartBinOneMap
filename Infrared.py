#C Programming for MlX90614
from ctypes import *
import os

#Get IR temperature through shared object file, mlx90614 is written in c, in order for python to call this project, it has to be compiled into shared object
def GetIRTemperature():
    path = os.path.dirname(os.path.abspath(__file__)) + "/Mlx90614.so"
    temperatureSensor = CDLL(path)
    temperatureSensor.Main.restype = c_double 
    return temperatureSensor.Main()

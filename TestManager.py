from Infrared import *
from ServoMotor import *
from BluetoothController import *
from TelegramBot import *
from Ultrasonic import *
import RPi.GPIO as GPIO
from Helper import *
from Thingsboard import *
from Connect import *
from RouteManager import *
import Prediction
        

def TestUltrasonic():
    dataset = GetUltrasonicData()
    try:
        assert (dataset[0] >= 0 and dataset[0] <= 30)
        assert (dataset[1] >= 0 and dataset[1] <= 100)
    except:
        print("GetUltrasonicData() failed")


def TestInfrared():
    try:
        assert GetIRTemperature() > 0
    except:
        print("GetIRTemperature() failed")
        
        
def TestServoMotor():
    #Observe if the Servo Motor turns in real life
    try:
        assert (TurnServoMotor(True))
        assert (TurnServoMotor(False))
    except:
        print("TurnServoMotor() failed")


def TestTelegram():
    try:
        assert (SendTelegramMessage("Test"))
    except:
        print("SendTelegramMessage() failed")


def TestBluetooth():
    try:
        assert GetBluetoothDevices() >= 0
    except:
        print("GetBluetoothDevices failed")


def TestGetPiLocation():
    try:
        assert (GetPiLocation()) == "Bef Orchard Blvd"
    except:
        print("GetPiLocation() failed")
        

def TestGetTimeIndex():
    try:
        timeIndex = GetTimeIndex()
        assert (timeIndex >= 0 and timeIndex <= 143)
    except:
        print("GetTimeIndex() failed")
        

def TestGetHibernationDuration():
    try:
        duration = GetHibernationDuration()
        assert (duration >= 0 and duration <= 600)
    except:
        print("GetHibernationDuration() failed")


def TestThingsboardSendTemperature():
    try:
        assert (SendTemperature()) 
    except:
        print("SendTemperature() for Thingsboard failed")
        
        
def TestSendUltrasonicPercentage():
    try:
        assert (SendUltrasonicPercentage())
    except:
        print("SendUltrasonicPercentage() for Thingsboard failed")
        
        
def TestPin():
    uatPin = 33
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(uatPin, GPIO.OUT)
    while True:
        GPIO.output(uatPin, GPIO.HIGH)
        

def TestCreateData():
    try:
        assert CreateData("Test", 1, 2, 3, 4, 5, 6) == 201   
    except:
        print("CreateData() for RestDB failed")
        

def TestReadData():
    try:
        assert ReadData() != "-1"  
    except:
        print("ReadData() for RestDB failed")
        

def TestGetBinData():
    try:
        assert GetBinData() != "-1"  
    except:
        print("GetBinData() for RestDB failed")
        

def TestPostRequest():
    try:
        token = PostRequest()
        assert token != "-1"  
    except:
        print("PostRequest() for OneMap failed")
    return token
    


def TestGetRequest(token):
    try:
        assert GetRequest("1.3359318918779122,103.94469822951413", "1.302692387316223,103.82987370050854", token) != "-1" 
    except:
        print("GetRequest() for OneMap failed")
        

def TestML():
    try:
        assert (Prediction.GetPrediction("Bef Orchard Blvd-ML-1", 30.0, 10, 0))
    except:
        print("Test Machine Learning fail")




#Unit Testing
def AutomatedUnitTesting():
    TestUltrasonic()
    TestInfrared()
    TestServoMotor()
    TestTelegram()
    TestBluetooth()
    TestGetPiLocation()
    TestGetTimeIndex()
    TestGetHibernationDuration()
    TestThingsboardSendTemperature()
    TestSendUltrasonicPercentage()
    TestCreateData()    
    TestReadData()
    TestGetBinData()
    TestPostRequest()
    TestGetRequest(token)
    TestML()

    

AutomatedUnitTesting()
 



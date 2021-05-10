import numpy
from sklearn.metrics import r2_score
import Connect
import json
from datetime import date, timedelta
from scipy import stats


ydataTrash = []
ydataCrowd = []
timeAxis = []


# Object file for return type
class BinPrediction:
    def __init__(self, TimeDateFull, Confidence):
        self.TimeDateFull = TimeDateFull
        self.Confidence = Confidence


def GetDataBase(location):
    # Clearing of arrays
    timeAxis.clear()
    ydataTrash.clear()
    ydataCrowd.clear()
    # Load data from database and convert them into json type and store into variable
    cacheData = json.loads(Connect.ReadData())
    for i in range(len(cacheData)):
        if cacheData[i]["BinLocation"] == location:
            # Putting the value and appending it into the array for plotting into variable
            timeAxis.append(float(cacheData[i]["TimeIndex"]))
            ydataTrash.append(float(cacheData[i]["TrashThrown"]))
            ydataCrowd.append(float(cacheData[i]["NumberOfBluetoothDevice"]))


def GetPrediction(location, level, timeIndex, bluetooth): #Main Method
    returnBin = BinPrediction(0, 0) # Creating a new BinPrediction object
    additionalTrash = 0 # Initialize value of additional trash
    GetDataBase(location) # Calls method and input the value into the array
    trashModel = numpy.poly1d(numpy.polyfit(timeAxis, ydataTrash, 3)) # Create a model for polynomial regression for trash and time
    trashLine = numpy.linspace(1, 144, 100) # Best fit polynomial line
    crowdModel = numpy.poly1d(numpy.polyfit(timeAxis, ydataCrowd, 3)) # Create a model for polynimal regression for crowd and time
    crowdLine = numpy.linspace(1, 20, 100) # Best fit polynomial line
    PredictCrowd(timeIndex, crowdLine, crowdModel)
    predictedCrowd = float(PredictCrowd(timeIndex, crowdLine, crowdModel))
    trustCrowd = CrowdTrust(crowdModel) # Calls method to check if crowd data is trustable
    if int(bluetooth) >= float(predictedCrowd * 1.25) and trustCrowd is True: # Check condition to see if there is a surge and if the crowd data is trustable
        additionalTrash = CrowdLinear(int(bluetooth)) # Add trash level
    level = float(level) + float(additionalTrash) # Factor in the additional trash and the current trash for the trash value
    Predict(int(timeIndex), level, trashModel, trashLine, returnBin)
    return returnBin


def Predict(timeSlot, currentLevel, trashModel, trashLine, returnBin):
    cumulativeLevel = currentLevel
    timeSlot = timeSlot + 1
    isFull = False
    while isFull is False: # Check condition to check if bin is full
        futureLevel = float(trashModel((int(timeSlot) % 144))) # Get the predicted trash level of the next interval in x-xis
        if futureLevel < 0: # Prevent negative value
            futureLevel = 0
        cumulativeLevel = cumulativeLevel + float(futureLevel) # Cumulate current trash level with future trash level
        if cumulativeLevel >= 100: # Check condition to see if the cumulated trash level reaches 100%
            isFull = True # Set boolean to true
            returnBin.TimeDateFull = TimeConvert(int((int(timeSlot) % 144) - 1), int(timeSlot / 144)) # Return the time when the bin will be full
        timeSlot = timeSlot + 1
    returnBin.Confidence = r2_score(ydataTrash, trashModel(timeAxis)) # Calc R2 of the model


def PredictCrowd(timeSlot, crowdline, crowdModel):
    predictedLevel = float(crowdModel((int(timeSlot) % 144))) # Use linear regression to get the crowd level base on the time
    return predictedLevel


def CrowdLinear(crowdlevel):
    slope, intercept, r, p, std_err = stats.linregress(ydataTrash, ydataCrowd) # Linear regression of trash and crowd level
    return slope * crowdlevel + intercept # Returns the trash level base on crowd level


def CrowdTrust(crowdModel):
    score = r2_score(ydataCrowd, crowdModel(timeAxis)) # R2 score of polynomial graph
    if float(score) < 0.8: # Check condition if data is trustable or not
        return False
    else:
        return True


def TimeConvert(timeSlot, date_offset):
    today = date.today() + timedelta(days=date_offset) # Get today date and add additional day base on the offset
    convertedTime = str(ConvertHours(timeSlot)) + ":" + str(ConvertMinutes(timeSlot))
    convertedDate = today.strftime("%d-%m-%Y") # Returns the date which includes the offset
    return convertedDate + " " + convertedTime + ":00"


def ConvertHours(timeSlot):
    returnValue = int(timeSlot / 6)
    if timeSlot < 6:
        return "00"
    elif returnValue < 10:
        return "0" + str(returnValue)
    else:
        return str(returnValue)


def ConvertMinutes(timeSlot):
    returnValue = (int(timeSlot % 6))*10
    if returnValue == 0:
        return "00"
    else:
        return str(returnValue)
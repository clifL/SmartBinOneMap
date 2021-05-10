import os
import datetime

#Machine learning is measured by every 10 mins frequency, per day will be divided into 0 (00 00) to 143 (23 50) index. 
#This method will return the current index which will be used as the input.
def GetTimeIndex():
    try:
        hour = int(datetime.datetime.now().strftime("%H"))
        minute = int(datetime.datetime.now().strftime("%M"))
        timeIndex = (hour * 6)
        if minute != 0:
            timeIndex = timeIndex + (minute // 10)
        return timeIndex
    except:
        return -1


#Get time for the system to sleep, after it has completed its task on the 10 minutes rountine (Save resources)
def GetHibernationDuration():
    try:
        minute = int(datetime.datetime.now().strftime("%M"))
        minutesToWait = 10 - (minute % 10)
        second = int(datetime.datetime.now().strftime("%S"))
        return ((minutesToWait * 60) - second)
    except:
        return -1


#Instead of hard coding the bin location, we have a location.txt which user can edit for the location of the pi externally instead through the script
def GetPiLocation():
    try: 
        path = os.path.dirname(os.path.abspath(__file__)) + "/Location.txt"
        locationFile = open(path, "r")
        location = locationFile.read()
        locationFile.close()
        return location
    except:
        return ""

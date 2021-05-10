import requests
import json
import datetime
from json import JSONEncoder


class BinData:
    def __init__(self, location, capacity, numberOfDevice):
        self.location = location
        self.capacity = capacity
        self.numberOfDevice  = numberOfDevice


def CreateData(binLocation, currentTemperature, distance, capacity, numberOfDevices, timeIndex, trashThrown):
    url = "https://teamdrama-159c.restdb.io/rest/data"
    r = {
        "Timestamp": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        "BinLocation" : binLocation,
        "Temperature": currentTemperature,
        "Distance": distance,
        "USCapacity" : capacity,
        "NumberOfBluetoothDevice" : numberOfDevices,
        "TimeIndex": timeIndex,
        "TrashThrown": trashThrown
    }
    class Encoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime.datetime)):
                return obj.isoformat()    

    d = json.dumps(r,cls=Encoder,indent=4)
    headers = {
        'content-type': "application/json",
        'x-apikey': "835f4277b46fe83da4b25b56bf7ff40d740c5",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=d, headers=headers)
    return response.status_code

        
        
def GetBinData():
    url = "https://teamdrama-159c.restdb.io/rest/dustbin"
    headers = {
        'content-type': "application/json",
        'x-apikey': "835f4277b46fe83da4b25b56bf7ff40d740c5",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        return "-1"
    binArray = []
    cacheData = json.loads(response.text)
    for i in range(len(cacheData)):
        #print(cacheData[i]["Location"])
        binArray.append(BinData(str(cacheData[i]["Location"]), str(cacheData[i]["Capacity"]),
                                str(cacheData[i]["NumberOfDevice"])))
        
    return binArray


#read function
def ReadData():
    url = "https://teamdrama-159c.restdb.io/rest/data"
    headers = {
        'content-type': "application/json",
        'x-apikey': "835f4277b46fe83da4b25b56bf7ff40d740c5",
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        return "-1"
    return response.text

#dataset = GetBinData()
#for x in dataset:
#    print(x.location)



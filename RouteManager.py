import requests
import time
from time import sleep
import json
import itertools


def GetRequest(originGeometries, destinationGeometries, accessToken):
    originGeometries = originGeometries.replace(" ", "")
    destinationGeometries = destinationGeometries.replace(" ", "")
    url = "https://developers.onemap.sg/privateapi/routingsvc/route?start=" + str(originGeometries) + "&end=" + str(destinationGeometries) + "&routeType=walk&token=" + accessToken
    r = requests.get(url)
    while r.text == "":
        sleep(1)
    if r.status_code != 200:
        return "-1" 
    y = json.loads(r.text)
    return y["route_summary"]["total_time"]

    

def PostRequest():
    try:
        r = requests.post('https://developers.onemap.sg/privateapi/auth/post/getToken', json={"email":"1901820@sit.singaporetech.edu.sg","password":"Onemap_123"})
        while r.json == "":
            time.sleep(1)
            if r.status_code != 200:
                return "-1"
        y = json.loads(r.text)
        return y["access_token"]
    except:
        return "-1"
    

def LoopAllPermutations(startLocation, rawList):
    mappedCostList = {}
    permutationList=[]
    permutations =  list(itertools.permutations(rawList, len(rawList)))
    for pathTuple in permutations:
        pathList = list(pathTuple)
        pathList.insert(0, startLocation)
        permutationList.append(pathList)
    accessToken = PostRequest()
    for i in range(len(permutationList)):
        costSum = 0
        for x in range(len(permutationList[i])- 1):
            if (str(permutationList[i][x]) + "|" + str(permutationList[i][x+1])) in mappedCostList:
                costSum = costSum + mappedCostList[(str(permutationList[i][x]) + "|" + str(permutationList[i][x+1]))]
            else:
                cost = GetRequest(permutationList[i][x], permutationList[i][x+1], accessToken)
                #print(cost)
                #print(permutationList[i][x])
                #print(permutationList[i][x+1])
                #print(accessToken)
                mappedCostList[(permutationList[i][x] + "|" + permutationList[i][x+1])] = cost
                costSum = costSum + int(cost)
        permutationList[i].append(costSum)
    return permutationList


def FindShortestPath():
    pairedGeolocation = {
    "SembWaste" : "1.3359318918779122,103.94469822951413",
    "Bef Orchard Blvd" : "1.302692387316223,103.82987370050854",
    "Aft Tomlinson Rd" : "1.3061112483429593,103.82578978670266",
    "Opp Four Seasons Hotel" : "1.30450796427145,103.8291238011639",
    "Delfi Orchard" : "1.307037228310421,103.82839545961609",
    "Cliveden at Grange" : "1.2993458325434124,103.82662211642928"
    }
    geometryList = ["1.302692387316223,103.82987370050854", "1.3061112483429593,103.82578978670266", "1.30450796427145,103.8291238011639",
    "1.307037228310421,103.82839545961609", "1.2993458325434124,103.82662211642928"]
    permutationList = LoopAllPermutations("1.3359318918779122,103.94469822951413", geometryList)
    lowestPosition = 0
    lowestValue = permutationList[0][len(permutationList[0]) -1]
    k = 1
    for k in range(len(permutationList)):
        currentValue = permutationList[k][len(permutationList[0]) -1]
        if lowestValue > currentValue:
            lowestValue = currentValue
            lowestPosition = k
    shortestPath = ""
    count = 1
    for q in range(len(permutationList[lowestPosition]) -1):
        for x in pairedGeolocation:
            if pairedGeolocation[x] == permutationList[lowestPosition][q]:
                #shortestPath.append(x)
                if x == "SembWaste": continue
                shortestPath = shortestPath + str(count) + ". " + x + "\n" 
                count = count + 1
    returnResult = []
    returnResult.append("Shortest Path from SembWaste (Sequential Order):\n" + shortestPath)
    returnResult.append(str(lowestValue))
    return returnResult
import bluetooth

def GetBluetoothDevices():
    try: 
        nearbyDevices = bluetooth.discover_devices(lookup_names = False,lookup_class = False)
        noOfDevices = len(nearbyDevices)
        return noOfDevices
    except:
        return -1
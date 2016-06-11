def cmdToInt(cmd):
    if not isinstance(cmd, str):
        cmd = str(cmd)
    if cmd.lower() == 'on' or cmd == '1':
        return 1
    if cmd.lower() == 'off' or cmd == '0':
        return 0

class lightDef(object):
    def __init__(self):
        self.__WZ1 = ("WZ1", 1)
        self.__WZ2 = ("WZ2", 2)
        self.__SZ1 = ("SZ1", 4)
        self.__lightMap = []
        self.__lightMap.append(self.__WZ1)
        self.__lightMap.append(self.__WZ2)
        self.__lightMap.append(self.__SZ1)
        self.__triggerMaxSZValue = 15
        self.__triggerMaxKitchenValue = 50
        self.__kitchenIP = "192.168.0.11"
        self.__szIP = "192.168.0.88"

    def getLightID(self, lightString):
        for idTuple in self.__lightMap:
            if idTuple[0].lower() == lightString.lower():
                return idTuple[1]

    def getLightThreshold(self, sensorID):
        if sensorID.lower() == "kitchen":
            return self.__triggerMaxKitchenValue
        if sensorID.lower() == "sz":
            return self.__triggerMaxSZValue
        return 0
    
    def getIP(self, sensorID):
        if sensorID.lower() == 'kitchen':
            return self.__kitchenIP
        if sensorID.lower() == 'sz':
            return self.__szIP
    
    def getKitchenIP(self):
        return self.__kitchenIP
    
    def getSZIP(self):
        return self.__szIP
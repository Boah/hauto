class lightDef(object):
    def __init__(self):
        self.__WZ1 = ("WZ1", 1)
        self.__WZ2 = ("WZ2", 2)
        self.__SZ1 = ("SZ1", 4)
        self.__lightMap = []
        self.__lightMap.append(self.__WZ1)
        self.__lightMap.append(self.__WZ2)
        self.__lightMap.append(self.__SZ1)

    def getLightID(self, lightString):
        for idTuple in self.__lightMap:
            if idTuple[0] == lightString:
                return idTuple[1]

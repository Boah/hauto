'''
Created on 18.05.2016

@author: mirko
'''

class LightStatusStore(object):
    '''
    I am Borg
    '''
    __shared_state = {}
    __statusWZ1 = 'off'
    __statusWZ2 = 'off'
    __statusSZ1 = 'off'

    
    def __init__(self):
        self.__dict__ = self.__shared_state
        
    def getStatus(self):
        retVal = []
        retVal.append(('WZ1', self.__statusWZ1))
        retVal.append(('WZ2', self.__statusWZ2))
        retVal.append(('SZ1', self.__statusSZ1))
        return retVal
    
    def getStatusAsString(self):
        retStr = ""
        retVal = self.getStatus()
        for idx, tuple_ in enumerate(retVal):
            retStr += str(tuple_[0]) + "=" + str(tuple_[1])
            if(idx != len(retVal)-1):
                retStr += " "
        return retStr
    
    def setStatus(self, light, status):
        if(light.lower()=='wz1'):
            self.__statusWZ1 = self.__getStatusString(status)
        if(light.lower()=='wz2'):
            self.__statusWZ2 = self.__getStatusString(status)
        if(light.lower()=='sz1'):
            self.__statusSZ1 = self.__getStatusString(status)
            
    def __getStatusString(self, status):
        if(status.lower() == 'off' or status == '0'):
            return 'off'
        if(status.lower() == 'on' or status == '1'):
            return 'on'
    
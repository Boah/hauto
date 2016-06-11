'''
Created on 16.05.2016

@author: mirko
'''

import logging
import schedule

from subprocess import call
from .lightDef import lightDef
from sensorClient import LightSensorClient
from argumentParser.argumentParser import parseArgs
from .lightDef import cmdToInt
from lightStatusStore.lightStatusStore import LightStatusStore

class Trigger(object):
    '''
    classdocs
    '''


    def __init__(self, sensorQuery=None):
        '''
        Constructor
        '''
        self.__triggerPath = "/home/mirko/smarthome/raspberry-remote/send"
        self.__checkSensor = None
        if sensorQuery:
            self.activateSensorThreshold(sensorQuery)
        self.__defs = lightDef()
        self.__sensorClient = LightSensorClient()
        self.__lightStatusStore = LightStatusStore()

    def __trigger(self, light, cmd):
        try:
            logging.info("Try to set light " + str(light) + " to " + str(cmd))
            logging.info(call([self.__triggerPath, "10101", str(self.__defs.getLightID(light)), str(cmdToInt(cmd))]))
            self.__lightStatusStore.setStatus(light, cmd)
            return True
        except:
            logging.info("Tried to set light " + str(light) + " to " + str(cmd) + " failed")
            return False
            
    def triggerLight(self, light, cmd):
        if self.__checkSensor and cmd == 1:
            if self.__sensorClient.getLightValueFromServer(self.__defs.getIP(self.__checkSensor)) < self.__defs.getLightThreshold(self.__checkSensor):
                self.__trigger(light, cmd)
        else:
            self.__trigger(light, cmd)
            
    #Ignores internal Values
    def triggerLightWithSensor(self, light, cmd, sensor):
        if not isinstance(cmd, str):
            cmd = str(cmd)
        if cmd == '1' or cmd.lower() == 'on':
            sensorValue = self.__sensorClient.getLightValueFromServer(self.__defs.getIP(sensor))
            sensorThreshold = self.__defs.getLightThreshold(sensor)
            logging.info("comparing Sensor Value: " + str(sensorValue) + " with Sensor Threshold: " + str(sensorThreshold))
            if sensorValue < sensorThreshold:
                return self.__trigger(light, cmd)
        else:
            return self.__trigger(light, cmd)
            
    #Ignores internal Values
    def triggerLightWithoutSensor(self, light, cmd):
            return self.__trigger(light, cmd)
    
    def activateSensorThreshold(self, sensorID):
        if sensorID.lower() == 'kitchen' or sensorID.lower() == 'sz':
            self.__checkSensor = sensorID
        else:
            logging.warn(str(sensorID) + " is not a valid Sensor ID")
            
    def deactivateSensorThreshold(self):
        self.__checkSensor = None
            

if __name__ == '__main__':
    FORMAT = '%(asctime)s %(module)s:%(funcName)s:%(lineno)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    args = parseArgs()
    trigger = Trigger()
    if args.sensor:
        trigger.activateSensorThreshold(args.sensor)
    else:
        trigger.deactivateSensorThreshold()
        
    if (args.on):
        trigger.triggerLight(args.lightID, 1)
    elif (args.off):
        trigger.triggerLight(args.lightID, 0)
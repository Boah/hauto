'''
Created on 16.05.2016

@author: mirko
'''

from trigger.trigger import Trigger
from argumentParser.argumentParser import parseArgs
from trigger.lightDef import lightDef
from sensorClient.sensorClient import LightSensorClient

import logging

if __name__ == '__main__':
    FORMAT = '%(asctime)s %(module)s:%(funcName)s:%(lineno)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    args = parseArgs()
    trigger = Trigger()
    ldefs = lightDef()
    lclient = LightSensorClient()
    if (args.on):
        if not args.sensor:
            trigger.trigger(ldefs.getLightID(args.lightID), 1)
        elif args.sensor.lower() == 'sz':
            lval = lclient.getLightValueFromServer('192.168.0.88')
            logging.info("Measured: " + str(lval))
            if lval < 2:
                trigger.trigger(ldefs.getLightID(args.lightID), 1)
        elif args.sensor.lower() == 'kitchen':
            if lclient.getLightValueFromServer('192.168.0.11') < 2:
                trigger.trigger(ldefs.getLightID(args.lightID), 1)
    else:
        trigger.trigger(ldefs.getLightID(args.lightID), 0)

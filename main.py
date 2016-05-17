'''
Created on 16.05.2016

@author: mirko
'''

from trigger.trigger import Trigger
from argumentParser.argumentParser import parseArgs
from trigger.lightDef import lightDef

import logging

if __name__ == '__main__':
    FORMAT = '%(asctime)s %(module)s:%(funcName)s:%(lineno)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    args = parseArgs()
    trigger = Trigger()
    ldefs = lightDef()
    if (args.on):
        trigger.trigger(ldefs.getLightID(args.lightID), 1)
    else:
        trigger.trigger(ldefs.getLightID(args.lightID), 0)

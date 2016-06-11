'''
Created on 16.05.2016

@author: mirko
'''

from trigger.trigger import Trigger
from argumentParser.argumentParser import parseArgs
from scheduler.scheduler import Scheduler
from interfaces.socketInterface import SocketInterface

import logging
from scheduler.schedulerDataContainer import SchedulerDataContainer

if __name__ == '__main__':
    FORMAT = '%(levelname)s: %(asctime)s %(module)s:%(funcName)s:%(lineno)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    args = parseArgs()
    trigger = Trigger(args.sensor)

    if not args.daemon:
        if (args.on):
            trigger.triggerLight(args.lightID, 1)
        elif (args.off):
            trigger.triggerLight(args.lightID, 0)
    else:
        # Try to restore scheduler Data from File
        if SchedulerDataContainer().fromFile("/var/log/schedData"):
            logging.info("Restored Scheduler Data")
        else:
            logging.info("Could not restore scheduler Data")
        
        scheduler = Scheduler()
        scheduler.run_continuously(30)
        socketInterface = SocketInterface()
        socketInterface.startLightServer()
        pass
        

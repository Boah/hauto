'''
Created on 18.05.2016

@author: mirko
'''

class LightStatusStore(object):
    '''
    classdocs
    '''
    __statusWZ1 = False
    __statusWZ2 = False
    __statusSZ1 = False

    def __init__(self, params):
        '''
        Constructor
        '''
        
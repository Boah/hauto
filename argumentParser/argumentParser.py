'''
Created on 17.05.2016

@author: mirko
'''
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='Control lights')
    parser.add_argument('-l', '--light', action='store')
    parser.add_argument('-d', '--daemon', action='store_true')
    parser.add_argument('-1', '--on', action='store_true')
    parser.add_argument('-0', '--off', action='store_true')
    parser.add_argument('-s', '--sensor', action='store')
    args = parser.parse_args()
    if (not args.on and not args.off) or (args.on and args.off):
        args.on = True
        args.off = False
    return args
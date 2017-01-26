#!/usr/bin/python

import sys
import math
from random import randint, seed
from towerState import TowerState

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

Modes = Enum    ([  "TEST_ALL",

                    "TEST_ADD_REMOVE",
                    "TEST_FILE_LOAD",
                    "TEST_EXPAND_STATE",
                    "TEST_TIMING"
                ])

Heuristics = Enum   ([  "HEURISTIC_1",
                        "HEURISTIC 2",
                    ])


class Settings(object):
    def __init__(self):
        self.VERBOSE = True
        self.MODE = Modes.TEST_ALL
        self.FILENAME = "perms-9.txt"
        self.NMAX = 10000


def Usage(settings):
    print '\n*** Usage:\nusage to be determined\n'

def parseArgs(settings):
    #FIXME implement this once all our settings are known

    print "***** Running the Towers of Corvallis with the following settings"
    print "***** VERBOSE = \t", settings.VERBOSE
    print "***** MODE = \t\t", settings.MODE
    print "***** FILENAME = \t" + settings.FILENAME

    print ""
    return True

def loadProblemsFromFile(filename):
    problems = []
    lines = [line.rstrip('\n') for line in open(filename)]

    for line in lines[1:]: # use slicing to chop off the first line, since it is header
        problems = problems + [TowerState.createTowerFromLine(line)]
    return problems

def testAll(settings):

    print "***** Testing ALL MODES"
    testAddRemove(settings)
    testFileLoad(settings)
    testExpandState(settings)
    testTiming(settings)

def testAddRemove(settings):
    seed(567)
    print "\n***** Testing Add and Remove"

    tower = TowerState()
    tower.consolePrint()

    for i in range(0,10):
        tower.addDisc(randint(0,2),randint(0,100))
        tower.consolePrint()

    print '\n\n'
    tower.removeDisc(0)
    tower.consolePrint()

    tower.removeDisc(2)
    tower.consolePrint()

    tower.removeDisc(1)
    tower.consolePrint()

    tower.removeDisc(2)
    tower.consolePrint()

    tower.removeDisc(0)
    tower.consolePrint()

def testFileLoad(settings):
    print "\n***** Testing File Load"
    problemSet = loadProblemsFromFile(settings.FILENAME)
    for problem in problemSet:
        problem.consolePrint()



def testExpandState(settings):
    print "\n***** Testing State Expansion, Initial State"
    seed(6503)
    tower = TowerState()
    for i in range(0,10):
        tower.addDisc(randint(0,2),randint(0,100))
    tower.consolePrint()

    print "After expansion"
    expanded =  tower.expandState()
    for i in expanded:
        i.consolePrint()

    print "\nnext initial state"
    tower = TowerState()
    for i in range(0, 2):
        tower.addDisc(randint(0, 2), randint(0, 100))
    tower.consolePrint()

    print "After expansion"
    expanded = tower.expandState()
    for i in expanded:
        i.consolePrint()

def testTiming(settings):

    print "\n***** Testing Timing"
    beamWidths = [5, 10, 15, 20, 25, 50, 100] #FIXME handle infinity uniformly somehow?
    heuristicFunctions = [1,2]
    problemSizes = [4, 5, 6, 7]

    for bw in beamWidths:
        for hf in heuristicFunctions:
            for ps in problemSizes:
                problemSet = loadProblemsFromFile("perms-"+ str(ps) + ".txt")
                print "\nBeam Width : " + str(bw)
                print "Heuristic Function : " + str(hf)
                print "Problem Size :" + str(ps)
                print "Solution Length \t Nodes Expanded \t Heuristic Eval Time \t Total Time \t Heuristic"
                for problem in problemSet:
                    data = problem.performSearch(settings.NMAX)
                    print str(data[0]) + "\t" + str(data[1]) + "\t" + str(data[2]) + "\t" + str(data[3]) + "\t"

'''
     For beam widths 5, 10, 15, 20, 25, 50, 100, infty
        For each heuristic function h,
          For at least 4 different sizes (number of disks)
             For each of the 20 problems p, Solve p using h or until NMAX nodes are expanded.
                Record the solution length if successful, the number of nodes expanded, and the total CPU time spent on evaluating the heuristic and on solving the whole problem.
'''

'''
main script
'''
settings = Settings()
if not parseArgs(settings):
    Usage
    quit()

elif settings.MODE == Modes.TEST_ALL:
    testAll(settings)


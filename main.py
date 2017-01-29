#!/usr/bin/python

import sys
import math
from random import randint, seed
from towerState import TowerState, loadProblemsFromFile
import towerUnitTests

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

Modes = Enum    ([  "TIMING",       # this is the main mode, timing a bunch of functions

                    # these are all unit tests
                    "TEST_ADD_REMOVE",
                    "TEST_FILE_LOAD",
                    "TEST_EXPAND_STATE",
                    "TEST_BFS",
                    "TEST_DFS",
                    "TEST_A_STAR",
                    "TEST_BEAM",

                    "TEST_ALL"
                ])

SearchFns = Enum   ([           'BFS',
                                'DFS',
                                'A_STAR',
                                'BEAM'
                    ])
searchFnDict = {
    'BFS': TowerState.performBFSearch,
    'DFS': TowerState.performDFSearch,
    'A_STAR': TowerState.performAStarSearch,
    'BEAM': TowerState.performBeamSearch,
}

HeuristicFns = Enum ([          'ADMISSIBLE',
                                'INADMISSIBLE'
                    ])
heuristicFnDict = {
    'ADMISSIBLE': TowerState.evaluateInadmissible,
    'INADMISSIBLE': TowerState.evaluateAdmissible,
}

class Settings(object):
    def __init__(self):
        self.VERBOSE = True
        self.MODE = Modes.TEST_ALL
        self.FILENAME = "perms-9.txt"
        self.NMAX = 10000
        self.beamWidths = [5]  # , 10, 15, 20, 25, 50, 100] #FIXME handle infinity uniformly somehow?
        self.searchFns = [SearchFns.BFS, SearchFns.DFS, SearchFns.A_STAR, SearchFns.BEAM]
        self.heuristicFns = [HeuristicFns.ADMISSIBLE, HeuristicFns.INADMISSIBLE]
        self.problemSizes = [4]  # , 5, 6, 7]


def Usage(settings):
    #FIXME implement this once our usage is known
    print '\n*** Usage:\nusage to be determined\n'

def parseArgs(settings):
    #FIXME implement this once all our settings are known

    print "***** Running the Towers of Corvallis with the following settings"
    print "***** VERBOSE = \t", settings.VERBOSE
    print "***** MODE = \t\t", settings.MODE
    print "***** FILENAME = \t" + settings.FILENAME
    print "***** NMAX = \t" + str(settings.NMAX)
    print "***** BEAM WIDTHS = " + str(settings.beamWidths)
    print "***** SEARCH FNS = " + str(settings.searchFns)
    print "***** HEURISTIC FNS = " + str(settings.heuristicFns)
    print "***** PROBLEM Sizes = " + str(settings.problemSizes)

    print ""
    return True




'''
Pseudocode provided for main timing loop:

     For beam widths 5, 10, 15, 20, 25, 50, 100, infty
        For each heuristic function h,
          For at least 4 different sizes (number of disks)
             For each of the 20 problems p, Solve p using h or until NMAX nodes are expanded.
                Record the solution length if successful, the number of nodes expanded, and the total CPU time spent on evaluating the heuristic and on solving the whole problem.
'''
def computeTiming(settings):
    print "\n***** Testing Timing"
    for sf in settings.searchFns:
        searchFnToCall = searchFnDict[sf]
        for bw in settings.beamWidths:
            for hf in settings.heuristicFns:
                heuristicFnToCall = heuristicFnDict[hf]
                for ps in settings.problemSizes:
                    problemSet = loadProblemsFromFile("perms-" + str(ps) + ".txt")
                    print "\nSearch Function :\t" + str(sf)
                    print "Beam Width :\t" + str(bw)
                    print "Heuristic Function :\t" + str(hf)
                    print "Problem Size :\t" + str(ps)
                    print "Solution Length \t Nodes Expanded \t Heuristic Eval Time \t Total Time \t Heuristic"
                    for problem in problemSet:
                        data = searchFnToCall(problem, settings.NMAX, heuristicFnToCall)
                        print str(data[0]) + "\t" + str(data[1]) + "\t" + str(data[2]) + "\t" + str(data[3]) + "\t"


'''
main script
'''
settings = Settings()
if not parseArgs(settings):
    Usage
    quit()

# Main mode here, computing timing information
elif settings.MODE == Modes.TIMING:
    computeTiming(settings)

# Unit tests for basic operations
elif settings.MODE == Modes.TEST_ADD_REMOVE:
    towerUnitTests.testAddRemove(settings)
elif settings.MODE == Modes.TEST_FILE_LOAD:
    towerUnitTests.testFileLoad(settings)
elif settings.MODE == Modes.TEST_EXPAND_STATE:
    towerUnitTests.testExpandState(settings)

# Unit tests for search Operations
elif settings.MODE == Modes.TEST_BFS:
    towerUnitTests.testBFS(settings)
elif settings.MODE == Modes.TEST_DFS:
    towerUnitTests.testDFS(settings)
elif settings.MODE == Modes.TEST_A_STAR:
    towerUnitTests.testAStarSearch(settings)
elif settings.MODE == Modes.TEST_BEAM:
    towerUnitTests.testBeamSearch(settings)



elif settings.MODE == Modes.TEST_ALL:
    towerUnitTests.testAddRemove(settings)
    towerUnitTests.testFileLoad(settings)
    towerUnitTests.testExpandState(settings)
    towerUnitTests.testBFS(settings)
    towerUnitTests.testDFS(settings)
    towerUnitTests.testAStarSearch(settings)
    towerUnitTests.testBeamSearch(settings)

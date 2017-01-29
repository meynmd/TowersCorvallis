#!/usr/bin/python
import sys
import math
from random import randint, seed
from towerState import TowerState
import towerUnitTests
from searcher import performBFSearch, performDFSearch, performAStarSearch, performBeamSearch
from heuristicFns import evaluateAdmissible, evaluateInadmissible


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

# this enum provides the modes of the program.  Some of them may not be accesible via command line flags
Modes = Enum([
    "TIMING",       # this is the main mode, timing a bunch of functions

    # these are all unit tests
    "TEST_ADD_REMOVE",
    "TEST_EXPAND_STATE",
    "TEST_BFS",
    "TEST_DFS",
    "TEST_A_STAR",
    "TEST_BEAM",

    "TEST_ALL"
    ])

SearchFns = Enum([  'BFS',
                    'DFS',
                    'A_STAR',
                    'BEAM'
                ])
# This dictionary implements the function table for the enum above
searchFnDict = {
    'BFS': performBFSearch,
    'DFS': performDFSearch,
    'A_STAR': performAStarSearch,
    'BEAM': performBeamSearch,
}

HeuristicFns = Enum ([          'ADMISSIBLE',
                                'INADMISSIBLE'
                    ])
heuristicFnDict = {
    'ADMISSIBLE': evaluateAdmissible,
    'INADMISSIBLE': evaluateInadmissible,
}

class Settings(object):
    def __init__(self):
        self.VERBOSE = False
        self.MODE = Modes.TEST_BFS
        self.FILENAME = "perms-3.txt"
        self.NMAX = 10000
        self.beamWidths = [5]  # , 10, 15, 20, 25, 50, 100] #FIXME handle infinity uniformly somehow?
        self.searchFns = [SearchFns.BFS, SearchFns.DFS, SearchFns.A_STAR, SearchFns.BEAM]
        self.heuristicFns = [HeuristicFns.ADMISSIBLE, HeuristicFns.INADMISSIBLE]
        self.problemSizes = [4]  # , 5, 6, 7]


def Usage():
    print '\n*** Usage:\n\t\tmain [-f FILENAME] [-a] [-t] [-v] [-n NMAX]\n'
    print '\t [-f filename] - Sets the file containing problems to FILENAME'
    print '\t [-a] - Mode selection - Runs all unit tests, but not timing'
    print '\t [-t] - Mode selection - Runs timing test'
    print '\t [-v] - Sets output to verbose'
    print '\t [-n NMAX] - Sets the the number of iterations before search is considered failed to NMAX'

def parseArgs(settings):
    argc = len(sys.argv) - 1
    for i in range(1,argc):
        token = sys.argv[i]
        if token == '-f':
            if i + 1 <= argc:
                print "setting filename"
                settings.FILENAME = sys.argv[i+1]
                i += 1
            else:
                print "Insufficient arguments, expected Filename after -f"
                return False
        elif token == '-a':
            settings.MODE = Modes.TEST_ALL
        elif token == '-t':
            settings.MODE = Modes.TIMING
        #FIXME more mode setting commands?
        elif token == '-v':
            settings.VERBOSE = True
        else:
            print "Unknown token : " + token
            return False

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
    Usage()
    quit()

# Main mode here, computing timing information
elif settings.MODE == Modes.TIMING:
    computeTiming(settings)

# Unit tests for basic operations
elif settings.MODE == Modes.TEST_ADD_REMOVE:
    towerUnitTests.testAddRemove(settings)
elif settings.MODE == Modes.TEST_EXPAND_STATE:
    towerUnitTests.testExpandState(settings)

# Unit tests for search Operations
elif settings.MODE == Modes.TEST_BFS:
    performBFSearch(settings)
elif settings.MODE == Modes.TEST_DFS:
    performDFSearch(settings)
elif settings.MODE == Modes.TEST_A_STAR:
    performAStarSearch(settings)
elif settings.MODE == Modes.TEST_BEAM:
    performBeamSearch(settings)



elif settings.MODE == Modes.TEST_ALL:
    towerUnitTests.testAddRemove(settings)
    towerUnitTests.testExpandState(settings)
    performBFSearch(settings)
    performDFSearch(settings)
    performAStarSearch(settings)
    performBeamSearch(settings)

#!/usr/bin/python
import sys
import math
from random import randint, seed
from towerState import TowerState
import unitTests
from searcher import performBFSearch, performAStarSearch, performBeamSearch
import searchState

sys.setrecursionlimit(10000)

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
    "TEST_HEURISTIC",

    # these are all the search tests
    "TEST_BFS",
    "TEST_A_STAR",
    "TEST_BEAM",

    "TEST_ALL"
    ])

SearchFns = Enum([  'BFS',
                    'A_STAR',
                    'BEAM'
                ])
# This dictionary implements the function table for the enum above
searchFnDict = {
    'BFS': performBFSearch,
    'A_STAR': performAStarSearch,
    'BEAM': performBeamSearch,
}

HeuristicFns = Enum ([          'NUM_DISCS_OUT_OF_PLACE',
                                'NUM_DISCS_OUT_OF_PLACE_ALL_PEG',
                                'MANHATTAN_DISTANCE',
                                'MANHATTAN_DISTANCE_ALL_PEG',
                                'WEIGHTED_NUM_DISCS_OUT_OF_PLACE',
                                'WEIGHTED_NUM_DISCS_OUT_OF_PLACE_ALL_PEG',
                                'WEIGHTED_MANHATTAN_DISTANCE',
                                'WEIGHTED_MANHATTAN_DISTANCE_ALL_PEG'
                    ])
heuristicFnDict = {
#    'NUM_DISCS_OUT_OF_PLACE_ALL_PEG'            : searchState.numDiscsOutOfPlaceAllPeg,
    'MANHATTAN_DISTANCE_ALL_PEG'                : searchState.manhattanDistanceAllPeg,
    'WEIGHTED_NUM_DISCS_OUT_OF_PLACE_ALL_PEG'   : searchState.weightedNumDiscsOutOfPlaceAllPeg,
#    'WEIGHTED_MANHATTAN_DISTANCE_ALL_PEG'       : searchState.weightedManhattanDistanceAllPeg
}

class Settings(object):
    def __init__(self):
        self.VERBOSE = False
        self.PRINT_RESULTS = True
        self.MODE = Modes.TEST_BEAM
        self.FILENAME = "perms-6.txt"
        self.NMAX = 500
        self.beamWidth = 50
        self.searchFn = SearchFns.BEAM
        self.heuristicFn =  HeuristicFns.MANHATTAN_DISTANCE_ALL_PEG
                            # HeuristicFns.NUM_DISCS_OUT_OF_PLACE_ALL_PEG
                            # HeuristicFns.MANHATTAN_DISTANCE_ALL_PEG
                            # HeuristicFns.WEIGHTED_MANHATTAN_DISTANCE_ALL_PEG
                            # HeuristicFns.WEIGHTED_NUM_DISCS_OUT_OF_PLACE_ALL_PEG
        self.problemSize = 10


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
    print "***** BEAM WIDTH = " + str(settings.beamWidth)
    print "***** SEARCH FN = " + str(settings.searchFn)
    print "***** HEURISTIC FN = " + str(settings.heuristicFn)
    print "***** PROBLEM Size = " + str(settings.problemSize)

    print ""
    return True


def loadProblemsFromFile(filename):
    problems = []
    lines = [line.rstrip('\n') for line in open(filename)]

    for line in lines[1:]: # use slicing to chop off the first line, since it is header
        problems = problems + [TowerState.createTowerFromLine(line)]
    return problems

'''
Pseudocode provided for main timing loop:

     For beam widths 5, 10, 15, 20, 25, 50, 100, infty
        For each heuristic function h,
          For at least 4 different sizes (number of disks)
             For each of the 20 problems p, Solve p using h or until NMAX nodes are expanded.
                Record the solution length if successful, the number of nodes expanded, and the total CPU time spent on evaluating the heuristic and on solving the whole problem.
'''
def computeTiming(settings):
    print "\n***** Testing Timing, overriding certain flags"
    settings.PRINT_RESULTS = False
    settings.VERBOSE = False
    searchFns = [SearchFns.BEAM, SearchFns.A_STAR]
    beamWidths = [5, 10, 15, 20, 25, 50, 100]
    heuristicFns = [    #HeuristicFns.NUM_DISCS_OUT_OF_PLACE_ALL_PEG,
                        HeuristicFns.MANHATTAN_DISTANCE_ALL_PEG,
                        HeuristicFns.WEIGHTED_NUM_DISCS_OUT_OF_PLACE_ALL_PEG,
                        #HeuristicFns.WEIGHTED_MANHATTAN_DISTANCE_ALL_PEG,
                    ]
    problemSizes = [3,4,5,6,7,8,9,10] #FIXME 8,9,10
    print "Search Function \t Beam Width \t Heuristic \t Problem Size\tFailures\tAvg Solution Depth \t Avg Nodes Expanded \t Avg Heuristic Eval Time \t Avg Total Time\tMax Solution Depth \t Max Nodes Expanded \t Max Heuristic Eval Time \t Max Total Time\tMin Solution Depth \t Min Nodes Expanded \t Min Heuristic Eval Time \t Min Total Time"

    for sf in searchFns:
        searchFnToCall = searchFnDict[sf]
        for bw in beamWidths:
            for hf in heuristicFns:
                heuristicFnToCall = heuristicFnDict[hf]
                for ps in problemSizes:
                    data = []
                    problemSet = loadProblemsFromFile("perms-" + str(ps) + ".txt")

                    for problem in problemSet:
                        data += [searchFnToCall(problem, settings, heuristicFnToCall, bw)]
                        #print "\t" + str(data[-1][0]) + "\t" + str(data[-1][1]) + "\t" + str(data[-1][2]) + "\t" + str(data[-1][3]) + "\t"

                    failures = []
                    successes = []
                    for datum in data:
                        if(datum[4]):
                            successes += [datum]
                        else:
                            failures += [datum]
                    try:
                        solnLengthList, nodesExpandedList, heuristicTimesList, totalTimesList, failuresList = [list(tup) for tup in zip(*successes)]
                    except ValueError:
                        print str(sf) + "\t" + str(bw) + "\t" + str(hf) + "\t" + str(ps) + "\t" + str(len(failures))
                        continue

                    numProblems = len(problemSet)
                    print str(sf) + "\t" + str(bw) + "\t" + str(hf) + "\t" + str(ps) + "\t" + str(len(failures)),
                    print "\t" + str(sum(solnLengthList)/numProblems) + "\t" + str(sum(nodesExpandedList)/numProblems) + "\t" + str(sum(heuristicTimesList)/numProblems) + "\t" + str(sum(totalTimesList)/numProblems),
                    print "\t" + str(max(solnLengthList)) + "\t" + str(max(nodesExpandedList)) + "\t" + str(max(heuristicTimesList)) + "\t" + str(max(totalTimesList)),
                    print "\t" + str(min(solnLengthList)) + "\t" + str(min(nodesExpandedList)) + "\t" + str(min(heuristicTimesList)) + "\t" + str(min(totalTimesList))

            if not searchFnToCall == performBeamSearch:
                break

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
    unitTests.testAddRemove(settings)
elif settings.MODE == Modes.TEST_EXPAND_STATE:
    unitTests.testExpandState(settings)

# if we reached here we will need to load a problem to test with and a heuristic function
problemSet = loadProblemsFromFile(settings.FILENAME)
theProblem = problemSet[0]


theHeuristic = heuristicFnDict[settings.heuristicFn]

if settings.MODE == Modes.TEST_HEURISTIC:
    heuristicFns = [  # HeuristicFns.NUM_DISCS_OUT_OF_PLACE_ALL_PEG,
        HeuristicFns.WEIGHTED_NUM_DISCS_OUT_OF_PLACE_ALL_PEG,
        HeuristicFns.MANHATTAN_DISTANCE_ALL_PEG,
        # HeuristicFns.WEIGHTED_MANHATTAN_DISTANCE_ALL_PEG,
    ]
    print heuristicFns[0]
    unitTests.testHeuristic(settings, problemSet, heuristicFnDict[heuristicFns[0]])
    print
    print heuristicFns[1]
    unitTests.testHeuristic(settings, problemSet, heuristicFnDict[heuristicFns[1]])

# Unit tests for search Operations
elif settings.MODE == Modes.TEST_BFS:
    for i in range(0,len(problemSet)):
        theProblem = problemSet[i]
        performBFSearch(theProblem, settings, theHeuristic, settings.beamWidth)
elif settings.MODE == Modes.TEST_A_STAR:
    for i in range(0,len(problemSet)):
        theProblem = problemSet[i]
        performAStarSearch(theProblem, settings, theHeuristic, settings.beamWidth)
elif settings.MODE == Modes.TEST_BEAM:
    for i in range(0,len(problemSet)):
        theProblem = problemSet[i] 
        performBeamSearch(theProblem, settings, theHeuristic, settings.beamWidth)

if settings.MODE == Modes.TEST_ALL:
    #unitTests.testAddRemove(settings)
    #unitTests.testExpandState(settings)

    performAStarSearch(theProblem, settings, theHeuristic, settings.beamWidth)
    performBeamSearch(theProblem, settings, theHeuristic, settings.beamWidth)
    performBFSearch(theProblem, settings, theHeuristic, settings.beamWidth)

    computeTiming(settings)

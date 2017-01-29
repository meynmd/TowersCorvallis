#!/usr/bin/python
import time
from collections import deque
from towerState import TowerState
from heuristicFns import evaluateAdmissible

def loadProblemsFromFile(filename):
    problems = []
    lines = [line.rstrip('\n') for line in open(filename)]

    for line in lines[1:]: # use slicing to chop off the first line, since it is header
        problems = problems + [TowerState.createTowerFromLine(line)]
    return problems

# this function as defined makes no sense, but it shows the expected order of
# arguments in the tuple returned by the actual searchers
def performBFSearch(settings):
    print "performing Breadth"

    problemSet = loadProblemsFromFile(settings.FILENAME)

    theProblem = problemSet[0]

    totalTimeStart = time.time()

    # FIXME define this
    goalDepth = 0
    nodesExpanded = 0
    heuristicTime = 0

    searchFrontier = deque()
    searchFrontier.append(theProblem)

    loopCounter = 0;

    while len(searchFrontier):
        loopCounter += 1
        if loopCounter > settings.NMAX:
            print "iterations expired, goal not found"
            break
        print "\n\n************** loop iter"
        print "currently " + str(len(searchFrontier)) + " items in the frontier"
        for os in searchFrontier:
            os.consolePrint()
        currentState = searchFrontier[0]
        print "Current solution depth " + str(currentState.solutionDepth)
        if currentState.goalRecognized():
            goalDepth = currentState.solutionDepth
            print "goal found"
            break;
        childStates = currentState.expandState()
        nodesExpanded += 1

        print "printing child states before filtering"
        for cs in childStates:
            cs.solutionDepth += 1
            cs.consolePrint()

        print
        # Filter and add the states
        for cs in childStates:
            duplicateFound = False
            for os in searchFrontier:
                if cs.sameState(os):
                    print "Duplicate found"
                    cs.consolePrint()
                    os.solutionDepth = min(os.solutionDepth, cs.solutionDepth)
                    duplicateFound = True
                    break
            if not duplicateFound:
                print "appending "
                cs.consolePrint()
                searchFrontier.append(cs)
        print "popping left"
        searchFrontier.popleft()

    print "loop ended"
    totalTimeEnd = time.time()

    print "Goal Depth ", goalDepth
    print "Nodes expanded ", nodesExpanded
    print "Heuristic time ", heuristicTime
    print "Total Time ", totalTimeEnd - totalTimeStart

    while(currentState):
        currentState.consolePrint()
        currentState = currentState.predecessor

    return (goalDepth, nodesExpanded, heuristicTime, totalTimeEnd - totalTimeStart)


def performDFSearch(settings):
    # print "performing Depth"
    # FIXME define this
    return (0, 0, 0, 0)


def performAStarSearch(settings):
    print "performing AStar"



    problemSet = loadProblemsFromFile(settings.FILENAME)

    theProblem = problemSet[0]

    totalTimeStart = time.time()

    # FIXME define this
    goalDepth = 0
    nodesExpanded = 0
    heuristicTime = 0

    searchFrontier = deque()
    theProblem.heuristicEstimate = evaluateAdmissible(theProblem)
    searchFrontier.append(theProblem)


    loopCounter = 0;

    while len(searchFrontier):
        loopCounter += 1
        if loopCounter > settings.NMAX:
            print "iterations expired, goal not found"
            break
        print "\n\n************** loop iter"
        print "currently " + str(len(searchFrontier)) + " items in the frontier"
        for os in searchFrontier:
            os.consolePrint()

        #FIXME choose a state in a principled fashion
        currentState = searchFrontier[0]
        for cs in searchFrontier:
            if currentState.heuristicEstimate > cs.heuristicEstimate:
                currentState = cs

        print "Current solution depth " + str(currentState.solutionDepth)
        if currentState.goalRecognized():
            goalDepth = currentState.solutionDepth
            print "goal found"
            break;
        childStates = currentState.expandState()
        nodesExpanded += 1

        print "printing child states before filtering"
        for cs in childStates:
            cs.solutionDepth += 1
            cs.consolePrint()

        print
        # Filter and add the states
        for cs in childStates:
            duplicateFound = False
            for os in searchFrontier:
                if cs.sameState(os):
                    print "Duplicate found"
                    cs.consolePrint()
                    os.solutionDepth = min(os.solutionDepth, cs.solutionDepth)
                    duplicateFound = True
                    break
            if not duplicateFound:
                print "appending "
                cs.consolePrint()
                #FIXME evaluate heuristic
                cs.heuristicEstimate = evaluateAdmissible(cs)
                searchFrontier.append(cs)
        print "popping left"
        #FIXME remove in a more principled fashion
        searchFrontier.remove(currentState)

    print "loop ended"
    totalTimeEnd = time.time()

    print "Goal Depth ", goalDepth
    print "Nodes expanded ", nodesExpanded
    print "Heuristic time ", heuristicTime
    print "Total Time ", totalTimeEnd - totalTimeStart

    while (currentState):
        currentState.consolePrint()
        currentState = currentState.predecessor

    return (goalDepth, nodesExpanded, heuristicTime, totalTimeEnd - totalTimeStart)


def performBeamSearch(settings):
    # print "performing Beam"
    # FIXME define this
    return (0, 0, 0, 0)

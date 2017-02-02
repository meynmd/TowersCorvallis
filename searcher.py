#!/usr/bin/python
import time
from collections import deque
from towerState import TowerState
import searchState
from searchState import SearchState


def performBFSearch(initialState, settings, heuristicFn):
    if settings.VERBOSE: print "performing regular Breadth-First Search"
    totalTimeStart = time.time()

    # FIXME define a measurement struct?
    goalDepth = 0
    nodesExpanded = 0
    heuristicTime = 0

    searchFrontier = deque()
    initialSearchState = SearchState(initialState)
    searchFrontier.append(initialSearchState)

    loopCounter = 0;
    while len(searchFrontier):
        loopCounter += 1

        # Cleverly choose the first element of the queue
        currentState = searchFrontier[0]

        # Check to see if we are done
        if loopCounter > settings.NMAX:
            if settings.VERBOSE: print "iterations expired, goal not found"
            break
        if currentState.tower.goalRecognized():
            goalDepth = currentState.solutionDepth
            if settings.VERBOSE: print "goal found"
            break;

        # Perform expansion of the current state
        nodesExpanded += 1
        childStates = currentState.tower.expandState()
        childSearchStates = []
        for cs in childStates:
            childSearchStates.append(SearchState(cs, currentState))

        if settings.VERBOSE:
            print "\n\n************** loop iter"
            print "currently " + str(len(searchFrontier)) + " items in the frontier"
            for state in searchFrontier:
                print state
            print "Current solution depth " + str(currentState.solutionDepth)
            print "printing child states before filtering"

            for cs in childSearchStates:
                print cs

        # Filter and add the states
        for cs in childSearchStates:
            duplicateFound = False
            for os in searchFrontier:
                if cs.tower.sameState(os.tower):
                    if settings.VERBOSE:  print "Duplicate found", cs
                    os.solutionDepth = min(os.solutionDepth, cs.solutionDepth)
                    duplicateFound = True
                    break
            if not duplicateFound:
                searchFrontier.append(cs)
                if settings.VERBOSE:  print "appending ", cs

        #remember to remove the item we chose (cleverly, the first item in the list)
        searchFrontier.popleft()

    totalTimeEnd = time.time()

    if settings.VERBOSE:
        print "Goal Depth ", goalDepth
        print "Nodes expanded ", nodesExpanded
        print "Heuristic time ", heuristicTime
        print "Total Time ", totalTimeEnd - totalTimeStart

    while(currentState):
        if settings.VERBOSE: print currentState
        currentState = currentState.predecessor

    return (goalDepth, nodesExpanded, heuristicTime, totalTimeEnd - totalTimeStart)


def performDFSearch(initialState, settings, heuristicFn):
    if settings.VERBOSE: print "performing Depth"

    # FIXME define this
    print " DFS SEARCH NOT WRITTEN YET"
    return (0, 0, 0, 0)


def performAStarSearch(initialState, settings, heuristicFn):
    if settings.VERBOSE: print "performing AStar"
    totalTimeStart = time.time()

    # FIXME define a measurement struct?
    goalDepth = 0
    nodesExpanded = 0
    heuristicTime = 0

    searchFrontier = deque()
    initialSearchState = SearchState(initialState)
    heuristicFn(initialSearchState)
    searchFrontier.append(initialSearchState)

    goalState = None
    prevState = None
    loopCounter = 0
    while len(searchFrontier):
        loopCounter += 1

        # Choose a state in a principled fashion
        currentState = searchFrontier[0]
        for cs in searchFrontier:
            if currentState.heuristicEstimate > cs.heuristicEstimate:
                currentState = cs

        # Check to see if we are done ( a little different from BFS)
        if loopCounter > settings.NMAX:
            if settings.VERBOSE: print "iterations expired, goal not found"
            break
        if currentState.tower.goalRecognized():
            goalState = currentState
        if goalState:
            lowestHeuristic = goalState.heuristicEstimate
            for os in searchFrontier:
                if os.heuristicEstimate < lowestHeuristic:
                    lowestHeuristic = os.heuristicEstimate
            # if this test fails, there are still promising options to expand in the frontier
            if lowestHeuristic == goalState.heuristicEstimate:
                goalDepth = goalState.solutionDepth
                if settings.VERBOSE: print "goal found"
                break;

        # Perform expansion of the current state
        nodesExpanded += 1
        childStates = currentState.tower.expandState()
        childSearchStates = []
        for cs in childStates:
            childSearchStates.append(SearchState(cs, currentState))

        if settings.VERBOSE:
            print "\n\n************** loop iter ", loopCounter
            print "currently " + str(len(searchFrontier)) + " items in the frontier"
            for state in searchFrontier:
                print state
            print "Current solution depth " + str(currentState.solutionDepth)
            print "printing child states before filtering"

            for cs in childSearchStates:
                print cs

        # Filter and add the states
        for cs in childSearchStates:
            if prevState and cs.tower.sameState(prevState.tower):
                if settings.VERBOSE:
                    print "LOOPING Duplicate found", cs
                continue
            duplicateFound = False
            for os in searchFrontier:
                if cs.tower.sameState(os.tower):
                    if settings.VERBOSE:  print "Duplicate found", cs
                    os.solutionDepth = min(os.solutionDepth, cs.solutionDepth)
                    duplicateFound = True
                    break
            if not duplicateFound:
                heuristicFn(cs)
                searchFrontier.append(cs)
                if settings.VERBOSE:  print "appending ", cs

        # remove in a more principled fashion
        prevState = currentState
        searchFrontier.remove(currentState)

    totalTimeEnd = time.time()

    if settings.VERBOSE:
        print "*********** Performance Summary"
        print "Goal Depth ", goalDepth
        print "Nodes expanded ", nodesExpanded
        print "Heuristic time ", heuristicTime
        print "Total Time ", totalTimeEnd - totalTimeStart

    while(currentState):
        if settings.VERBOSE: print currentState
        currentState = currentState.predecessor

    return (goalDepth, nodesExpanded, heuristicTime, totalTimeEnd - totalTimeStart)


def performBeamSearch(initialState, settings, heuristicFn):
    if settings.VERBOSE: print "performing Beam"

    # FIXME define this
    print " BEAM SEARCH NOT WRITTEN YET"
    return (0, 0, 0, 0)

#!/usr/bin/python
import time
from collections import deque
from towerState import TowerState
import searchState
from searchState import SearchState


def performBFSearch(initialState, settings, heuristicFn, unusedArg):
    if settings.VERBOSE: print "performing regular Breadth-First Search"
    totalTimeStart = time.time()

    goalDepth = 0
    nodesExpanded = 0
    heuristicTime = 0

    searchFrontier = deque()
    exploredStates = deque()
    initialSearchState = SearchState(initialState)
    searchFrontier.append(initialSearchState)
    exploredStates.append(initialSearchState)

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

        '''
        if settings.VERBOSE:
            print "\n\n************** loop iter"
            print "currently " + str(len(searchFrontier)) + " items in the frontier"
            for state in searchFrontier:
                print state
            print "Current solution depth " + str(currentState.solutionDepth)
            print "printing child states before filtering"

            for cs in childSearchStates:
                print cs
        '''

        # Filter and add the states
        for cs in childSearchStates:
            duplicateFound = False
            for os in exploredStates:
                if cs.tower.sameState(os.tower):
                    os.solutionDepth = min(os.solutionDepth, cs.solutionDepth)
                    duplicateFound = True
                    break
            if not duplicateFound:
                searchFrontier.append(cs)
                exploredStates.append(cs)

        #remember to remove the item we chose (cleverly, the first item in the list)
        searchFrontier.popleft()

    totalTimeEnd = time.time()

    if settings.PRINT_RESULTS:
        print "Goal Depth ", goalDepth
        print "Nodes expanded ", nodesExpanded
        print "Heuristic time ", heuristicTime
        print "Total Time ", totalTimeEnd - totalTimeStart

    while(currentState):
        if settings.PRINT_RESULTS: print currentState
        currentState = currentState.predecessor

    return (goalDepth, nodesExpanded, heuristicTime, totalTimeEnd - totalTimeStart)

def performAStarSearch(initialState, settings, heuristicFn, unusedArg):
    if settings.VERBOSE: print "performing AStar"
    totalTimeStart = time.time()

    goalDepth = 0
    nodesExpanded = 0
    heuristicTime = 0

    searchFrontier = deque()
    exploredStates = deque()
    initialSearchState = SearchState(initialState)
    heuristicTime += heuristicFn(initialSearchState)
    searchFrontier.append(initialSearchState)
    exploredStates.append(initialSearchState)

    goalState = None
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
            if settings.VERBOSE: print settings.NMAX, "iterations expired, goal not found"
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

        '''
        if settings.VERBOSE:
            print "\n************** loop iter ", loopCounter,
            print " currently " + str(len(searchFrontier)) + " items in the frontier",
            for state in searchFrontier:
                print state
            print "Current solution depth " + str(currentState.solutionDepth)
            print "printing child states before filtering"

            for cs in childSearchStates:
                print cs
        '''

        # Filter and add the states
        for cs in childSearchStates:
            duplicateFound = False
            for os in exploredStates:
                if cs.tower.sameState(os.tower):
                    os.solutionDepth = min(os.solutionDepth, cs.solutionDepth)
                    duplicateFound = True
                    break
            if not duplicateFound:
                heuristicTime += heuristicFn(cs)
                searchFrontier.append(cs)
                exploredStates.append(cs)

        searchFrontier.remove(currentState)

    totalTimeEnd = time.time()

    if settings.PRINT_RESULTS:
        print "*********** Performance Summary"
        print "Goal Depth ", goalDepth
        print "Nodes expanded ", nodesExpanded
        print "Heuristic time ", heuristicTime
        print "Total Time ", totalTimeEnd - totalTimeStart

    while(currentState):
        if settings.PRINT_RESULTS: print currentState
        currentState = currentState.predecessor

    return (goalDepth, nodesExpanded, heuristicTime, totalTimeEnd - totalTimeStart)


def performBeamSearch(initialState, settings, heuristicFn, beamWidth):
    if settings.VERBOSE: print "performing Beam"
    totalTimeStart = time.time()

    goalDepth = 0
    nodesExpanded = 0
    heuristicTime = 0

    searchFrontier = []
    exploredStates = deque()
    initialSearchState = SearchState(initialState)
    heuristicTime += heuristicFn(initialSearchState)
    searchFrontier += [initialSearchState]
    exploredStates.append(initialSearchState)

    goalState = None
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
            if settings.VERBOSE: print settings.NMAX, "iterations expired, goal not found"
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
            print "\n************** loop iter ", loopCounter,
            print " currently " + str(len(searchFrontier)) + " items in the frontier",
            for state in searchFrontier:
                print state
            print "Current solution depth " + str(currentState.solutionDepth)
            print "printing child states before filtering"

            for cs in childSearchStates:
                print cs


        # Filter and add the states
        for cs in childSearchStates:
            duplicateFound = False
            for os in exploredStates:
                if cs.tower.sameState(os.tower):
                    os.solutionDepth = min(os.solutionDepth, cs.solutionDepth)
                    duplicateFound = True
                    break
            if not duplicateFound:
                heuristicTime += heuristicFn(cs)
                searchFrontier += [cs]
                exploredStates.append(cs)

        searchFrontier.remove(currentState)

        #prune things that are not within the beam
        searchFrontier.sort()
        searchFrontier = searchFrontier[0:beamWidth]

    totalTimeEnd = time.time()

    if settings.PRINT_RESULTS:
        print "*********** Performance Summary"
        print "Goal Depth ", goalDepth
        print "Nodes expanded ", nodesExpanded
        print "Heuristic time ", heuristicTime
        print "Total Time ", totalTimeEnd - totalTimeStart

    while(currentState):
        if settings.PRINT_RESULTS: print currentState
        currentState = currentState.predecessor

    return (goalDepth, nodesExpanded, heuristicTime, totalTimeEnd - totalTimeStart)


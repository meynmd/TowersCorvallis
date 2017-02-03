# !/usr/bin/python
import time

import towerState

class SearchState(object):
    def __init__(self, tower, parent=None):
        if parent:
            self.solutionDepth = parent.solutionDepth + 1
        else:
            self.solutionDepth = 0
        self.predecessor = parent
        self.heuristicEstimate = -1
        self.tower = tower

    def __str__(self):
        return "d: " + str(self.solutionDepth) + " h:\t" + str(self.heuristicEstimate) + "\t" +str(self.tower)

    def __repr__(self):
        return str(self)

    def __cmp__(self, other):
        return cmp(self.heuristicEstimate, other.heuristicEstimate)

def numDiscsOutOfPlace(searchState):
    start = time.time()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # count occurences of discs not being in the proper order on the goal post
    for i in range(0, pegSize):
        cost += int(goalPeg[i] > goalPeg[i-1])

    searchState.heuristicEstimate = cost
    end = time.time()
    return end - start

def numDiscsOutOfPlaceAllPeg(searchState):
    start = time.time()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # count occurences of discs not being in the proper order on the goal post
    for i in range(0, pegSize):
        cost += 2*int(goalPeg[i] > goalPeg[i-1])

    # count how many discs are on the wrong post
    for thisPeg in searchState.tower.pegs:
        if not thisPeg == goalPeg:
            cost += len(thisPeg)
    searchState.heuristicEstimate = cost
    end = time.time()
    return end - start

def manhattanDistance(searchState):
    start = time.time()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # compute error between the expected disc and the disc we have, then double it
    # since each of these discs must be moved twice
    for i in range(0, pegSize):
        expectedDisc = searchState.tower.maxDiscSize - i
        cost += 2*abs(goalPeg[i] - expectedDisc)

    searchState.heuristicEstimate = cost
    end = time.time()
    return end - start

def manhattanDistanceAllPeg(searchState):
    start = time.time()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # compute error between the expected disc and the disc we have, then double it
    # since each of these discs must be moved twice
    for i in range(0, pegSize):
        expectedDisc = searchState.tower.maxDiscSize - i
        cost += 2*abs(goalPeg[i] - expectedDisc)

    # Same process for other posts, but prefer reverse order, so expected disc is just i
    # here we will add 1 to the cost, since even if the discs are in perfect reverse order
    # each disc must be moved once to return to goal state
    for thisPeg in searchState.tower.pegs:
        if not thisPeg == goalPeg:
            for i in range(0, len(thisPeg)):
                cost += abs(thisPeg[i] - i) + 1

    searchState.heuristicEstimate = cost
    end = time.time()
    return end - start

def weightedNumDiscsOutOfPlace(searchState):
    start = time.time()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # count occurences of discs not being in the proper order on the goal post
    for i in range(0, pegSize):
        weight = float(pegSize - i + 1) / float(pegSize)
        cost += weight*float(goalPeg[i] > goalPeg[i-1])

    searchState.heuristicEstimate = cost
    end = time.time()
    return end - start

def weightedNumDiscsOutOfPlaceAllPeg(searchState):
    start = time.time()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # count occurences of discs not being in the proper order on the goal post
    for i in range(0, pegSize):
        weight = float(pegSize - i + 1) / float(pegSize)
        cost += weight*2*float(goalPeg[i] > goalPeg[i-1])

    # count how many discs are on the wrong post
    for thisPeg in searchState.tower.pegs:
        if not thisPeg == goalPeg:
            cost += len(thisPeg)
    searchState.heuristicEstimate = cost
    end = time.time()
    return end - start

def weightedManhattanDistance(searchState):
    start = time.time()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # compute error between the expected disc and the disc we have, then double it
    # since each of these discs must be moved twice
    for i in range(0, pegSize):
        weight = float(pegSize - i + 1) / float(pegSize)
        expectedDisc = searchState.tower.maxDiscSize - i
        cost += 2*weight*abs(goalPeg[i] - expectedDisc)

    searchState.heuristicEstimate = cost
    end = time.time()
    return end - start

def weightedManhattanDistanceAllPeg(searchState):
    start = time.time()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # compute error between the expected disc and the disc we have, then double it
    # since each of these discs must be moved twice
    for i in range(0, pegSize):
        weight = float(pegSize - i + 1) / float(pegSize)
        expectedDisc = searchState.tower.maxDiscSize - i
        cost += 2*weight*abs(goalPeg[i] - expectedDisc)

    # Same process for other posts, but prefer reverse order, so expected disc is just i
    # here we will add 1 to the cost, since even if the discs are in perfect reverse order
    # each disc must be moved once to return to goal state
    for thisPeg in searchState.tower.pegs:
        if not thisPeg == goalPeg:
            thisPegSize = len(thisPeg)
            for i in range(0, thisPegSize):
                weight = float(thisPegSize - i + 1) / float(thisPegSize)
                cost += weight*(abs(thisPeg[i] - i) + 1)

    searchState.heuristicEstimate = cost
    end = time.time()
    return end - start
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
        return cmp(self.heuristicEstimate + self.solutionDepth, other.heuristicEstimate + other.solutionDepth)

# HEURISTIC 1a for report purposes
def numDiscsOutOfPlaceAllPeg(searchState):
    start = time.clock()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # compute error between the expected disc and the disc we have, then double it
    # since each of these discs must be moved twice
    for i in range(0, pegSize):
        expectedDisc = searchState.tower.maxDiscSize - i
        cost += 2 * int(bool(abs(goalPeg[i] - expectedDisc)))

    # count how many discs are on the wrong post
    for thisPeg in searchState.tower.pegs:
        if not thisPeg == goalPeg:
            cost += len(thisPeg)

    searchState.heuristicEstimate = cost
    end = time.clock()
    return end - start

# never mind...
def badManhattanDistanceAllPeg(searchState):
    start = time.clock()
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
    end = time.clock()
    return end - start


# heuristic fn 2a: "augmented" manhattan distance
def manhattanDistanceAllPeg(searchState):
    start = time.clock()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # start at bottom, no cost until we see a disc out of order
    # compute error between the expected disc and the disc we have, then double it
    # since each of these discs must be moved twice
    isInOrder = True
    for i in range(0, pegSize):
        expectedDisc = searchState.tower.maxDiscSize - i
        
        #cost += 2*abs(goalPeg[i] - expectedDisc)

        isInOrder = isInOrder and (goalPeg[i] == expectedDisc)
        if not isInOrder:	
            addedCost = 2 + abs(goalPeg[i] - expectedDisc)
            #print '\t\tnot in order: cost += ' + str(addedCost)
	    cost += addedCost

    for thisPeg in searchState.tower.pegs:
        if not thisPeg == goalPeg:
            for i in range(0, len(thisPeg)):
	    	for j in range(i, len(thisPeg)):
		    dP = thisPeg[i] - thisPeg[j]
		    if dP > 0:
		        cost += dP
                cost += 1



    #print '*******\nreturning cost ' + str(cost) + '\n****************'

    searchState.heuristicEstimate = cost
    end = time.clock()
    return end - start


# heuristic fn 2b: weighted "augmented" manhattan distance
def weightedManhattanDistanceAllPeg(searchState):
    start = time.clock()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # start at bottom, no cost until we see a disc out of order
    # compute error between the expected disc and the disc we have, then double it
    # since each of these discs must be moved twice
    isInOrder = True
    for i in range(0, pegSize):
        expectedDisc = searchState.tower.maxDiscSize - i
        if pegSize > 0:
            weight = float(pegSize - i + 1) / float(pegSize)
        else:
	    weight = 0
	#cost += 2*abs(goalPeg[i] - expectedDisc)

        weight += 1

        isInOrder = isInOrder and (goalPeg[i] == expectedDisc)
        if not isInOrder:	
            addedCost = 2 + abs(goalPeg[i] - expectedDisc)
            #print '\t\tnot in order: cost += ' + str(addedCost)
	    cost += weight * addedCost

    for thisPeg in searchState.tower.pegs:
        if not thisPeg == goalPeg:
            for i in range(0, len(thisPeg)):

                if pegSize > 0:
		    weight = float(pegSize - i + 1) / float(pegSize)
                else:
		    weight = 0
		weight += 1
		for j in range(i, len(thisPeg)):
		    dP = thisPeg[i] - thisPeg[j]
		    if dP > 0:
		        cost += weight * dP
                cost += 1



    #print '*******\nreturning cost ' + str(cost) + '\n****************'

    searchState.heuristicEstimate = cost
    end = time.clock()
    return end - start


	



#HEURISTIC 1b for report purposes
def weightedNumDiscsOutOfPlaceAllPeg(searchState):
    start = time.clock()
    cost = 0
    goalPeg = searchState.tower.pegs[0]
    pegSize = len(goalPeg)

    # count occurences of discs not being in the proper order on the goal post
    for i in range(0, pegSize):
        weight = float(pegSize - i ) / float(pegSize)
        expectedDisc = searchState.tower.maxDiscSize - i
        cost += weight* 2 * int(bool(abs(goalPeg[i] - expectedDisc)))

    # Same process for other posts, but prefer reverse order, so expected disc is just i
    # here we will add 1 to the cost, since even if the discs are in perfect reverse order
    # each disc must be moved once to return to goal state
    for thisPeg in searchState.tower.pegs:
        if not thisPeg == goalPeg:
            thisPegSize = len(thisPeg)
            for i in range(0, thisPegSize):
                weight = float(thisPegSize - i + 1) / float(thisPegSize)
                cost += weight*int(bool(abs(thisPeg[i] - i)))

    searchState.heuristicEstimate = cost
    end = time.clock()
    return end - start



# never mind...
def badWeightedManhattanDistanceAllPeg(searchState):
    start = time.clock()
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
    end = time.clock()
    return end - start

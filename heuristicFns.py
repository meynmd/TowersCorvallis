# !/usr/bin/python
import time

import towerState

def evaluateAdmissible(tower):
    #for i in range(0, tower.pegCount):
    print "********** evaluating a heuristic"


    # is a disk where it should be on the left peg
    #

    tower.consolePrint()
    #weight function 1/(length - index)
    # scoring function maxDisc - index - value
    cost = 0
    peg = tower.pegs[0]
    pegSize = len(peg)
    for i in range(0, pegSize):
        weight = float(i+1)/float(pegSize+1)
        positionScore = tower.maxDiscSize - i - peg[i] #float(peg[i])/float(tower.maxDiscSize)
        if not positionScore:
            continue

        cost += 2*(pegSize - i)
        print "current cost :",cost
        print "weight : ", weight
        print "positionScore :", positionScore
        print " i ", i
    return cost



def evaluateInadmissible(tower):
    return
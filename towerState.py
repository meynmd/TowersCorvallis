#!/usr/bin/python

import copy
import time

def loadProblemsFromFile(filename):
    problems = []
    lines = [line.rstrip('\n') for line in open(filename)]

    for line in lines[1:]: # use slicing to chop off the first line, since it is header
        problems = problems + [TowerState.createTowerFromLine(line)]
    return problems

PEG_COUNT = 3

class TowerState(object):
    @classmethod
    def createTowerFromLine(cls, line):
        t = TowerState()
        line = line.split(' ')
        for word in line:
            toAdd = 0
            try:
                toAdd = int(word)
            except ValueError:
                print "Bad token found :" + word + ":"
                print "in Line :"
                print line
                print "end erroneous line"
            t.addDisc(0, toAdd)
        return t

    def __init__(self):
        self.pegs = []
        for i in range(0, PEG_COUNT):
            self.pegs = self.pegs + [[]]

    def addDisc(self, pegIdx, discSize):
        self.pegs[pegIdx] = self.pegs[pegIdx] + [discSize]

    def removeDisc(self, pegIdx):
        if not self.pegs[pegIdx]:
            print 'stack underflow error'
            quit()
        toReturn = self.pegs[pegIdx][-1]
        self.pegs[pegIdx] = self.pegs[pegIdx][0:-1]
        return toReturn

    def consolePrint(self):
        if self.pegs:
            print self.pegs

    def expandState(self):
        # there are 3 choices of peg to remove a disc from in any given state,
        # then there are 2 choices of peg to place the disc on
        # thus, there are the following combinations given pegs A, B, C
        # and defining (X,Y) meaning to remove from peg X and place on peg Y
        # (A,B), (A,C), (B,A), (B,C), (C,A), (C,B), so we have branching factor 6
        childStates = []
        for i in range(0, PEG_COUNT):
            if self.pegs[i]: # if the list is empty, this test will fail
                for j in range(0, PEG_COUNT):
                    if i == j:
                        continue
                    newState = copy.deepcopy(self)
                    toAdd = newState.removeDisc(i)
                    newState.addDisc(j, toAdd)
                    childStates = childStates + [newState]
        return childStates

    def evaluateAdmissible(self):
        heuristicTimeStart = time.time()

        #FIXME define this

        heuristicTimeEnd = time.time()
        return heuristicTimeEnd - heuristicTimeStart

    def evaluateInadmissible(self):
        heuristicTimeStart = time.time()

        # FIXME define this

        heuristicTimeEnd = time.time()
        return heuristicTimeEnd - heuristicTimeStart

    # this function as defined makes no sense, but it shows the expected order of
    # arguments in the tuple returned by the actual searchers
    def performBFSearch(self, NMAX, heuristicFn):
        #print "performing Breadth"
        totalTimeStart = time.time()

        #FIXME define this

        solutionLength = 45
        nodesExpanded = 1032
        heuristicTime = 0

        for i in range(0, 100):
            heuristicTime += heuristicFn(self)

        totalTimeEnd = time.time()

        return (solutionLength, nodesExpanded, heuristicTime, totalTimeEnd - totalTimeStart)

    def performDFSearch(self, NMAX, heuristicFn):
        #print "performing Depth"
        # FIXME define this
        return (0,0,0,0)

    def performAStarSearch(self, NMAX, heuristicFn):
        #print "performing AStar"
        # FIXME define this
        return (0,0,0,0)

    def performBeamSearch(self, NMAX, heuristicFn):
        #print "performing Beam"
        # FIXME define this
        return (0,0,0,0)

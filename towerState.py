#!/usr/bin/python
import copy

class TowerState(object):
    def __init__(self):
        self.pegs = []
        self.maxDiscSize = -1
        self.pegCount = 3 # This should be built so that we can change this parameter easily, analog is adding swap space
        for i in range(0, self.pegCount):
            self.pegs = self.pegs + [[]]

    def __str__(self):
        return str(self.pegs)

    def __repr__(self):
        return str(self)

    @staticmethod
    def createTowerFromLine(line):
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
            if toAdd > t.maxDiscSize:
                t.maxDiscSize = toAdd
        return t


    def addDisc(self, pegIdx, discSize):
        self.pegs[pegIdx] = self.pegs[pegIdx] + [discSize]

    def removeDisc(self, pegIdx):
        if not self.pegs[pegIdx]:
            print 'stack underflow error'
            quit()
        toReturn = self.pegs[pegIdx][-1]
        self.pegs[pegIdx] = self.pegs[pegIdx][0:-1]
        return toReturn

    def goalRecognized(self):
        for i in range(1, self.pegCount):
            if self.pegs[i]:
                return False
        firstPeg = self.pegs[0]
        for i in range(1, len(firstPeg)):
            if firstPeg[i] > firstPeg[i-1]:
                return False
        return True



    def sameState(self, otherState):
        if self.pegCount != otherState.pegCount:
            return False
        for i in range(0,self.pegCount):
            if not len(self.pegs[i]) == len(otherState.pegs[i]):
                return False
            else:
                for j in range(0, len(self.pegs[i])):
                    if not self.pegs[i][j] == otherState.pegs[i][j]:
                        return False
        return True


    def expandState(self):
        # there are 3 choices of peg to remove a disc from in any given state,
        # then there are 2 choices of peg to place the disc on
        # thus, there are the following combinations given pegs A, B, C
        # and defining (X,Y) meaning to remove from peg X and place on peg Y
        # (A,B), (A,C), (B,A), (B,C), (C,A), (C,B), so we have branching factor 6
        childStates = []
        for i in range(0, self.pegCount):
            if self.pegs[i]: # if the list is empty, this test will fail
                for j in range(0, self.pegCount):
                    if i == j:
                        continue
                    newState = copy.deepcopy(self)
                    newState.predecessor = self
                    toAdd = newState.removeDisc(i)
                    newState.addDisc(j, toAdd)
                    childStates = childStates + [newState]
        return childStates

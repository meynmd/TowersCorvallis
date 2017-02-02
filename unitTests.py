# !/usr/bin/python
import sys
import math
from random import randint, seed
from towerState import TowerState
from searchState import SearchState

def testAddRemove(settings):
    print "\n***** Testing Add and Remove"
    tower = TowerState(); print tower

    seed(567)
    for i in range(0,10):
        tower.addDisc(randint(0,2),randint(0,100))
        print tower

    print '\n'
    tower.removeDisc(0); print tower
    tower.removeDisc(2); print tower
    tower.removeDisc(1); print tower
    tower.removeDisc(2); print tower
    tower.removeDisc(0); print tower

def testExpandState(settings):
    print "\n***** Testing State Expansion, Initial State"
    seed(6503)
    tower = TowerState()
    for i in range(0,10):
        tower.addDisc(randint(0,2),randint(0,100))
    print tower

    print "After expansion"
    expanded =  tower.expandState()
    for child in expanded:
        print child

    print "\nnext initial state"
    tower = TowerState()
    for i in range(0, 2):
        tower.addDisc(randint(0, 2), randint(0, 100))
    print tower

    print "After expansion"
    expanded = tower.expandState()
    for child in expanded:
        print child

def testHeuristic(settings, problemSet, theHeuristic):
    print "\n***** Testing a Heuristic"

    for problem in problemSet:
        ss = SearchState(problem)
        theHeuristic(ss)
        print ss

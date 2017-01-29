# !/usr/bin/python
import sys
import math
from random import randint, seed
from towerState import TowerState

def testAddRemove(settings):
    seed(567)
    print "\n***** Testing Add and Remove"

    tower = TowerState()
    tower.consolePrint()

    for i in range(0,10):
        tower.addDisc(randint(0,2),randint(0,100))
        tower.consolePrint()

    print '\n'
    tower.removeDisc(0)
    tower.consolePrint()

    tower.removeDisc(2)
    tower.consolePrint()

    tower.removeDisc(1)
    tower.consolePrint()

    tower.removeDisc(2)
    tower.consolePrint()

    tower.removeDisc(0)
    tower.consolePrint()

def testExpandState(settings):
    print "\n***** Testing State Expansion, Initial State"
    seed(6503)
    tower = TowerState()
    for i in range(0,10):
        tower.addDisc(randint(0,2),randint(0,100))
    tower.consolePrint()

    print "After expansion"
    expanded =  tower.expandState()
    for i in expanded:
        i.consolePrint()

    print "\nnext initial state"
    tower = TowerState()
    for i in range(0, 2):
        tower.addDisc(randint(0, 2), randint(0, 100))
    tower.consolePrint()

    print "After expansion"
    expanded = tower.expandState()
    for i in expanded:
        i.consolePrint()


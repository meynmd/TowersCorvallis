import sys
import math
from random import randint, seed
from towerState import TowerState, loadProblemsFromFile

def testAddRemove(settings):
    seed(567)
    print "\n***** Testing Add and Remove"

    tower = TowerState()
    tower.consolePrint()

    for i in range(0,10):
        tower.addDisc(randint(0,2),randint(0,100))
        tower.consolePrint()

    print 
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

def testFileLoad(settings):
    print "\n***** Testing File Load"
    problemSet = loadProblemsFromFile(settings.FILENAME)
    for problem in problemSet:
        problem.consolePrint()



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

def testBFS(settings):
    print "\n***** Testing BFS"

    #FIXME write this test
    return

def testDFS(settings):
    print "\n***** Testing DFS"

    # FIXME write this test
    return

def testAStarSearch(settings):
    print "\n***** Testing A* Search"

    # FIXME write this test
    return

def testBeamSearch(settings):
    print "\n***** Testing Beam Search"

    # FIXME write this test
    return

from __future__ import division
from random import randint
from CatchRates import catch_rate
from sys import argv
from math import floor, sqrt

# generation 1 calculation method (approximated)
# todo: improve accuracy to original formula if not yet accurate
def gen1(pkmn, hpratio, ball, status):
    if ball == "master": return 1

    if status in ("burn", "poison", "paralyze"):
        statusval = 12
    elif status in ("freeze", "sleep"):
        statusval = 25
    else:
        statusval = 0

    if ball == "great":
        ballval = 8
    else:
        ballval = 12 
    
    ballmod = {"poke":255, "great": 200, "ultra":150}

    p_0 = statusval / (ballmod[ball]+1)
    f = (1/hpratio) * (255*4/ballval)
    p_1 = ((catch_rate[pkmn]+1)/(ballmod[ball]+1)) * ((f+1)/256)

    return min(max(p_0+p_1, 0), 1)

# generation 3 & 4 calculation method
# todo: approximate with hp ratio instead of exact max/current values
# todo: check conditions for Gen 3/4 ball bonuses
def gen3_4(pkmn, hp_max, hp_curr, ball, status):
    ball_bonus = {"poke": 1, "great": 1.5, "ultra": 2, "master": 255}

    if status in ("sleep", "freeze"):
        status_bonus = 2
    elif status in ("paralysis", "burn", "poison"):
        status_bonus = 1.5
    else:
        status_bonus = 1

    a = ((3*hp_max - 2*hp_curr)*catch_rate[pkmn]*ball_bonus[ball]*status_bonus)/(3*hp_max)     
    p = a/255
    return min(max(p, 0), 1)

# test selected calculation method
def testgen1():
    pkmn = argv[1].lower()
    hpratio = float(argv[2])/float(argv[3])
    balltype = argv[4].lower()
    try:
        status = argv[5].lower()
    except:
        status = ""

    probability = gen1(pkmn, hpratio, balltype, status)
    print "Gen 1: Probability is %.6f (%.4f%% chance of success)" % (probability, probability*100)

# test selected calculation method
def testgen3_4():
    pkmn = argv[1].lower()
    hpcur = float(argv[2])
    hpmax = float(argv[3])
    balltype = argv[4].lower()
    try:
        status = argv[5].lower()
    except:
        status = ""

    probability = gen3_4(pkmn, hpmax, hpcur, balltype, status)
    print "Gen 3 & 4: Probability is %.6f (%.4f%% chance of success)" % (probability, probability*100)


testgen1()
testgen3_4() 

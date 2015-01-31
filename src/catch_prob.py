from __future__ import division
from sys import argv
from math import sqrt
from random import randint
from abc import ABCMeta, abstractmethod
from catch_rates import catch_rate as rate
# -*- coding: utf-8 -*-

# these globals represent groups of statuses that confer identical catch 
# chance bonuses across all generations' differing calculation methods (i.e.
# sleeping and frozen Pokemon are always equally easy to catch, and easier to 
# catch than burned, poisoned, or paralyzed pokemon; assuming all other 
# relevant variables are equal).
_TIER_1_STATUSES = ("burn", "poison", "paralyze")
_TIER_2_STATUSES = ("sleep", "freeze")
# standard ball bonuses from Generation 2 on.
# all Gen 1 balls give unconditional bonuses, unlike balls in later generations.
_BALL_BONUS = {"poke": 1, "great": 1.5, "ultra": 2, "master": 255}
_STANDARD_BALLS = _BALL_BONUS.keys()


class CatchCalc(object):
    """Base catch rate calculator; calculation methods vary by generation,
       but are essentially always derived from the same variables.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, p, hp_m, hp_c, b, s="none"):
        self.catchrate = rate[p.lower()]
        self.maxhp = hp_m
        self.currhp = hp_c
        self.ball = b
        self.status = s

    @abstractmethod
    def catch_chance(self):
        pass

    def master_catch(self):
        """Master balls have 100% success rate in all games.
        """
        if self.ball == "master":
            self.p_catch = 1
            return True


class NewGenCalc(CatchCalc):
    """Base calculator for post-Gen 1 games, all of which share much
       more similar catch methods with each other than they do with
       the gen 1 method. 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def __init__(self, p, hp_m, hp_c, b, s="none"):
        super(NewGenCalc, self).__init__(p, hp_m, hp_c, b, s)
    
    def master_catch(self):
        return super(NewGenCalc, self).master_catch()

    @abstractmethod
    def catch_chance(self, t0, t1, t2):
        if self.master_catch(): return
    
        if self.status in _TIER_1_STATUSES:
            status_bonus = t1
        elif self.status in _TIER_2_STATUSES:
            status_bonus = t2
        else:
            status_bonus = t0
        
        if type(self) == Gen2Calc:
            a = max((3 * self.maxhp - 2 * self.currhp) * 
                    min(max(self.catchrate * _BALL_BONUS[self.ball], 1), 255) / 
                    (3*self.maxhp), 1) + status_bonus
        elif type(self) == Gen3_4Calc:
            a = ((3 * self.maxhp - 2*self.currhp) * self.catchrate * 
                  _BALL_BONUS[self.ball] * status_bonus)/(3*self.maxhp)

        self.p_catch = min(max(a/255,0),1)
        
class Gen1Calc(CatchCalc):
    """Generation 1 calculator.
    """    
    def __init__(self, p, hp_c, hp_m, b, s):
        super(Gen1Calc, self).__init__(p, hp_m, hp_c, b, s)

    def catch_chance(self):
        if super(Gen1Calc, self).master_catch(): return     
        
        if self.status in _TIER_1_STATUSES:
            statusval = 12
        elif self.status in _TIER_2_STATUSES:
            statusval = 25
        else:
            statusval = 0

        if self.ball == "great":
            ballval = 8
        else:
            ballval = 12

        ballmod = {"poke": 255, "great": 200, "ultra": 150}
        p_0 = statusval / (ballmod[self.ball]+1)
        hpratio = self.currhp/self.maxhp
        f = (1/hpratio) * (255*4/ballval)
        p_1 = ((self.catchrate+1)/(ballmod[self.ball]+1)) * ((f+1)/256)
        self.p_catch =  min(max(p_0+p_1, 0), 1)


class Gen2Calc(NewGenCalc):    
    """Generation 2 calculator.
    """
    def __init__(self, p, hp_c, hp_m, b, s):
        super(Gen2Calc, self).__init__(p, hp_m, hp_c, b, s)

    def catch_chance(self):
        if super(Gen2Calc, self).master_catch(): return

        # burns, poisoning and paralysis grant no catch chance bonus
        # in generation 2 due to a glitch; hence, status_bonuses[1] eaualing 0
        status_bonuses = (0, 0, 10)            
        super(Gen2Calc, self).catch_chance(*status_bonuses)

   
class Gen3_4Calc(NewGenCalc):    
    """Generation 3 & 4 calculator. 
       Both gens' catch methods are identical.
    """
    def __init__(self, p, hp_c, hp_m, b, s):
        super(Gen3_4Calc, self).__init__(p, hp_m, hp_c, b, s)

    def catch_chance(self):
        if super(Gen3_4Calc, self).master_catch(): return
        status_bonuses = (1, 1.5, 2)   
        super(Gen3_4Calc, self).catch_chance(*status_bonuses)

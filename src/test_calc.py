from CatchProb import *
from CatchRates import catch_rate as rate

pkmn, ball = argv[1].lower(), argv[4].lower()
cur_hp, max_hp = float(argv[2]), float(argv[3])
try:
    status = argv[5].lower()
except:
    status = None

g1 = Gen1Calc(pkmn, cur_hp, max_hp, ball, status)
g1.catch_chance()
print "Gen 1 probability: %.4f (%.4f%% chance of success)" % (g1.p_catch, 100*g1.p_catch)

g2 = Gen2Calc(pkmn, cur_hp, max_hp, ball, status)
g2.catch_chance()
print "Gen 2 probability: %.4f (%.4f%% chance of success)" % (g2.p_catch, 100*g2.p_catch)

g3_4 = Gen3_4Calc(pkmn, cur_hp, max_hp, ball, status)
g3_4.catch_chance()
print "Gen 3/4 probability: %.4f (%.4f%% chance of success)" % (g3_4.p_catch, 100*g3_4.p_catch)


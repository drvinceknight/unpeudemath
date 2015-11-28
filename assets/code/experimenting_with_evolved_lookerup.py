import axelrod as axl
import csv
import random
import copy

max_size = 26  # Max size of tournaments considered
tournaments = min(max_size - 1, 30)  # Number of tournaments of each size to run
repetitions = 10  # Number of repetitions of each tournament

test_strategies = [axl.EvolvedLookerUp, axl.TitForTat, axl.Cooperator, axl.Defector, axl.DoubleCrosser]
strategies = [s() for s in axl.strategies if axl.obey_axelrod(s) and s not in test_strategies]

def rank(strategies, test_strategies=test_strategies, repetitions=10, processes=None):
    """Return the rank of the test_strategy in a tournament with given strats"""
    for s in test_strategies:
        strategies.append(s())
    nbr = len(test_strategies)
    tournament = axl.Tournament(strategies, repetitions=repetitions, processes=-1)
    results = tournament.play()
    return results.ranking[-nbr:], results.wins[-nbr:]

f = open('combined-data', 'w')
csvwrtr = csv.writer(f)

data = []

for size in range(1, max_size):

    row = [size]

    for k in range(tournaments):

        s = random.sample(strategies, size)
        strategy_labels = ";".join([str(st) for st in s])

        trnmt_s = copy.copy(s)
        results = rank(copy.copy(s), test_strategies=test_strategies, repetitions=repetitions)
        row.append([strategy_labels, results[0]] + results[1])


    data.append(row)
    csvwrtr.writerow(row)


f.close()

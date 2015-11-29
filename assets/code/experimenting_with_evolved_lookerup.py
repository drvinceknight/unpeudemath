import axelrod as axl
import csv
import random
import copy

max_size = 25  # Max size of tournaments considered (maximum size of the sample)
tournaments = 20  # Number of tournaments of each size to run (number of samples)
repetitions = 10  # Number of repetitions of each tournament (for a given sample)

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
f_lookerup = open('data-lookerup.csv', 'w')
csvwrtr_lookerup = csv.writer(f_lookerup)
f_titfortat = open('data-titfortat.csv', 'w')
csvwrtr_titfortat = csv.writer(f_titfortat)
f_cooperator = open('data-cooperator.csv', 'w')
csvwrtr_cooperator = csv.writer(f_cooperator)
f_defector = open('data-defector.csv', 'w')
csvwrtr_defector = csv.writer(f_defector)
f_doublcrosser = open('data-doublecrosser.csv', 'w')
csvwrtr_doublcrosser = csv.writer(f_doublcrosser)

data = []
ind_data = [[], [], [], [], []]


for size in range(1, max_size + 1):

    row = [size]
    ind_row = [copy.copy(row) for _ in range(5)]

    for k in range(tournaments):

        s = random.sample(strategies, size)
        strategy_labels = ";".join([str(st) for st in s])

        trnmt_s = copy.copy(s)
        results = rank(copy.copy(s), test_strategies=test_strategies, repetitions=repetitions)
        row.append([strategy_labels, results[0]] + results[1])
        for i, ts in enumerate(test_strategies):
            trnmt_s = copy.copy(s)
            results = rank(copy.copy(s), test_strategies=[ts], repetitions=repetitions)
            ind_row[i].append([strategy_labels, results[0]] + results[1])



    data.append(row)
    csvwrtr.writerow(row)

    csvwrtr_lookerup.writerow(ind_row[0])

    csvwrtr_titfortat.writerow(ind_row[1])

    csvwrtr_cooperator.writerow(ind_row[2])

    csvwrtr_defector.writerow(ind_row[3])

    csvwrtr_doublcrosser.writerow(ind_row[4])

f.close()
f_lookerup.close()
f_titfortat.close()
f_cooperator.close()
f_defector.close()
f_doublcrosser.close()

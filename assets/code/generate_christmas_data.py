import axelrod as axl
import numpy as np
import csv

family = [axl.Cooperator(),
          axl.Defector(),
          axl.Alternator(),
          axl.TitForTat(),
          axl.TwoTitsForTat(),
          axl.Grudger()]

def check_if_end_pop_cooperates(r=3, p=1, s=0, t=5,
                                digits=5, family=family, turns=10000):
    game = axl.Game(r=r, p=p, s=s, t=t)
    christmas = axl.Tournament(family, turns=50, repetitions=1, game=game)
    results = christmas.play()
    evo = axl.Ecosystem(results)
    evo.reproduce(turns)
    last_pop = [round(pop, digits) for pop in evo.population_sizes[-1]]
    return last_pop[1] == last_pop[2] == 0, last_pop

f = open('christmas.csv', 'w')
csvwtr = csv.writer(f)
csvwtr.writerow(['R', 'P', 'S', 'T', 'Promise',
                 'Cooperator',
                 'Defector',
                 'Alternator',
                 'TitForTat',
                 'TwoTitsForTat',
                 'Grudger'])
f.close()

max_t = 100
number_of_t = 15
number_of_r = 15
number_of_p = 15
number_of_s = 15

for t in np.linspace(5, max_t, number_of_t):
    for r in np.linspace(3, t, number_of_r, endpoint=False):
        for p in np.linspace(1, r, number_of_p, endpoint=False):

            data = []
            for s in np.linspace(0, p, number_of_s, endpoint=False):
                promise, pop = check_if_end_pop_cooperates(r=r, p=p, s=s, t=t)

                data.append([r, p, s, t, promise] + pop)

            # Write data every 15 'number_of_s' experiments
            f = open('christmas.csv', 'a')
            csvwtr = csv.writer(f)
            for row in data:
                csvwtr.writerow(row)
            f.close()

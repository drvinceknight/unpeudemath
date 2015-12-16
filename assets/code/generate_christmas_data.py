import axelrod as axl
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

for t in range(5, 101):
    for r in range(3, t):
        for p in range(1, r):
            for s in range(0, p):
                promise, pop = check_if_end_pop_cooperates(r=r, p=p, s=s, t=t)

                f = open('christmas.csv', 'a')
                csvwtr = csv.writer(f)
                csvwtr.writerow([r, p, s, t, promise] + pop)
                f.close()

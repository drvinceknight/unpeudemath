"""
Script to analyse the rock paper scissors lizard tournament I played in class

v 2015-2016
"""
from __future__ import division
import matplotlib.pyplot as plt

def dictplot(D, f, title):
    plt.figure()
    values = [v / sum(list(D.values())) for v in list(D.values())]
    plt.bar(range(len(D)), values, align='center')
    plt.xticks(range(len(D)), D.keys())
    plt.ylabel('Probability')
    plt.title(title)
    plt.savefig(f)

class Player():
    """
    A player
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Match():
    """
    A match corresponds to 3 duels
    """
    def __init__(self, players, duels):
        self.players = players
        self.duels = duels
        self.winner = sorted(self.players, key=lambda x: len([d for d in duels if d.winner == x]))[1]

    def __str__(self):
        return str(self.winner)


class Duel():
    """
    A dual of Rock, Paper, Scissors, Lizard, Spock
    """
    def __init__(self, players, strategies):
        self.players = players
        self.strategies = strategies
        if strategies[0] == strategies[1]:
            self.winner = 'Tie'
            self.winningstrategy = False
            self.losingstrategy = False
        if sorted(strategies) == sorted(['R','P']):
            self.winner = self.players[strategies.index('P')]
            self.winningstrategy = 'P'
            self.losingstrategy = 'R'
        if sorted(strategies) == sorted(['R','Sc']):
            self.winner = self.players[strategies.index('R')]
            self.winningstrategy = 'R'
            self.losingstrategy = 'Sc'
        if sorted(strategies) == sorted(['R','Sp']):
            self.winner = self.players[strategies.index('Sp')]
            self.winningstrategy = 'Sp'
            self.losingstrategy = 'R'
        if sorted(strategies) == sorted(['R','L']):
            self.winner = self.players[strategies.index('R')]
            self.winningstrategy = 'R'
            self.losingstrategy = 'L'
        if sorted(strategies) == sorted(['L','P']):
            self.winner = self.players[strategies.index('L')]
            self.winningstrategy = 'L'
            self.losingstrategy = 'P'
        if sorted(strategies) == sorted(['L','Sc']):
            self.winner = self.players[strategies.index('Sc')]
            self.winningstrategy = 'Sc'
            self.losingstrategy = 'L'
        if sorted(strategies) == sorted(['L','Sp']):
            self.winner = self.players[strategies.index('L')]
            self.winningstrategy = 'L'
            self.losingstrategy = 'Sp'
        if sorted(strategies) == sorted(['Sp','P']):
            self.winner = self.players[strategies.index('P')]
            self.winningstrategy = 'P'
            self.losingstrategy = 'Sp'
        if sorted(strategies) == sorted(['Sp','Sc']):
            self.winner = self.players[strategies.index('Sp')]
            self.winningstrategy = 'Sp'
            self.losingstrategy = 'Sc'
        if sorted(strategies) == sorted(['Sc','P']):
            self.winner = self.players[strategies.index('Sc')]
            self.winningstrategy = 'Sc'
            self.losingstrategy = 'P'

    def __str__(self):
        return str(self.winner)

players = [Player('Kev'),
           Player('Eva'),
           Player('Annalise'),
           Player('Heather'),
           Player('Abbie'),
           Player('Sheilla'),
           Player('Sam'),
           Player('Sean'),
           Player('Lewis'),
           Player('Anaesh'),
           Player('Henry'),
           Player('Ed'),
           Player('Brenna'),
           Player('Marcus'),
           Player('Adam'),
           Player('Henry')
           ]

round1 = [Match([players[0], players[1]], [Duel([players[0], players[1]], ['L', 'Sp']),
                                          Duel([players[0], players[1]], ['Sc', 'Sc']),
                                          Duel([players[0], players[1]], ['P', 'R']),
                                          ]),
          Match([players[2], players[3]], [Duel([players[2], players[3]], ['Sp', 'R']),
                                          Duel([players[2], players[3]], ['L', 'L']),
                                          Duel([players[2], players[3]], ['Sc', 'Sp']),
                                          Duel([players[2], players[3]], ['R', 'L'])
                                          ]),
          Match([players[4], players[5]], [Duel([players[4], players[5]], ['Sc', 'P']),
                                          Duel([players[4], players[5]], ['P', 'Sp']),
                                          Duel([players[4], players[5]], ['Sc', 'R']),
                                          ]),
          Match([players[6], players[7]], [Duel([players[6], players[7]], ['P', 'L']),
                                          Duel([players[6], players[7]], ['P', 'L']),
                                          ]),
          Match([players[8], players[9]], [Duel([players[8], players[9]], ['P', 'Sc']),
                                          Duel([players[8], players[9]], ['L', 'Sc']),
                                          ]),
          Match([players[10], players[11]], [Duel([players[10], players[11]], ['L', 'L']),
                                             Duel([players[10], players[11]], ['R', 'Sc']),
                                             Duel([players[10], players[11]], ['L', 'Sp']),
                                          ]),
          Match([players[12], players[13]], [Duel([players[12], players[13]], ['P', 'Sc']),
                                             Duel([players[12], players[13]], ['L', 'Sp']),
                                             Duel([players[12], players[13]], ['R', 'R']),
                                             Duel([players[12], players[13]], ['R', 'R']),
                                             Duel([players[12], players[13]], ['P', 'Sp']),
                                          ]),
          Match([players[14], players[15]], [Duel([players[14], players[15]], ['Sp', 'L']),
                                             Duel([players[14], players[15]], ['Sc', 'L']),
                                             Duel([players[14], players[15]], ['Sc', 'Sc']),
                                             Duel([players[14], players[15]], ['Sc', 'Sc']),
                                             Duel([players[14], players[15]], ['R', 'Sc']),
                                          ]),
                                          ]

strategies = [[s for m in round1 for d in m.duels for s in d.strategies]]
winningstrategies = [[d.winningstrategy for m in round1 for d in m.duels]]
losingstrategies = [[d.losingstrategy for m in round1 for d in m.duels]]

round2 = [Match([players[0], players[2]], [Duel([players[0], players[2]], ['R', 'Sp']),
                                          Duel([players[0], players[2]], ['Sp', 'Sp']),
                                          Duel([players[0], players[2]], ['Sc', 'P']),
                                          ]),
          Match([players[5], players[7]], [Duel([players[5], players[7]], ['Sc', 'P']),
                                          Duel([players[5], players[7]], ['R', 'R']),
                                          Duel([players[5], players[7]], ['R', 'Sp']),
                                          Duel([players[5], players[7]], ['P', 'L'])
                                          ]),
          Match([players[9], players[10]], [Duel([players[9], players[10]], ['Sc', 'R']),
                                            Duel([players[9], players[10]], ['Sc', 'P']),
                                            Duel([players[9], players[10]], ['Sc', 'R']),
                                          ]),
          Match([players[12], players[14]], [Duel([players[12], players[14]], ['P', 'Sc']),
                                          Duel([players[12], players[14]], ['R', 'L']),
                                          Duel([players[12], players[14]], ['P', 'P']),
                                          Duel([players[12], players[14]], ['L', 'Sp'])
                                          ]),
                                          ]

strategies.append([s for m in round2 for d in m.duels for s in d.strategies])
winningstrategies.append([d.winningstrategy for m in round2 for d in m.duels])
losingstrategies.append([d.losingstrategy for m in round2 for d in m.duels])

round3 = [Match([players[0], players[7]], [Duel([players[0], players[7]], ['R', 'P']),
                                           Duel([players[0], players[7]], ['Sc', 'Sp']),
                                          ]),
          Match([players[10], players[12]], [Duel([players[10], players[12]], ['L', 'R']),
                                             Duel([players[10], players[12]], ['Sc', 'Sc']),
                                             Duel([players[10], players[12]], ['L', 'P']),
                                             Duel([players[10], players[12]], ['P', 'R'])
                                          ]),
                                          ]

strategies.append([s for m in round3 for d in m.duels for s in d.strategies])
winningstrategies.append([d.winningstrategy for m in round3 for d in m.duels])
losingstrategies.append([d.losingstrategy for m in round2 for d in m.duels])

round4 = [Match([players[7], players[12]], [Duel([players[7], players[12]], ['Sp', 'P']),
                                            Duel([players[7], players[12]], ['R', 'L']),
                                            Duel([players[7], players[12]], ['Sc', 'Sc']),
                                            Duel([players[7], players[12]], ['P', 'P']),
                                            Duel([players[7], players[12]], ['R', 'Sp'])
                                          ])
                                          ]

strategies.append([s for m in round4 for d in m.duels for s in d.strategies ])
winningstrategies.append([d.winningstrategy for m in round4 for d in m.duels])
losingstrategies.append([d.losingstrategy for m in round3 for d in m.duels])

data = [s for l in strategies for s in l]
strategydict = dict((x,data.count(x)) for x in data)
dictplot(strategydict, 'allstrategies_2016.png', 'All strategies')

data = strategies[0]
strategydict = dict((x,data.count(x)) for x in data)
dictplot(strategydict, 'round1_2016.png', 'Strategies played in round 1')

data = strategies[1]
strategydict = dict((x,data.count(x)) for x in data)
dictplot(strategydict, 'round2_2016.png', 'Strategies played in round 2')

data = strategies[2]
strategydict = dict((x,data.count(x)) for x in data)
dictplot(strategydict, 'round3_2016.png', 'Strategies played in round 3')

data = [s for l in winningstrategies for s in l if s]
strategydict = dict((x,data.count(x)) for x in data)
dictplot(strategydict, 'winningstrategies_2016.png', 'Winning strategies')

data = [s for l in losingstrategies for s in l if s]
strategydict = dict((x,data.count(x)) for x in data)
dictplot(strategydict, 'losingstrategies_2016.png', 'Losing strategies')

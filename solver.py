import nerdle
from generate_space import *
from math import log2 as lg
from Timer import Timer
from scipy.stats import entropy
import csv
import random

GUESS_SPACE = get_file_contents(GUESS_FILE)
SOLUTION_SPACE = get_file_contents(SOLUTION_FILE)

def get_first(poss):
    x = Solver(poss)
    beste = 0
    best_guess = ""
    n = len(x.possibilties)
    t = Timer(n)
    i=0
    for g in x.possibilties:
        e = Solver.calculate_entropy(x.dist(g))
        if e > beste:
            beste = e
            best_guess = g
        with open("foo.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([g, e])
        i += 1
        print(f"{i} of {n}: {t.remains(i)}",end="\r")
    return best_guess



class Solver:
    def __init__(self, poss=1):
        self.guess_history = []
        if poss==1:
            self.possibilties = SOLUTION_SPACE
            self.first = "48-36=12"
        else:
            self.possibilties = GUESS_SPACE

    def prune(self, gue, pattern):
        pruned_possiblities = []
        for a in self.possibilties:
            if nerdle.get_patten(a, gue)==pattern:
                pruned_possiblities.append(a)
        self.possibilties = pruned_possiblities
        return self.possibilties
    
    def dist(self, g):
        """
        Returns the distribution associated with guess g
        """
        dist = dict()
        for a in self.possibilties:
            p = nerdle.get_patten(a,g)
            if p in dist:
                dist[p] += 1
            else:
                dist[p]=1
        return dist
    
    @staticmethod
    def calculate_entropy(dist):
        e = 0
        n = sum(dist.values())
        for d in dist:
            p = dist[d]/n
            e += p*lg(1/p)
        return e

    def get_best_guess(self):
        if self.guess_history==[]:
            entropies = {g:Solver.calculate_entropy(self.dist(g)) for g in self.possibilties}
            return max(entropies, key=entropies.get)
        else:
            return self.first

    def get_random_guess(self):
        return random.choice(self.possibilties)
import nerdle
from math import log2 as lg
from scipy.stats import entropy
import random


with open("docs/guess_space.txt", "r") as file:
    GUESS_SPACE = [e for e in file.read().split("\n") if e]
with open("docs/solution_space.txt", "r") as file:
    SOLUTION_SPACE = [e for e in file.read().split("\n") if e]


class Solver:
    def __init__(self, use_soln=True):
        """
        use_soln is the initial space we search over. It is set to True by 
        default
        """
        self.guess_history = []
        self.solved = False
        if use_soln:
            self.possibilties = SOLUTION_SPACE
            self.first = "48-36=12"
        else:
            self.possibilties = GUESS_SPACE

    def prune(self, gue, pattern):
        self.guess_history.append(gue)
        pruned_possibilities = []
        for a in self.possibilties:
            if nerdle.get_patten(a, gue)==pattern:
                pruned_possibilities.append(a)
        return pruned_possibilities
    
    def update_possibilities(self, gue, pattern):
        self.possibilties = self.prune(gue, pattern)
    
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
        if len(self.possibilties)==1:
            self.solved = True
            return self.possibilties[0]
        if self.guess_history==[]:
            return self.first
        else:
            entropies = {g:Solver.calculate_entropy(self.dist(g))
                 for g in self.possibilties}
            return max(entropies, key=entropies.get)
            
    def get_random_guess(self):
        return random.choice(self.possibilties)


def startInteractive():
    s = Solver()
    g = s.get_best_guess()
    print(f"The best guess is:\n{g}")
    while not s.solved:
        p = input("Type in the pattern:\n")
        s.update_possibilities(g,p)
        g = s.get_best_guess()
        print(f"The best guess is:\n{g}")
    print("SOLVED!!")
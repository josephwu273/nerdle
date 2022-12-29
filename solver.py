import nerdle
from scipy.stats import entropy
from random import choice as rc


with open("docs/guess_space.txt", "r") as file:
    GUESS_SPACE = [e for e in file.read().split("\n") if e]
with open("docs/solution_space.txt", "r") as file:
    SOLUTION_SPACE = [e for e in file.read().split("\n") if e]


class Solver:
    def __init__(self, heur=1, limit_guess=True):
        """
        limit_guess dictates if we limit the guesses to solutions
        """
        self.heuristic = {1:self.calculate_entropy}[heur]
        if limit_guess:
            self.guess_space = SOLUTION_SPACE
        else:
            self.guess_space = GUESS_SPACE
        self.guess_history = []
        self.solved = False
        self.possibilties = SOLUTION_SPACE
        self.first = "48-36=12"

    def prune(self, gue, pattern):
        """
        Given guess <gue> with resultant pattern <pattern>, returns the list of
        answers from self.possiblities that could still work as a solution
        """
        self.guess_history.append(gue)
        pruned_possibilities = []
        for a in self.possibilties:
            if nerdle.get_patten(a, gue)==pattern:
                pruned_possibilities.append(a)
        return pruned_possibilities
    
    def update(self, gue, pattern):
        self.possibilties = self.prune(gue, pattern)
    
    def dist(self, g):
        """
        Returns the distribution associated with guess g
        """
        dist = dict()
        for a in self.possibilties:
            p = nerdle.get_patten(a,g)
            dist[p] = dist.get(p,0)+1
        return dist
    
    def calculate_entropy(self, g):
        pdist = list(self.dist(g).values())
        return entropy(pdist)
    
    def get_next_guess(self):
        if len(self.possibilties)==1:
            self.solved = True
            return self.possibilties[0]
        if self.guess_history==[]:
            return self.first
        else:
            scores = {g:self.heuristic(g) for g in GUESS_SPACE}
            return max(scores, key=scores.get)
            
    def get_random_guess(self):
        return rc(self.possibilties)
    
    def startInteractive(self):
        g = self.get_next_guess()
        print(f"The first best guess is:\n{g}")
        while not self.solved:
            p = input("Type in the pattern:\n")
            self.update(g,p)
            g = self.get_next_guess()
            print(f"The best guess is:\n{g}")
        print("SOLVED!!")


class Simulator(Solver):
    def __init__(self, ans, heur=1, limit_guess=True):
        Solver.__init__(heur, limit_guess)
        self.ans = ans

    def simulate(self):
        ga = nerdle.Game(self.ans)
        while not self.solved:
            gu = self.get_next_guess()
            p,c = ga.play(gu)
            s.update(gu,p)
            unsolved = not bool(c)
        return (nerdle.NUM_GUESSES-ga.remaining)
    
    @staticmethod
    def simulate_all():
        pass


if __name__=="__main__":
    s = Solver()
    s.startInteractive()
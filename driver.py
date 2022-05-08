from docs.Timer import Timer
import docs.generate_space as gs
from solver import *
import nerdle
import csv


def guess_space():
    print("GENERATING GUESS SPACE...")
    gs.generate_guess_space(True)


def solution_space():
    print("GENERATING SOLUTION SPACE...")
    gs.generate_solution_space(True)


def get_best_first(poss):
    print("GENERATING BEST FIRST GUESS")
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


def simGame(ans, use_soln, optimal_guess=True):
    ga = nerdle.Game(ans)
    s = Solver(use_soln)
    guesser = s.get_best_guess if optimal_guess else s.get_random_guess
    unsolved = True
    while unsolved:
        gu = guesser()
        p,c = ga.play(gu)
        s.update_possibilities(gu,p)
        unsolved = not bool(c)
    return (nerdle.NUM_GUESSES-ga.remaining)


def simulate_all(us, og):
    space = SOLUTION_SPACE if us else GUESS_SPACE
    n = len(space)
    t = Timer(n)
    i=0
    failed = 0
    scores = []
    for a in SOLUTION_SPACE:
        try:
            scores.append(simGame(a, us, og))
        except ValueError:
            failed += 1
            n -= 1
        i+=1
        print(" "*50, end="\r")
        print(f"{i} of {n}, {t.remains(i)}", end="\r")
    print()
    print(sum(scores)/n)
    print(failed)
    return scores
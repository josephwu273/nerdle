import sys

import generate_space as gs
import solver

args = sys.argv[1]

if args[0]=="1":
    print("GENERATING GUESS SPACE...")
    gs.generate_guess_space(True)

if args[1]=="1":
    print("GENERATING SOLUTION SPACE...")
    gs.generate_solution_space(True)

if args[2]=="1":
    print("FINDING BEST FIRST GUESS...")
    solver.get_first(1)
    
import sys
sys.path.append("..")
from nerdle import *
from itertools import product
from docs.Timer import Timer
import string



GUESS_FILE = "guess_space.txt"
SOLUTION_FILE = "solution_space.txt"



def get_file_contents(f):
    with open(f, "r") as file:
        contents = [e for e in file.read().split("\n") if e]
    return contents


def generate_guess_space(disp=True):
    gspace = get_file_contents(GUESS_FILE)
    if len(gspace)!=0:
        raise Exception(f"{GUESS_FILE} is not empty. Clear it manually to "\
            "make sure you are not overwriting good data")
    all_combos = product(string.digits+"+-*/", repeat=LENGTH-3)
    #n is the the total number of candidates we must check
    #We peform some pruning first so n isn't actually isn't 14^LENGTH
    n = 12*(14**5)*10*6 #387233280
    i=0
    t = Timer(n, disp)
    for c in all_combos:
        c = "".join(c)
        for x in string.digits+"+-":
            #First entry cannot be * or / so prune those results...
            for y in string.digits:
                #Last entry must be a digit
                s = x+c+y
                for j in range(1,LENGTH-1):
                    if s[j-1].isdigit() and (s[j] in (string.digits+"+-")):
                        #Last entry of LHS must be a digit
                        #First entry of RHS cannot be * or /
                        eqn = s[:j]+"="+s[j:]
                        if Guess.validate(eqn):
                            gspace.append(eqn+"\n")
                    if disp:
                        i += 1
                        p = round(i/n*100, 4)
                        print(f" Finish in {t.remains(i)}; {p}% done", end="\r")
    print()
    print("Writing contents...")
    with open(GUESS_FILE,"a") as gfile:
        gfile.writelines(gspace)
    return gspace


def generate_solution_space(disp=True):
    gspace = get_file_contents(GUESS_FILE)
    if len(gspace)==0:
        print("Generating guess space first...")
        gspace = generate_guess_space()
    sspace = get_file_contents(GUESS_FILE)
    if len(sspace)!=0:
        raise Exception(f"{SOLUTION_FILE} is not empty. Clear it manually to "\
            "make sure you are not overwriting good data")
    sspace = []
    n = len(gspace)
    i=0
    t = Timer(n, disp)
    for g in gspace:
        if Solution.validate(g):
            sspace.append(g+"\n")
        if disp:
            i += 1
            p = round(i/n*100, 4)
            print(f"{g} {p}% done, {t.remains(i)}", end="\r")
    print()
    print("Writing contents...")
    with open(SOLUTION_FILE, "w") as sfile:
        sfile.writelines(sspace)
    return sspace

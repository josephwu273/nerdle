from nerdle import *
from itertools import product
from Timer import Timer

GUESS_FILE = "guess_space.txt"
SOLUTION_FILE = "solution_space.txt"

GUESS_SPACE = []
with open(GUESS_FILE, "r") as gfile:
    GUESS_SPACE = [e for e in gfile.read().split("\n") if e]
SOLUTION_SPACE = []
with open(SOLUTION_FILE, "r") as  sfile:
    SOLUTION_SPACE = [s for s in sfile.read().split("\n") if s]


def generate_guess_space(disp=False):
    global GUESS_SPACE
    if len(GUESS_SPACE)!=0:
        raise Exception(f"{GUESS_FILE} is not empty. Clear it manually to make sure you are not overriding good data")
    gspace = []
    all_combos = product("0123456789+-*/",repeat=LENGTH-3)
    n = 12*(14**5)*10 * 6
    i=0
    t = Timer(n, disp)
    for c in all_combos:
        c = "".join(c)
        for x in "0123456789+-":
            for y in "012345689":
                s = x+c+y
                for j in range(1,LENGTH-1):
                    if s[j-1].isdigit() and (s[j] in "0123456789+-"):
                        eqn = s[:j]+"="+s[j:]
                        if Guess.validate(eqn):
                            gspace.append(eqn+"\n")
                    if disp:
                        i += 1
                        p = round(i/n*100, 4)
                        print(f"{eqn} {p}% done, {t.remains(i)}", end="\r")
    print()
    with open(GUESS_FILE,"w") as gfile:
        gfile.writelines(gspace)
    GUESS_SPACE = gspace

def generate_solution_space(disp=False):
    global SOLUTION_SPACE
    sspace = []
    if len(GUESS_SPACE)==0:
        if disp: print("First generating guess space...")
        generate_guess_space(disp)
    n = len(GUESS_SPACE)
    i=0
    t = Timer(n, disp)
    for g in GUESS_SPACE:
        if Solution.validate(g):
            sspace.append(g+"\n")
        if disp:
            i += 1
            p = round(i/n*100, 4)
            print(f"{g} {p}% done, {t.remains(i)}", end="\r")
    print()
    with open("solution_space.txt", "w") as sfile:
        sfile.writelines(sspace)
    SOLUTION_SPACE = sspace
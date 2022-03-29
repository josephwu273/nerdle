from nerdle import *
from itertools import product
from Timer import Timer

GUESS_SPACE = []
SOLUTION_SPACE = []


def generate_guess_space(disp=False):
    GUESS_SPACE.clear()
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
                            GUESS_SPACE.append(eqn+"\n")
                    i += 1
                    p = round(i/n*100, 4)
                    if disp: print(f"{eqn} {p}% done, {t.remains(i)}", end="\r")
    print()
    with open("guess_space.txt","w") as gfile:
        gfile.writelines(GUESS_SPACE)

def generate_solution_space(disp=False):
    if len(GUESS_SPACE)==0:
        if disp: print("First generating guess space...")
        generate_guess_space(disp)
    n = len(GUESS_SPACE)
    i=0
    t = Timer(n, disp)
    for g in GUESS_SPACE:
        if Solution.validate(g):
            SOLUTION_SPACE.append(g+"\n")
        if disp:
            i += 1
            p = round(i/n*100, 4)
            print(f"{g} {p}% done, {t.remains(i)}", end="\r")
    print()
    with open("solution_space.txt", "w") as sfile:
        sfile.writelines(SOLUTION_SPACE)

from sys import path, argv
path.append("..")
from nerdle import *
from docs.Timer import Timer


def get_file_contents(f):
    with open(f, "r") as file:
        contents = [e for e in file.read().split("\n") if e]
    return contents


def generate_solution_space(gf, sf):
    """
    Filters the guesses from file <gf> and returns the solutions
    Writes solutions into file <sf>
    """
    sspace = []
    gspace = get_file_contents(gf)
    n = len(gspace)
    i=0
    t = Timer(n)
    for g in gspace:
        if Solution.validate(g):
            sspace.append(g+"\n")
        i += 1
        p = round(i/n*100, 4)
        print(f"{g} {p}% done, {t.remains(i)}", end="\r")
    print()
    sspace.sort()
    print("Writing contents...")
    with open(sf, "w") as sfile:
        sfile.writelines(sspace)
    return sspace

if __name__ == "__main__":
    gf = argv[1]
    sf = argv[2]
    generate_solution_space()

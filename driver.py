#WARNING: THIS CODE WILL TAKE A WHILE TO RUN
from itertools import product
from nerdle import *



guess_space = []
solution_space = []

p = product(CHAR_SET,repeat=LENGTH)
n = len(CHAR_SET)**LENGTH
i=0
for s in p:
    s = "".join(s)
    if Guess.validate(s):
        guess_space.append(s)
    if Solution.validate(s):
        solution_space.append(s)
    p = round(i/n * 100, 4)
    print(f"{p}% done: Tabulating {i} of {n}", end="\r")
    i += 1

print(len(guess_space))
print(len(solution_space))

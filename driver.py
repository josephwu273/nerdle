#WARNING: THIS CODE WILL TAKE A WHILE TO RUN
from itertools import product
from nerdle import *



guess_space = []
solution_space = []

p = product("0123456789+-*/",repeat=LENGTH-1)
n = 14**7 * 6
i=0
for s in p:
    s = "".join(s)
    for j in range(1,LENGTH-1):
        q = s[:j]+"="+s[j:]
        if Guess.validate(q):
            guess_space.append(q)
        if Solution.validate(q):
            solution_space.append(q)
        p = round(i/n * 100, 4)
        i += 1
        print(f"{p}% done", end="\r")

print(len(guess_space))
print(len(solution_space))

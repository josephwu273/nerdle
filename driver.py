#WARNING: THIS CODE WILL TAKE A WHILE TO RUN
from itertools import product
from nerdle import *
import datetime
 

#code borrowed from https://code-maven.com/python-time-left
class Timer(object):
    def __init__(self, total):
        self.start = datetime.datetime.now()
        self.total = total
 
    def remains(self, done):
        now  = datetime.datetime.now()
        #print(now-start)  # elapsed time
        left = (self.total - done) * (now - self.start) / done
        sec = int(left.total_seconds())
        if sec < 60:
           return f"{sec} seconds"
        elif sec<3600:
           return f"{int(sec/60)} minutes"
        else:
            return f"{int(sec/3600)} hours; {int((sec%3600)/60)} minutes"


guess_space = []
solution_space = []

p = product("0123456789+-*/",repeat=LENGTH-1)
n = 14**7 * 6
i=0
t = Timer(n)
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
        print(f"{p}% done, {t.remains(i)}", end="\r")

print(len(guess_space))
print(len(solution_space))

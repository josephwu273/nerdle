from sys import argv
from itertools import product
from re import match
from re import sub


def get_expressions(n, m):
    """
    Returns all expressions of length n that evaluate to less than m
    """
    exp_regex = r"^(\d|\+|\-|\d\*\*|\d\*|\d\/)*\d$"
    d = dict()
    print(f"Generating all {n}-length strings. {14**n} strings to parse.")
    i=0
    for s in product("0123456789+-*/", repeat=n):
        i += 1
        print(f"{round(i/14**n*100,4)}% completed    ", end='\r')
        s = "".join(s)
        if match(exp_regex,s):
            try:
                #strip leading 0s from the expression and evaluate it
                num = eval(sub(r"(^|[^\d])0+(\d)", r"\1\2", s))
                if abs(num)<=m:
                    if num in d:
                        d[num].add(s)
                    else:
                        d[num]= {s}
            except ZeroDivisionError:
                pass
    print()
    return d

def get_equations(n, f):
    """
    Returns all equations of length n and writes it to file f
    """
    h = (n-1)//2
    equations = []
    #Greatest value either side of an n-length equation can have
    max_num = int(h*"9")
    for i in range(1,h+1):
        print(f"PART {i} of {h}:")
        exp1 = get_expressions(i, max_num)
        exp2 = get_expressions(n-1-i, max_num)
        for v in (set(exp1)&set(exp2)):
            for eqn in product(exp1[v],exp2[v]):
                equations.append(eqn[0]+"="+eqn[1]+"\n")
                equations.append(eqn[1]+"="+eqn[0]+"\n")
        print()
        print()
    equations.sort()
    with open(f,"w") as file:
        file.writelines(equations)

    return equations

if __name__ == "__main__":
    n = int(argv[1])
    f = argv[2]
    get_equations(n,f)
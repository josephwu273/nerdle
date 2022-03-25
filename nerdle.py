from http.client import FORBIDDEN


CHAR_SET = "0123456789+-*/="
LEN = 8
FORBIDDEN = ["//"]

class Guess:
    def __init__(self, str):
        self.f = str

class Solution(Guess):
    def __init__(self, str):
        self.f = str

def validate_guess(exp):
    #Check input length
    if len(exp) != 8:
        return False
    #Check every char is in CHAR_SET
    if (not all(c in CHAR_SET for c in exp)):
        return False
    #Check exp does not contain "//"
    if "//" in exp:
        return False
    #Check there is 1 and only 1 "="
    eqn = exp.split("=")
    if len(eqn) != 2:
        return False
    #Check LHS and RHS evaluate to the same
    LHS = eqn[0]
    RHS = eqn[1]
    try:
        x = eval(LHS)
        y = eval(RHS)
    except:
        return False
    return x==y

def validate_solution(exp):
    return "sadness"


print(validate_guess("4/2=+2"))
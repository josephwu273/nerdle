CHAR_SET = "0123456789+-*/="


def validate_guess(exp):
    #Check every char is in CHAR_SET
    #Check exp does not contain "//"
    if (not all(c in CHAR_SET for c in exp)) or "//" in exp:
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


print(validate_guess("4//2=2"))
CHAR_SET = "0123456789+-*/="

def validate(exp):
    eqn = exp.split("=")
    if len(eqn) != 2:
        return False
    LHS = eqn[0]
    RHS = eqn[1]
    try:
        x = eval(LHS)
        y = int(RHS)
    except:
        return False
    return x==y


print(validate("2+3+=5"))
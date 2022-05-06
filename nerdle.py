import re

CHAR_SET = "0123456789+-*/="
LENGTH = 8
NUM_GUESSES = 6
EXACT = "G"
CLOSE = "P"
WRONG = "B"


class Guess:
    GUESS_REGEX = r"^(?!.*//)[\d+\-*/]*=[\d+\-*/]*$"
    #No //-symbol
    
    @classmethod
    def validate(cls, s):
        return cls.check_equality(s) and cls.check_format(s) #and cls.check_length(s)
        
    @staticmethod
    def check_length(s):
        """
        Checks that <s> is the right LENGTH for a nerdle guess
        """
        return len(s)==LENGTH
    
    @staticmethod
    def check_format(s):
        """
        Checks that <s> is in the correct format. Note that an input can pass 
        check_format and still be an invalid guess.
        """
        return bool(re.match(Guess.GUESS_REGEX,s))

    @staticmethod
    def split_equation(s):
        """
        Returns LHS and RHS of equation as a tuple of stringles. Also strips LHS
        and RHS of any leading zeroes that will cause SyntaxErrors in Python. 
        """
        expressions = s.split("=")
        #No current Nerdle variant allows multiple equals signs so check for that
        if len(expressions)!=2:
            raise ValueError("Equation has more than one = sign")
        else:
            #strip leading 0s because python is dumb about leading zeros
            #fucking dumbass
            LHS = re.sub(r"(^|[^\d])0+(\d)", r"\1\2", expressions[0])
            RHS = re.sub(r"(^|[^\d])0+(\d)", r"\1\2", expressions[1])
            return LHS,RHS
    
    @staticmethod
    def check_equality(s):
        """
        Checks validity/equality of equation
        """
        try:
            LHS,RHS = Guess.split_equation(s)
            return eval(LHS)==eval(RHS)
        except:
            return False



class Solution(Guess):
    SOLUTION_REGEX = r"^([1-9]\d*[+\-*/][1-9]\d*)([+\-*/][1-9]\d*)*=(0|[1-9]\d*)$"
    #No leading/lone zero; no leading/double operator; only numbers on RHS

    @staticmethod
    def check_format(s):
        return bool(re.match(Solution.SOLUTION_REGEX,s))



class Game:
    def __init__(self, ans):
        self.answer = ans
        self.remaining = NUM_GUESSES
    
    @property
    def answer(self):
        return self._answer
    @answer.setter
    def answer(self, a):
        if not Solution.validate(a):
            raise ValueError("Inputted answer is not a valid Nerdle Solution")
        self._answer = a

    def play(self, gue):
        if Guess.validate(gue):
            pattern = get_patten(self.answer, gue)
            self.remaining -= 1
            print(pattern)
            if pattern==EXACT*LENGTH:
                print(f"CORRECT! Guessed in {NUM_GUESSES-self.remaining}")
            elif self.remaining==0:
                print("GAME OVER")
            else:
                print("Guess again...")
        else:
            print("Bad Guess. Try again")

def get_patten(ans, gue):
    """
    Given guess <gue> outputs the answer patten as a string. If given an
    invalid guess, returns a string of 0-s
    """
    if not Guess.validate(gue):
        return "0"*LENGTH
    output = [WRONG]*LENGTH
    counts = {c:ans.count(c) for c in ans}
    #EXACT Pass. To handle duplicate chars correctly, It is neceary to 
    # first pass through the guess checking for exact matches
    for i in range(LENGTH):
        a=ans[i]
        g=gue[i]
        if a==g:
            output[i]=EXACT
            counts[g] -= 1
    #CLOSE pass, now pass through inserting CLOSE as neceesary
    for j in range(LENGTH):
        a=ans[j]
        g=gue[j]
        if a!=g and g in ans and counts[g]>0:
            output[j]=CLOSE
            counts[g] -= 1
    return "".join(output)
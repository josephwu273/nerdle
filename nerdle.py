import re

CHAR_SET = "0123456789+-*/="
LENGTH = 8
#Note that no current iteration of nerdle allows for multiple equals signs
NUM_EQUALS = 1
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
        Ensures <s> is the right LENGTH for a nerdle guess
        """
        return len(s)==LENGTH
    
    @staticmethod
    def check_format(s):
        """
        Checks that <s> has only allowed chars and no forbidden subsings
        """
        return bool(re.match(Guess.GUESS_REGEX,s))

    @staticmethod
    def split_equation(s):
        """
        Returns LHS and RHS of equation as a tuple
        """
        expressions = s.split("=")
        if len(expressions)!=2:
            raise ValueError("Equation has more than one = sign")
        else:
            return expressions[0],expressions[1]
    
    @staticmethod
    def check_equality(s):
        """
        Checks validity/equality of equation
        """
        expressions = Guess.split_equation(s)
        #strip leading 0s because python is dumb about leading zeros
        #fucking dumbass
        LHS = re.sub(r"0+(\d)", r"\1", expressions[0])
        RHS = re.sub(r"0+(\d)", r"\1", expressions[1])
        try:
            return LHS==RHS
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

    def guess(self, gue):
        output = [WRONG]*LENGTH
        ans = self.answer
        counts = {c:ans.count(c) for c in ans}
        #EXACT Pass. To handle duplicate chars correctly, It is neceary to 
        # first pass through the guess checking for exact matches
        i=0
        while i<len(ans):
            a=ans[i]
            g=gue[i]
            if a==g:
                output[i]=EXACT
                counts[g] -= 1
            i+=1
        #CLOSE pass, now pass through inserting CLOSE as neceesary
        j=0
        while j<len(ans):
            a=ans[j]
            g=gue[j]
            if a!=g and g in ans and counts[g]>0:
                output[j]=CLOSE
                counts[g] -= 1
            j+=1
        print("".join(output))
        return "".join(output)
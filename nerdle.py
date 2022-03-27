import re
from turtle import RawPen

CHAR_SET = "0123456789+-*/="
LENGTH = 8
GUESS_FORBIDDEN = ["//"]
SOLUTION_FORBIDDEN = ["**", "++", "+-", "-+", "--"] + GUESS_FORBIDDEN
FIRST_FORBIDDEN = "0+-"
NUM_EQUALS = 1
NUM_GUESSES = 6
EXACT = "G"
CLOSE = "P"
WRONG = "B"


class Guess:
    @classmethod
    def validate(cls, s):
        le = cls.check_length(s)
        ch = cls.check_chars(s)
        ne = cls.check_numequals(s)
        eq = cls.check_equality(s)
        fi = cls.check_firstchar(s)
        nz = cls.check_nolonezero(s)
        return all([le, ch, ne, eq, fi, nz])

    @staticmethod
    def check_length(s):
        """
        Ensures <s> is the right LENGTH for a nerdle guess
        """
        return len(s)==LENGTH
    
    @staticmethod
    def check_chars(s):
        """
        Checks that <s> has only allowed chars and no forbidden subsings
        """
        return all(c in CHAR_SET for c in s) and all(e not in s for e in GUESS_FORBIDDEN)
    
    @staticmethod
    def check_numequals(s):
        """
        Checks <s> has the correct number of equals signs
        """
        return s.count("=")==NUM_EQUALS

    @staticmethod
    def split_equation(s):
        return s.split("=")
    
    @staticmethod
    def check_equality(s):
        """
        Checks validity/equality of equation
        """
        string_expressions = Guess.split_equation(s)
        #strip leading 0s because python is dumb about leading zeros
        #fucking dumbass
        expressions = [re.sub(r"0+(\d)", r"\1",se) for se in string_expressions]
        print(expressions)
        try:
            y = [eval(i) for i in expressions]
            return all([q==y[0] for q in y])
        except:
            return False
    
    @staticmethod
    def check_firstchar(s):
        return True
    
    @staticmethod
    def check_nolonezero(s):
        return True


class Solution(Guess):
    @staticmethod
    def check_chars(s):
        g = Guess.check_chars(s)
        return g and all(e not in s for e in SOLUTION_FORBIDDEN)

    @staticmethod
    def check_firstchar(s):
        try:
            LHS,RHS = Solution.split_equation(s)
            l = all(LHS[0]!=c for c in FIRST_FORBIDDEN)
            r = all(RHS[0]!=c for c in FIRST_FORBIDDEN)
            return l and r
        except:
            return False
    
    @staticmethod
    def check_nolonezero(s):
        r = r".*(\+|-|\*|\/)0+(=|\+|-|\*|\/).*"
        return not bool(re.match(r,s))


class Game:
    def __init__(self, ans):
        self.answer = ans
        self.remaining = NUM_GUESSES

    def guess(self, guess):
        output = [WRONG]*5
        ans = self.answer
        counts = {c:ans.count(c) for c in ans}
        i=0
        while i<len(ans):
            a=ans[i]
            g=guess[i]
            if a==g:
                output[i]=EXACT
                counts[a] -= 1
            i+=1
        j=0
        while j<len(ans):
            a=ans[j]
            g=guess[j]
            if a!=g and g in ans and counts[g]>0:
                output[j]=CLOSE
            j+=1
        print("".join(output))
        return "".join(output)
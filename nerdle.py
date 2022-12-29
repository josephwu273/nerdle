from re import match, sub as rsub

CHAR_SET = "0123456789+-*/="
EXACT = "G"
CLOSE = "P"
WRONG = "B"


class Guess:
    #No //-symbol
    GUESS_REGEX = r"^(?!.*//)[\d+\-*/]*=[\d+\-*/]*$"
    LHS_REGEX = RHS_REGEX = r"^(\d|\+|\-|\d\*\*|\d\*|\d\/)*\d$"   
    
    #Needs to be classmethod to insure the correct regex is used
    @classmethod
    def validate(cls, s):
        lhs, rhs = cls.split_equation(s)
        format = bool(match(cls.LHS_REGEX,lhs)) and bool(match(cls.RHS_REGEX,rhs))
        #print(format)
        #strip leading 0s because python is dumb about leading zeros
        #fucking dumbass
        LHS = rsub(r"(^|[^\d])0+(\d)", r"\1\2", lhs)
        RHS = rsub(r"(^|[^\d])0+(\d)", r"\1\2", rhs)
        equality = False
        try:
            equality = eval(LHS)==eval(RHS)
        except:
            pass
        #print(equality)
        return format and equality

    @staticmethod
    def split_equation(s):
        """
        Returns LHS and RHS of equation as a tuple of strings. Also strips LHS
        and RHS of any leading zeroes that will cause SyntaxErrors in Python. 
        """
        expressions = s.split("=")
        #No current Nerdle variant allows multiple equals signs so check for that
        if len(expressions)!=2:
            raise ValueError("Equation has more than one = sign")
        else:
            return expressions[0],expressions[1]


class Solution(Guess):
    #No leading/lone zero; no leading/double operator; only numbers on RHS
    SOLUTION_REGEX = r"^([1-9]\d*[+\-*/][1-9]\d*)([+\-*/][1-9]\d*)*=(0|[1-9]\d*)$"
    LHS_REGEX = r"^[1-9]\d*([\+\-\*\/][1-9]\d*)*$"
    RHS_REGEX = r"^(0|[1-9]\d*)$"


class Game:
    @staticmethod
    def get_patten(ans, gue):
        """
        Given guess <gue> outputs the answer patten as a string.
        """
        if len(ans)!=len(gue):
            raise ValueError("Answer and guess should have the same length")
        if not Guess.validate(gue):
            raise ValueError("Input is not a valid guess")

        le = len(ans)
        output = [WRONG]*le
        counts = {c:ans.count(c) for c in ans}
        #EXACT Pass. To handle duplicate chars correctly, It is neceary to 
        # first pass through the guess checking for exact matches
        for i in range(le):
            a=ans[i]
            g=gue[i]
            if a==g:
                output[i]=EXACT
                counts[g] -= 1
        #CLOSE pass, now pass through inserting CLOSE as neceesary
        for j in range(le):
            a=ans[j]
            g=gue[j]
            if a!=g and g in ans and counts[g]>0:
                output[j]=CLOSE
                counts[g] -= 1
        return "".join(output)

    def __init__(self, ans, num_guesses=6):
        self.answer = ans
        self.remaining = num_guesses
        self.len = len(ans)
        #0=still playing; 1=game won; -1=game lost
        self.status = 0
    @property
    def answer(self):
        return self._answer
    @answer.setter
    def answer(self, a):
        if not Solution.validate(a):
            raise AttributeError("Inputted answer is not a valid Nerdle Solution")
        self._answer = a
    @property
    def remaining(self):
        return self._remaining
    @remaining.setter
    def remaining(self,r):
        if r<0:
            self.status = -1
            raise AttributeError("Negative guesses. This should never happen.")
        elif r==0:
            self.status = -1
        self._remaining = r

    def guess(self, g):
        return Game.get_patten(self.answer, g)
    
    def play(self, gue):
        if len(gue)==self.len and gue.count("=")==1 and Guess.validate(gue):
            pattern = self.guess(gue)
            self.remaining -= 1
            if pattern==EXACT*self.len:
                self.status = 1
            return pattern
        else:
            raise IOError("Bad Guess. Try again")

    def startInteractive(self):
        print("WELCOME TO NERDLE")
        print(f"THE HIDDEN EQUATION IS {self.len} CHARACTERS LONG")
        print(f"YOU HAVE {self.remaining} GUESSES TO SOLVE")
        i = 1
        while self.status==0:
            g = input(f"Guess {i}:\n")
            try:
                p = self.play(g)
                print(f"{p}\n")
                i += 1
            except IOError:
                print("Bad Guess. Try Again")
        if self.status==1:
            print("YOU WON")
            print(f"{i-1} guesses used")
        elif self.status==-1:
            print("GAME OVER")
        pass
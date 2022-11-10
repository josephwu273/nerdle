from re import match as rmatch, sub as rsub

CHAR_SET = "0123456789+-*/="
EXACT = "G"
CLOSE = "P"
WRONG = "B"


class Guess:
    GUESS_REGEX = r"^(?!.*//)[\d+\-*/]*=[\d+\-*/]*$"
    LHS_REGEX = RHS_REGEX = r"^(\d|\+|\-|\d\*\*|\d\*|\d\/)*\d$"
    #No //-symbol
    
    @classmethod
    #This needs to be a class method to insure the correct check_format() is called
    def validate(cls, s):
        return cls.check_equality(s) and cls.check_format(s) #and cls.check_length(s)
        
    @staticmethod
    def check_format(s):
        """
        Checks that <s> is in the correct format. Note that an input can pass 
        check_format and still be an invalid guess.
        """
        return bool(rmatch(Guess.GUESS_REGEX,s))

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
            #strip leading 0s because python is dumb about leading zeros
            #fucking dumbass
            LHS = rsub(r"(^|[^\d])0+(\d)", r"\1\2", expressions[0])
            RHS = rsub(r"(^|[^\d])0+(\d)", r"\1\2", expressions[1])
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
        return bool(rmatch(Solution.SOLUTION_REGEX,s))



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
            raise AttributeError("Negative guesses")
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
            print(f"{i} guesses used")
        elif self.status==-1:
            print("GAME OVER")
        pass
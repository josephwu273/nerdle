CHAR_SET = "0123456789+-*/="
LENGTH = 8
GUESS_FORBIDDEN = ["//"]
SOLUTION_FORBIDDEN = ["**", "++", "+-", "-+", "--"] + GUESS_FORBIDDEN
FIRST_FORBIDDEN = "0+-"
NUM_EQUALS = 1


class Guess:
    @classmethod
    def validate(cls, s):
        le = cls.check_length(s)
        ch = cls.check_chars(s)
        ne = cls.check_numequals(s)
        eq = cls.check_equality(s)
        fi = cls.check_firstchar(s)
        return le and ch and ne and eq

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
        return (s.split("=")[0], s.split("=")[1])
    
    @staticmethod
    def check_equality(s):
        """
        Checks validity/equality of equation
        """
        #strip leading zeros because Python itself doesn't allow leading zeros
        #fucking dumbass
        s1, s2 = Guess.split_equation(s)
        LHS =  ' '.join(str(int(x)) if x.isdigit() else x for x in s1.split())
        RHS =  ' '.join(str(int(x)) if x.isdigit() else x for x in s2.split())
        try:
            return eval(LHS)==eval(RHS)
        except:
            return False
    
    @staticmethod
    def check_firstchar(s):
        return True


class Solution(Guess):
    @staticmethod
    def check_chars(s):
        g = Guess.check_chars(s)
        return g and all(e not in s for e in SOLUTION_FORBIDDEN)

    @staticmethod
    def check_firstchar(s):
        LHS,RHS = Solution.split_equation(s)
        l = all(LHS[0]!=c for c in FIRST_FORBIDDEN)
        r = all(RHS[0]!=c for c in FIRST_FORBIDDEN)
        return l and r




print(Guess.validate("1**2=001")) #is True
print(Solution.validate("1**2=001")) #is False
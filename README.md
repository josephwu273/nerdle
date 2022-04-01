# nerdle
A project to use information theory to solve the game of nerdle
https://nerdlegame.com/classic/

## Guess Space vs. Answer Space

A **guess** is any equation that Nerdle will accept as a valid input. A **solution** is an equation that can appear as the answer to a daily game. The guess space and solution space are different and have different rules which we highlight below.

- **Exponents** (`**`) are rendered by the parser. Solutions forbid exponents. Guesses allow them.
- Solutions forbid **explicitly negative** numbers. Guesses allow them.
  - `1-14=-13` or `10+-5=14`
- Solutions forbid** explicitly positives**. Guesses allow them:
  - `+6*1+1=7`
- Solutions forbid **lone zeroes** on the LHS and **any leading zeroes**. Guesses allow lone zeroes and leading zeroes anywhere.
- Solutions forbid **operators** on the RHS (ie the RHS must be a number). GUesses allow operators on the RHS.
- Equations with ***implcit* negative** numbers CAN be nerdle solutions
  - `1-8+10=3` (implicit -7)
- Equations with decimal points are not valid guesses or solutions but ***implicit* decimals** CAN be nerdle solutions: 
  - `5/2*4=10` (implicit 2.5)

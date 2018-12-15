#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

import sys
sys.path.insert(0, 'src/')
from flr_token import Token, TokenType
from scanner import Scanner
from error import LexicalError

##try:
##    filename = sys.argv[1]
##    myfile   = open(filename)
program  = """
{
# using state machines, inspired by
#   https://blog.plover.com/math/divisibility-by-7.html
# note:
#    - I inlined black(),to save the extra function call.
#    - The loop must work forward through the digits of n,
#      not backwards, which is why is_divisible_tr()'s
#      else clause looks odd.  It would be nice in a Flair
#      implementation to reverse(n) first and then use the
#      more natural tail-recursive case:
#         is_divisible_tr(n // 10, blue((state + (n % 10)) % 7)
#      BUT that would lose trailing 0s!
}

program divisible_by_seven(n : integer);

  { standard function from the Flair library }
  function MOD( m : integer, n : integer ) : integer
  begin
    return m - (m/n) * n
  end;

  function blue(state : integer) : integer
  begin
    return      if state = 0 then 0
           else if state = 1 then 3
           else if state = 2 then 6
           else if state = 3 then 2
           else if state = 4 then 5
           else if state = 5 then 1
                {state == 6} else 4
  end;

  function is_divisible_tr(n : integer, state : integer) : integer
  begin
    return if n < 10 then
              blue( (state + n) % 7 )     { black() inlined here }
           else
              is_divisible_tr(MOD(n, 10), is_divisible_tr(n/10, state))
  end;

begin
    return is_divisible_tr(n, 0) = 0
end.

"""

scanner  = Scanner(program)
token = Token(TokenType.EOF)

print("Tokens:\n")
while True:
    tkn = scanner.get_next_token()
    if not tkn:
        print("Something is wrong. Correct me.")
        break
    if tkn.isEOF():                  
        print("\nExecution complete.")
        break 
    print(tkn)   

##except LexicalError as le:
##    print('Lexical error: ' + str(le))
##except Exception as exc:
##    print('Something went wrong: ' + str(exc))

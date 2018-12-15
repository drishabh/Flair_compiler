# Flair_compiler

Source language: Flair (Grammar in /doc)

Taget language : Tiny Machine (tm)

Known bugs: No known bug exists.


Behind the scenes:
	1) The program creates correct 3AC for any legal Flair program.
	2) tm code generation takes place in codeGen and is done 
	   by translating appropriate 3AC to tm code.
	

Features: 
 1) Tail recursion implemented.
 2) Proper error messages for parser.
 
 3) Import is enabled now. The syntax is defined in the grammar and
    some test cases (main_test_A.flr)  portray the correct semantics.
    Import enables the user to imort the main function and all the definitions. **NEW**

Currently working on:
	- Choosing register for code gen using 'get register' and
	  using more than 2 registers for operations.
 
Running the code generator:
	To test the code generator, call flairc from cmd and pass appropriate arguments or
	you can run the mainCodeGen.py in /src and pass appropriate arguments.
	
	
Running the type checker:
	To test the type checker, call flairv from cmd and pass appropriate arguments or
	you can run the mainTypeChecker.py in /src and pass appropriate arguments.
	
	
Running the parser:
	To test the parser, call flairf from cmd and pass appropriate arguments or
	you can run the mainParser.py in /src and pass appropriate arguments.
	
	
Running the scanner:
	To test the scanner, call flairs from cmd and pass appropriate arguments or
	you can run the mainScanner.py in /src and pass appropriate arguments.
	

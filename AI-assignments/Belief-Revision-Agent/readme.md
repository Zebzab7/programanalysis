## How To Run
To run the program run the main.py file.
## Control flow

When run the you will be prompted with a list of actions where entering 1-5 will then show run the function required. 

At the program start the program intialises with a few variables for testing purposes, these can easily be seen with entering 3. 

If in a prompt to make logical expression typing in ```end```, will stop it, otherwise it will ask endlessly for more prompt input.

The commands for And,Or,Implication are as followed ```&, |, >> ``` Implication can also be written as ```Implies(A,B)```


The program does not support any type of command for biimplication. An biimplication can be written in like this 
```(A>>B)&(B>>A) ``` or ```Implies(A,B) & Implies(B>>A) ``` where A and B are the 2 values that needs to be biimplicated. 

Of note is that any some letters are protected from the package sympy, these include ``E, Q `` among others. If a wrong input is written, the program will ask for a new input and show what went wrong
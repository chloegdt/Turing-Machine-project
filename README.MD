# Turing Machine Simulator Project

## Installation

1. Install Python
*Python version used: 3.10.8*

## Content

- Q7/
 - ADDYZ
 - COPYXY
 - MUL
 - RIGHT
 - XLEFT
 - XSEARCH
- Q8/
 - COPY32_42_52
 - LEFT345
 - SORT
 - SORT_ALL_IN_ONE
- CALLER
- COPY
- ERASE1
- mt.py
- PALINDROME
- README.MD

## Utilisation

1. Run the following command: ```python mt.py questionk```
where k is the question number (1 to 10)
2. Or run the following command to execute a turing machine on a given word: ```python mt.py machine_file word```
where *machine_file* is the file containing the code of the machine and *word* the input word matching the alphabet given in **Rules**

## Rules

The file containing the script of a turing machine should follow the description language of the website [turingmachinesimulator](https://turingmachinesimulator.com/ "turingmachinesimulator") :
- ```name:``` is optional (the machine takes the name of the file by default)
- ```init:``` is requiered
- ```accept``` is requiered
- a transition should look like
```q0,a,b```
```q1,a,a,-,>```

We added the following rules :
- the name/init/accept of the turing machine cannot contains a **,** (comma)
- a special transition should look like
```q0,a,b,M,q1```
where M is the turing machine to call
- authorized alphabet: 0, 1, #
- authorized working alphabet: 0, 1, #, \_
- **'** (apostrophe) is forbidden when naming states
## Note

The file Q7/MUL is the main file calling all the others within the Q7/ folder.

The file Q8/SORT is the main file calling all the others within the Q8/ folder
except SORT_ALL_IN_ONE which is the same turing machine without call.

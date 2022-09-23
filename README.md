# SUDOKU SOLVER USING CONSTRAINTS SATISFACTION PROBLEM ALGORITHM 
For this task I built a program that searches the least steps possible solution for a sudoku puzzle.
I used Forward Checking Algorithm + Minimum Variable Choice (MVC), so the required steps/attempts to solve
the puzzle are as little as possible.

Follow this simple instructions to run program at the bottom of main.py

Assign to "levels_list" the difficulty levels that you want program to run, it can have numbers 0-6 

0 --> ALREADY SOLVED PUZZLE (Used for validation of correct implementation during development) \
1 --> EASY LEVEL \
2 --> MEDIUM LEVEL \
3 --> HARD LEVEL \
4 --> EVIL LEVEL \
5 --> WORLD'S HARDEST SUDOKU (MIGHT TAKE A WHILE, DO NOT WORRY) \
6 --> PUZZLE GIVEN ON CANVA AS EXAMPLE BY TEACHER

Run "main.py" to solve every sudoku puzzle on "levels_list"
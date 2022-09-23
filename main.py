import copy
import math
import pandas as pd
from time import time

# Project for AI class
# Tec de Monterrey
# Benjamín Ávila Rosas
# Sept, 2022.

# CODE EXPLANATION VIDEO --> https://youtu.be/4GkxgBKP9sg

PUZZLE_REGION_SIZE = 3
PUZZLE_SIZE = PUZZLE_REGION_SIZE * PUZZLE_REGION_SIZE
SUDOKU_DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]
RANGE_1 = [0, 1, 2]
RANGE_2 = [3, 4, 5]
RANGE_3 = [6, 7, 8]

column_names = range(PUZZLE_SIZE)
possible_answers_attempts = 0


# ---- SUDOKU SOLVER USING CONSTRAINTS SATISFACTION PROBLEM ALGORITHM ----
# For this task I built a program that searches the least steps possible solution for a sudoku puzzle.
# I used Forward Checking Algorithm + Minimum Variable Choice (MVC), so the required steps/attempts to solve
# the puzzle went as little as possible.

# This class stores console output text formats
class ConsoleFormats:
    BOLD = '\033[1m'
    NORMAL = '\033[0m'


# Class that represents a Node in the Search Tree.
# Each node stores a different sudoku puzzle state, the MVC and their relations info
class SudokuStateNode:
    def __init__(self, sudoku_state, children, parent, mvc):
        self.sudoku_state = sudoku_state
        self.children = children
        self.parent = parent
        self.mvc = mvc
        self.fill_empty_variables()

    # Deletes from variable domain every number (from original domain) that fails sudoku's game restrictions
    def wipe_matches_for_position(self, row_index, column_index):
        self.wipe_matches_on_row(row_index)
        self.wipe_matches_on_column(column_index)
        self.wipe_matches_on_block(row_index, column_index)

    # Deletes from variable domain every number (from original domain) that is al ready used on position's block
    def wipe_matches_on_block(self, row_index, column_index):
        row_range = get_range_for_index(row_index)
        column_range = get_range_for_index(column_index)

        for x in row_range:
            for y in column_range:
                if len(self.sudoku_state[x][y]) == 1:
                    wiping_number = self.sudoku_state[x][y][0]
                    # print("Removing " + str(wiping_number) + " from block " + str(row_range) + "," + str(column_range))

                    for aux_x in row_range:
                        for aux_y in column_range:
                            if aux_x != x or aux_y != y:
                                aux_list = self.sudoku_state[aux_x][aux_y]

                                if wiping_number in aux_list:
                                    aux_list.remove(wiping_number)
                                    self.sudoku_state[aux_x][aux_y] = aux_list

    # Deletes from variable domain every number (from original domain) that is al ready used on position's column
    def wipe_matches_on_column(self, column_index):
        # Search for already made choices in the column and delete that choice from the rest of rows in that column
        for row in range(PUZZLE_SIZE):
            # A 1 length domain in a variable means there was a choice made so that choice must be deleted from the
            # rest of domains of variables in the same column
            if len(self.sudoku_state[row][column_index]) == 1:
                wiping_number = self.sudoku_state[row][column_index][0]

                for aux_row in range(PUZZLE_SIZE):
                    # Wipe used numbers from every row of column except itself
                    if aux_row != row:
                        aux_list = self.sudoku_state[aux_row][column_index]

                        # Wipe used number in case it was in the domain of the variable
                        if wiping_number in aux_list:
                            aux_list.remove(wiping_number)
                            self.sudoku_state[aux_row][column_index] = aux_list

    # Deletes from variable domain every number (from original domain) that is al ready used on position's row
    def wipe_matches_on_row(self, row_index):
        # Search for already made choices in the row and delete that choice from the rest of columns in that row
        for column in range(PUZZLE_SIZE):
            # A 1 length domain in a variable means there was a choice made so that choice must be deleted from the
            # rest of domains of variables in the same row
            if len(self.sudoku_state[row_index][column]) == 1:
                wiping_number = self.sudoku_state[row_index][column][0]

                for aux_column in range(PUZZLE_SIZE):
                    # Wipe used numbers from every column of row except itself
                    if aux_column != column:
                        aux_list = self.sudoku_state[row_index][aux_column]

                        # Wipe used number in case it was in the domain of the variable
                        if wiping_number in aux_list:
                            aux_list.remove(wiping_number)
                            self.sudoku_state[row_index][aux_column] = aux_list

    # Prints domain value for every position on current puzzle state (Used for development purposes)
    def print_state_variables_domain(self):
        for x in range(PUZZLE_SIZE):
            for y in range(PUZZLE_SIZE):
                print("Domain for " + str(x) + "," + str(y) + " --> " + str(self.sudoku_state[x][y]))

    # Do Forward Check to reduce variables domains and searches for position with the smallest domain to use it
    # to expand a search node for each value on domain
    def forward_check_and_mvc_search(self):
        global possible_answers_attempts

        solved_puzzle_flag = 1
        smallest_list = copy.deepcopy(SUDOKU_DOMAIN)  # Original Sudoku Variables Domain

        # Iterates on hole puzzle to check if it's solved or not, it also reduces variable domains in case puzzle still not solved
        for x in range(PUZZLE_SIZE):
            for y in range(PUZZLE_SIZE):
                # Execute deletion of values on variable domain that do not satisfy sudoku's restrictions
                self.wipe_matches_for_position(x, y)

                # If there is a variable with no options available on domain, program stops searching for solutions at this tree level
                if len(self.sudoku_state[x][y]) == 0:
                    solved_puzzle_flag = 2

                # If domain has more than one option on position, program keeps looking for solutions on a deeper tree level
                elif len(self.sudoku_state[x][y]) > 1 and solved_puzzle_flag != 0:
                    solved_puzzle_flag = 0

                # MVC must store the smallest domain of a variable found on puzzle's matrix
                if 1 < len(self.sudoku_state[x][y]) < len(smallest_list):
                    smallest_list = copy.deepcopy(self.sudoku_state[x][y]) # Store smallest domain
                    self.mvc = [x, y] # Store smallest domain position on matrix

        # Puzzle solution is found
        if solved_puzzle_flag == 1:
            # Print puzzle solution
            print_formatted_sudoku(self.sudoku_state, 1)
            return solved_puzzle_flag

        # Program might keep looking for a valid puzzle solution
        elif solved_puzzle_flag == 0:
            for value in smallest_list:
                # Increase attempts number
                possible_answers_attempts += 1

                # Assign option value to puzzle in MVC position
                sudoku_matrix_aux = copy.deepcopy(self.sudoku_state)
                sudoku_matrix_aux[self.mvc[0]][self.mvc[1]] = [value]

                # Create a node for option in domain
                option_node = SudokuStateNode(sudoku_matrix_aux, [], self, None)

                # Add option node to current node children list
                self.children.append(option_node)

                # Do Forward Checking and evaluate if puzzle is completed for current option node
                solved_puzzle_flag = option_node.forward_check_and_mvc_search()

                # Stop searching if solution is already found
                if solved_puzzle_flag == 1:
                    break

                # Stop searching if there IS NO SOLUTION AVAILABLE for given puzzle
                if self.parent is None and solved_puzzle_flag == 2:
                    print("No possible solution")
                    break

        return solved_puzzle_flag

    # Assigns original sudoku domain (1-9) to every variable that doesn't have a value when puzzle has just been read from CSV
    def fill_empty_variables(self):
        for y in range(PUZZLE_SIZE):
            for x in range(PUZZLE_SIZE):
                if not self.sudoku_state[y][x]:
                    self.sudoku_state[y][x] = copy.deepcopy(SUDOKU_DOMAIN)


# Create 9x9 puzzle matrix for given CSV data
def create_sudoku_matrix_from_csv(sudoku_from_csv):
    temp_matrix = create_sudoku_empty_matrix()
    initial_matrix = copy.deepcopy(temp_matrix)

    for y in range(PUZZLE_SIZE):
        for x in range(PUZZLE_SIZE):
            # Assign value when founded on  position of original puzzle
            if math.isnan(sudoku_from_csv[x][y]) == 0:
                initial_matrix[y][x] = [int(sudoku_from_csv[x][y])]

            # Assign empty array when no value founded on position of original puzzle
            else:
                initial_matrix[y][x] = []

    return initial_matrix


# Get correct CSV file data depending on difficulty level choice
def get_csv_for_difficulty_level(selected_level):
    sudoku_from_csv = None
    print("\n*********** ", end='')

    if selected_level == 0:
        print("SOLVED LEVEL ", end='')
        sudoku_from_csv = pd.read_csv("Sudoku - Solved.csv", names=column_names)
    if selected_level == 1:
        print("EASY LEVEL ", end='')
        sudoku_from_csv = pd.read_csv("Sudoku - Easy.csv", names=column_names)
    if selected_level == 2:
        print("MEDIUM LEVEL ", end='')
        sudoku_from_csv = pd.read_csv("Sudoku - Medium.csv", names=column_names)
    if selected_level == 3:
        print("HARD LEVEL", end='')
        sudoku_from_csv = pd.read_csv("Sudoku - Hard.csv", names=column_names)
    if selected_level == 4:
        print("EVIL LEVEL ", end='')
        sudoku_from_csv = pd.read_csv("Sudoku - Evil.csv", names=column_names)
    if selected_level == 5:
        print("WORLD'S HARDEST SUDOKU ", end='')
        sudoku_from_csv = pd.read_csv("Sudoku - World Hardest Sudoku.csv", names=column_names)
    if selected_level == 6:
        print("PUZZLE IN CANVA", end='')
        sudoku_from_csv = pd.read_csv("Sudoku - Canva.csv", names=column_names)

    print(" ***********")
    return sudoku_from_csv


# Creates a "better" looking console output of sudoku puzzle
def print_formatted_sudoku(matrix, solved):
    if solved == 1:
        print("\n******** SOLVED SUDOKU PUZZLE *******")
    else:
        print("******* INITIAL SUDOKU PUZZLE *******")

    for y in range(PUZZLE_SIZE):
        for char in range(PUZZLE_SIZE):
            print("----", end='')
        print("-", end='')

        print()
        print("| ", end='')
        for x in range(PUZZLE_SIZE):
            if matrix[y][x]:
                print(ConsoleFormats.BOLD + str(matrix[y][x][0]) + ConsoleFormats.NORMAL, end='')
                print(" |", end=' ')
            else:
                print(" " + " |", end=' ')
        print()

    for char in range(PUZZLE_SIZE):
        print("----", end='')
    print()


# As the name says, it solves the puzzle :P
def solve_sudoku(selected_level):
    # Get CSV file for selected difficulty level
    sudoku_from_csv = get_csv_for_difficulty_level(selected_level)

    # Create sudoku puzzle from CSV file
    sudoku_matrix = create_sudoku_matrix_from_csv(sudoku_from_csv)

    # Print unsolved sudoku puzzle
    print_formatted_sudoku(sudoku_matrix, 0)

    # Initialize timer for solution
    start_time = time()

    # Create root node with initial sudoku state
    new_node = SudokuStateNode(sudoku_matrix, [], None, None)

    # Solve puzzle
    new_node.forward_check_and_mvc_search()

    # Stop timer
    finish_time = time()
    execution_duration = finish_time - start_time

    # Print solution performance results
    print("\n" + str(possible_answers_attempts) + " attempts done to solve puzzle")
    print("Puzzle Solution Search took: " + str("{:.4f}".format(execution_duration)) + " seconds")


# Create empty 9x9 matrix for later usage
def create_sudoku_empty_matrix():
    sudoku_empty_matrix = []

    for y in range(PUZZLE_SIZE):
        new_row = []
        for x in range(PUZZLE_SIZE):
            new_variable = []
            new_row.append(new_variable)
        sudoku_empty_matrix.append(new_row)

    return sudoku_empty_matrix


# Returns range where given columns or row index belongs in sudoku puzzle
def get_range_for_index(index):
    if index in RANGE_1:
        return RANGE_1
    if index in RANGE_2:
        return RANGE_2
    if index in RANGE_3:
        return RANGE_3


# This list stores the difficulty levels that program will run, it can have numbers 0-6
# 0 --> ALREADY SOLVED PUZZLE (Used for validation of correct implementation during development)
# 1 --> EASY LEVEL
# 2 --> MEDIUM LEVEL
# 3 --> HARD LEVEL
# 4 --> EVIL LEVEL
# 5 --> WORLD'S HARDEST SUDOKU (MIGHT TAKE A WHILE, DO NOT WORRY)
# 6 --> PUZZLE GIVEN ON CANVA AS EXAMPLE BY TEACHER
levels_list = [1, 2, 3, 4, 5, 6]

# Run Sudoku solver for every level selected
for level in levels_list:
    solve_sudoku(level)


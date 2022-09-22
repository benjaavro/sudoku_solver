import copy
import math
import pandas as pd

PUZZLE_REGION_SIZE = 3
PUZZLE_SIZE = PUZZLE_REGION_SIZE * PUZZLE_REGION_SIZE
SUDOKU_DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]
RANGE_1 = [0, 1, 2]
RANGE_2 = [3, 4, 5]
RANGE_3 = [6, 7, 8]

column_names = range(PUZZLE_SIZE)
sudoku_from_csv = pd.read_csv("Sudoku - Canva.csv", names=column_names)


class ConsoleFormats:
    BOLD = '\033[1m'
    NORMAL = '\033[0m'


class SudokuStateNode:
    def __init__(self, sudoku_state, children, parent):
        self.sudoku_state = sudoku_state
        self.children = children
        self.parent = parent

    def fill_empty_variables(self):
        for y in range(PUZZLE_SIZE):
            for x in range(PUZZLE_SIZE):
                if not self.sudoku_state[y][x]:
                    self.sudoku_state[y][x] = copy.deepcopy(SUDOKU_DOMAIN)

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

    def wipe_matches_on_block(self, row_index, column_index):
        row_range = get_range_for_index(row_index)
        column_range = get_range_for_index(column_index)

        for x in row_range:
            for y in column_range:
                if len(self.sudoku_state[x][y]) == 1:
                    wiping_number = self.sudoku_state[x][y][0]

                    for aux_x in row_range:
                        for aux_y in column_range:
                            if aux_x != x or aux_y != y:
                                aux_list = self.sudoku_state[aux_x][aux_y]

                                if wiping_number in aux_list:
                                    aux_list.remove(wiping_number)
                                    self.sudoku_state[aux_x][aux_y] = aux_list

    @staticmethod
    def wipe_matches_for_position(row_index, column_index):
        new_node.wipe_matches_on_row(row_index)
        new_node.wipe_matches_on_column(column_index)
        new_node.wipe_matches_on_block(row_index, column_index)

    def forward_check_wiping(self):
        for x in range(PUZZLE_SIZE):
            for y in range(PUZZLE_SIZE):
                self.wipe_matches_for_position(x, y)

    def print_state_variables_domain(self):
        for x in range(PUZZLE_SIZE):
            for y in range(PUZZLE_SIZE):
                print("Domain for " + str(x) + "," + str(y) + " --> " + str(self.sudoku_state[x][y]))


def get_range_for_index(index):
    if index in RANGE_1:
        return RANGE_1
    if index in RANGE_2:
        return RANGE_2
    if index in RANGE_3:
        return RANGE_3


def create_sudoku_empty_matrix():
    sudoku_empty_matrix = []

    for y in range(PUZZLE_SIZE):
        new_row = []
        for x in range(PUZZLE_SIZE):
            new_variable = []
            new_row.append(new_variable)
        sudoku_empty_matrix.append(new_row)

    return sudoku_empty_matrix


def create_sudoku_matrix_from_csv():
    global sudoku_from_csv

    temp_matrix = create_sudoku_empty_matrix()
    initial_matrix = copy.deepcopy(temp_matrix)

    for y in range(PUZZLE_SIZE):
        for x in range(PUZZLE_SIZE):
            if math.isnan(sudoku_from_csv[x][y]) == 0:
                initial_matrix[y][x] = [int(sudoku_from_csv[x][y])]
            else:
                initial_matrix[y][x] = []

    return initial_matrix


def print_formatted_sudoku(matrix, solved):
    if solved == 1:
        print("\n\n******** SOLVED SUDOKU PUZZLE *******")
    else:
        print("\n\n****** UNSOLVED SUDOKU PUZZLE *******")

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


sudoku_matrix = create_sudoku_matrix_from_csv()

new_node = SudokuStateNode(sudoku_matrix, [], None)
# print_formatted_sudoku(new_node.sudoku_state, 0)

new_node.fill_empty_variables()
new_node.forward_check_wiping()
new_node.print_state_variables_domain()

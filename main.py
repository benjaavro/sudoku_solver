import pandas as pd
import numpy as np
import math
import itertools

POSSIBLE_VALUES = set(range(1, 10))
BLOQUES = [
    set(itertools.product([0, 1, 2], ['A', 'B', 'C'])),
    set(itertools.product([0, 1, 2], ['D', 'E', 'F'])),
    set(itertools.product([0, 1, 2], ['G', 'H', 'I'])),

    set(itertools.product([3, 4, 5], ['A', 'B', 'C'])),
    set(itertools.product([3, 4, 5], ['D', 'E', 'F'])),
    set(itertools.product([3, 4, 5], ['G', 'H', 'I'])),

    set(itertools.product([6, 7, 8], ['A', 'B', 'C'])),
    set(itertools.product([6, 7, 8], ['D', 'E', 'F'])),
    set(itertools.product([6, 7, 8], ['G', 'H', 'I'])),
]


sudoku_df = pd.read_csv('./sudoku_input.csv',  header=None)
sudoku_df.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
sudoku_df.head(10)

sudoku_df = sudoku_df.fillna('')
sudoku_df.head()


def get_indexes(row_index, column_index):
    index_blocks = [b for b in BLOQUES if (row_index, column_index) in b][0]
    column_indexes = {(row_index, c_index) for c_index in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']}
    row_indexes = {(r_index, column_index) for r_index in range(9)}

    return index_blocks.union(column_indexes).union(row_indexes)


def get_values_in_indexes(indexes, df):
    values_set = set()
    for r_i, c_i in indexes:
        value_cell = df.iloc[r_i][c_i]
        if not (isinstance(value_cell, str) or isinstance(value_cell, set)):
            values_set = values_set.union({value_cell})
    return values_set


def get_df_sudoku(sudoku_df_):
    sudoku_df_ = sudoku_df_.copy()
    for row_index, row in sudoku_df_.iterrows():
        for c_index in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
            cell_value_is_empty = sudoku_df_.iloc[row_index][c_index] == ''
            if cell_value_is_empty:
                cell_possible_values = POSSIBLE_VALUES
                used_values = get_values_in_indexes(get_indexes(row_index, c_index), sudoku_df_)
                cell_possible_values = cell_possible_values - used_values
                if len(cell_possible_values) == 0:
                    return None
                if len(cell_possible_values) == 1:
                    sudoku_df_.iloc[row_index][c_index] = cell_possible_values.pop()
                else:
                    sudoku_df_.iloc[row_index][c_index] = cell_possible_values
    return sudoku_df_


sudoku_df_v1 = get_df_sudoku(sudoku_df)
print(sudoku_df_v1)

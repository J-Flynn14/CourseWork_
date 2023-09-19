import numpy as np
import pygame as pg
from pygame_menu import pygame_menu as pg_menu
import sys

TITLE = "Connect 4!"
BLOCKSIZE = 100
BG_COLOR = (40, 41, 35)

def check_win(board:np.ndarray) -> int:
    if not any(0 in x for x in board): return 3

    diags_p = [board[::-1,:].diagonal(i) for i in range(-board.shape[0]+1,board.shape[1])]
    diags_n = [board.diagonal(i) for i in range(board.shape[1]-1,-board.shape[0],-1)]
    
    diags = [n.tolist() for n in (diags_p + diags_n)]
    rows = [list(row) for row in board]
    cols = [list(board[:, i]) for i in range(board.shape[1])]

    all_states = diags + rows + cols

    for state in all_states:
        for i in range(len(state)):
            try:
                if state[i] == state[i+1] == state[i+2] == state[i+3]:
                    match state[i]:
                        case 0: pass
                        case 1: return 1
                        case 2: return 2
            except IndexError:
                pass
    return 0

def get_valid_locations(board:np.ndarray) -> list:
        cols = [list(board[:, i]) for i in range(board.shape[1])]
        col_arr = []
        for i in range(len(cols)):
            if np.count_nonzero(board[:, i]) != board.shape[0]:
                col_arr.append(i)
        return col_arr

def get_cols(board:np.ndarray) -> list[np.ndarray]:
    return [[int(i) for i in list(board[:,c])] for c in range(board.shape[0])]

def drop_piece(board:np.ndarray, col:int, player:int) -> np.ndarray:
    row = (board.shape[0] - np.count_nonzero(board[:, col])) - 1
    b_copy = np.copy(board)
    b_copy[row][col] = player
    return b_copy
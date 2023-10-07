from copy import deepcopy
from functools import cached_property
from dataclasses import dataclass
import numpy as np

TITLE = "Connect 4!"
BLOCKSIZE = 100
BG_COLOR = (40, 41, 35)

@dataclass
class Board():
    state: np.ndarray

    def __eq__(self, __value:object) -> bool:
        if self.state.shape != __value.state.shape: return False
        else: return (self.state == __value.state).all()
    
    @property
    def shape(self):
        return self.state.shape
    
    def check_win(self) -> int:
        if not any(0 in x for x in self.state): return 3

        sub_states = self._get_sub_states()

        for _i, state in enumerate(sub_states):
            for i in range(len(state)):
                try:
                    _ = state[i+3]
                except IndexError: break

                if state[i] == state[i+1] == state[i+2] == state[i+3]:
                    match state[i]:
                        case 0: pass
                        case 1: return 1
                        case 2: return 2
        return 0

    def get_valid_locations(self) -> list[int]:
        cols = [list(self.state[:, i]) for i in range(self.shape[1])]
        col_arr = [i for i in range(len(cols)) if np.count_nonzero(self.state[:, i]) != self.shape[0]]
        return col_arr

    def get_cols(self) -> list[np.ndarray]:
        return [[int(i) for i in list(self.state[:,c])] for c in range(self.state.shape[0])]

    def drop_piece(self, col:int, player:int, sim=False) -> np.ndarray|None:
        row = (self.state.shape[0] - np.count_nonzero(self.state[:, col])) - 1
        if sim:
            b_copy = self.copy()
            b_copy.state[row][col] = player
            return b_copy
        else: self.state[row, col] = player

    def _get_sub_states(self) -> list[list[int]]:
        diags_p = [self.state[::-1,:].diagonal(i) for i in range(-self.shape[0]+1,self.shape[1])]
        diags_n = [self.state.diagonal(i) for i in range(self.shape[1]-1,-self.shape[0],-1)]
        
        diags = [n.tolist() for n in (diags_p + diags_n)]
        rows = [list(row) for _i, row in enumerate(self.state)]
        cols = [list(self.state[:, i]) for i in range(self.shape[1])]
        sub_states = diags + rows + cols
        return sub_states
    
    def copy(self):
        return deepcopy(self)
    
    
from utils import *

class MinimaxAgent:
    def __init__(self):
        pass

    @staticmethod
    def drop_piece(board:np.ndarray, col:int, player:int) -> np.ndarray:
        row = (board.shape[0] - np.count_nonzero(board[:, col])) - 1
        b_copy = np.copy(board)
        b_copy[row][col] = player
        return b_copy
       
    def evaluate_window(self, window:list, player:int) -> int:
        score = 0
        opp_player = 1
        if player == 1: opp_player = 2

        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2
        if window.count(opp_player) == 3 and window.count(0) == 1:
            score -= 50
        return score

    def get_score(self, board:np.ndarray, player:int) -> int:
        score = 0
        n_rows, n_cols = board.shape
        
        center_array = [int(i) for i in list(board[:, n_cols//2])]
        center_count = center_array.count(player)
        score += center_count * 3

        for row in board:
            for c in range(n_cols-3):
                window = list(row[c:c+4])
                score += self.evaluate_window(window, player)

        for col in get_cols(board):
            for r in range(n_rows-3):
                window = list(col[r:r+4])
                score += self.evaluate_window(window, player)
                
        for r in range(n_rows-3):
            for c in range(n_cols-3):
                window = [board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        for r in range(n_rows-3):
            for c in range(n_cols-3):
                window = [board[r+3-i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)
        return score
         
    def minimax(self, board:np.ndarray, depth:int, maximising_player:bool, alpha=-np.inf, beta=np.inf) -> tuple[int,float]:
        if depth == 0: return None, self.get_score(board, 2)
        match check_win(board):
            case 0: pass
            case 1: return -1, -10000000000000
            case 2: return -1, 100000000000000
            case 3: return -1, 0

        valid_locations = get_valid_locations(board)
        if maximising_player:
            value = -np.inf
            column = np.random.choice(valid_locations)

            for col in valid_locations:
                b_copy = self.drop_piece(board, col, 2)
                p_score = self.minimax(b_copy, depth-1, False, alpha, beta)[1]

                if p_score > value:
                    value = p_score
                    column = col

                alpha = max(alpha, value)

                if alpha >= beta:
                    break

            return column, value
        else:
            value = np.inf
            column = np.random.choice(valid_locations)

            for col in valid_locations:
                b_copy = self.drop_piece(board, col, 1)
                p_score = self.minimax(b_copy, depth-1, True, alpha, beta)[1]

                if p_score < value:
                    value = p_score
                    column = col

                beta = min(beta, value)

                if alpha >= beta:
                    break

            return column, value



        



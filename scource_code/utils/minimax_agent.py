from utils import *

class MinimaxAgent:
    @staticmethod
    def get_score(board:Board, player:int) -> int:
        # Calculate score for all subsarrays of board
        score = 0
        opp_player = 1
        if player == 1: opp_player = 2

        sub_states = board._get_sub_states()

        for _i, state in enumerate(sub_states):
            for i in range(len(state)):
                try:
                    _ = state[i+3]
                except IndexError: break
                window = [state[i],state[i+1],state[i+2],state[i+3]]
                player_count = window.count(player)
                zero_count = window.count(0)

                if player_count == 4:
                    score += 100
                elif player_count == 3 and zero_count == 1:
                    score += 5
                elif player_count == 2 and zero_count == 2:
                    score += 2
                elif window.count(opp_player) == 3 and zero_count == 1:
                    score -= 50

        center_array = [int(i) for i in list(board.state[:, board.shape[0]//2])]
        center_count = center_array.count(player)
        score += center_count * 3
        return score
    
    def minimax(self, board:Board, depth:int, maximising_player:bool, alpha=-np.inf, beta=np.inf) -> tuple[int,float]:
        #executes minimax algorithm on all child nodes to get best action
        if depth == 0: return None, self.get_score(board, 2)
        match board.check_win():
            case 0: pass
            case 1: return -1, -10000000000000
            case 2: return -1, 1000000000000
            case 3: return -1, 0

        valid_locations = board.get_valid_locations()
        if maximising_player:
            value = -np.inf
            column = np.random.choice(valid_locations)

            for _i, col in enumerate(valid_locations):
                new_state = board.drop_piece(col, 2, sim=True)
                p_score = self.minimax(new_state, depth-1, False, alpha, beta)[1]
                del new_state

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

            for _i, col in enumerate(valid_locations):
                new_state = board.drop_piece(col, 1, sim=True)
                p_score = self.minimax(new_state, depth-1, True, alpha, beta)[1]
                del new_state

                if p_score < value:
                    value = p_score
                    column = col

                beta = min(beta, value)

                if alpha >= beta:
                    break

            return column, value
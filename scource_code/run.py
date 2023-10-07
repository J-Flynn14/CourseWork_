from utils import *
from utils.env import ConnectFour
from utils.minimax_agent import MinimaxAgent

agent = MinimaxAgent()
env = ConnectFour(agent=agent, board_shape=(7,6))

if __name__ == "__main__":
    observation = env.reset()

    while 1: 
        env.render()

        action = env.get_action(observation)

        if action in env.get_valid_locations():
            observation = env.step(action)
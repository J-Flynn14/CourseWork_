from utils import *
from utils.minimax_agent import MinimaxAgent
import pygame as pg
from pygame.locals import DOUBLEBUF
from pygame_menu import pygame_menu as pg_menu
from typing import NoReturn
import sys

class ConnectFour(Board):
    def __init__(self, agent:MinimaxAgent, board_shape:tuple[int]):
        self.n_cols, self.n_rows = board_shape[0], board_shape[1]
        super().__init__(np.zeros((self.n_rows, self.n_cols), dtype=int))
        self.ai_on = True
        self.agent = agent
        self.depth = 1
        self.score = {1: 0, 2: 0}

        self.init_window(())
        self.init_menu()

    @property
    def player(self) -> int:
        return 1 if self.turn == 0 else 2

    @property
    def selection(self) -> int:
        return int(pg.mouse.get_pos()[0]/BLOCKSIZE)

    @property
    def board_surface(self) -> pg.Surface:
        board_surface = pg.Surface((self.n_cols * BLOCKSIZE, self.n_rows * BLOCKSIZE))

        for row in range(self.n_rows):
            for col in range(self.n_cols):
                _r = pg.draw.rect(board_surface,"blue",((col * BLOCKSIZE), (row * BLOCKSIZE), BLOCKSIZE, BLOCKSIZE))
                match self.state[row][col]:
                    case 1:
                        pg.draw.circle(
                            board_surface,
                            "yellow",
                            (_r.centerx, _r.centery),
                            BLOCKSIZE / 2.3,
                        )
                    case 2:
                        pg.draw.circle(
                            board_surface,
                            "red",
                            (_r.centerx, _r.centery),
                            BLOCKSIZE / 2.3,
                        )
                    case 0:
                        pg.draw.circle(
                            board_surface,
                            BG_COLOR,
                            (_r.centerx, _r.centery),
                            BLOCKSIZE / 2.3,
                        )
        return board_surface

    @property
    def score_screen(self) -> pg.Surface:
        score_counter = pg.Surface((self.n_cols * BLOCKSIZE, (self.n_rows + 1) * BLOCKSIZE), pg.SRCALPHA)
        score_counter = self.draw_text(
            score_counter,
            f"Yellow:{self.score[1]} Red:{self.score[2]}",
            int(BLOCKSIZE * 0.3),
            (255, 255, 255),
            (self.n_cols / 3) + 10,
            (self.n_rows / 3),
        )
        return score_counter

    @property
    def win_screen(self) -> pg.Surface:
        win_screen = pg.Surface((self.n_cols * BLOCKSIZE, (self.n_rows + 1) * BLOCKSIZE), pg.SRCALPHA)
        if self.player_won == 3:
            win_screen = self.draw_text(
                win_screen,
                f"Draw!",
                int(BLOCKSIZE * 0.4),
                (255, 255, 255),
                (self.n_cols / 3) + 10,
                (self.n_rows / 3),
            )
        else:
            win_screen = self.draw_text(
                win_screen,
                f"Player {self.player_won} Wins!",
                int(BLOCKSIZE * 0.4),
                (255, 255, 255),
                (self.n_cols / 3) + 10,
                (self.n_rows / 3),
            )
        return win_screen

    @staticmethod
    def draw_text(surface, text, size, color, x, y) -> pg.Surface:
        font = pg.font.SysFont("arialblack", size)
        image = font.render(text, True, color)
        surface.blit(image, (x, y))
        return surface

    @staticmethod
    def close() -> NoReturn:
        pg.quit()
        sys.exit(0)

    def init_window(self, board_shape:tuple) -> None:
        pg.init()
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.K_ESCAPE, pg.MOUSEBUTTONDOWN])

        if board_shape != (): self.n_cols, self.n_rows = board_shape[0], board_shape[1]

        self.window = pg.display.set_mode((self.n_cols * BLOCKSIZE, (self.n_rows + 1) * BLOCKSIZE), DOUBLEBUF, 8)
        
        try: icon = pg.image.load("icon.png"); pg.display.set_icon(icon)
        except: pass
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

    def init_menu(self) -> None:
        difficulties = [("Easy", 1), ("Normal", 3), ("Hard", 4)]
        game_modes = [("Singleplayer", 1), ("Multiplayer", 2)]
        board_sizes = [("7x6", 1), ("5x4", 2), ("6x5", 3),
                       ("8x7", 4), ("8x8", 5), ("9x7", 6),
                       ("10x7", 7)]

        self.menu = pg_menu.Menu(
            "Connect Four",
            self.n_cols * BLOCKSIZE,
            (self.n_rows + 1) * BLOCKSIZE,
            theme=pg_menu.themes.THEME_DARK,
        )
        self.options_menu = pg_menu.Menu(
            "Options",
            self.n_cols * BLOCKSIZE,
            (self.n_rows + 1) * BLOCKSIZE,
            theme=pg_menu.themes.THEME_DARK,
        )
        self.options_menu.add.selector(
            "Game Mode",
            game_modes,
            onchange=self.change_game_mode,
            style='fancy',
            style_fancy_bgcolor=BG_COLOR,
            style_fancy_bordercolor=BG_COLOR
        )
        self.options_menu.add.selector(
            "Ai Difficulty",
            difficulties,
            onchange = self.change_difficulty,
            style='fancy',
            style_fancy_bgcolor=BG_COLOR,
            style_fancy_bordercolor=BG_COLOR
        )
        self.options_menu.add.selector(
            "Board Size",
            board_sizes,
            onreturn=self.change_board_size,
            style='fancy',
            style_fancy_bgcolor=BG_COLOR,
            style_fancy_bordercolor=BG_COLOR
        )
        self.menu.add.button("Play", self.menu.disable)
        self.menu.add.button(self.options_menu.get_title(), self.options_menu)
        self.menu.add.button("Exit", self.close)

    def change_game_mode(self, value:tuple[str,int], mode:int) -> str:
        selected = value[0]
        match mode:
            case 1: self.ai_on = True
            case 2: self.ai_on = False
        self.score = {1: 0, 2: 0}
        self.reset()
        return selected

    def change_difficulty(self, value:tuple[str,int], difficulty:int) -> str:
        selected = value[0]
        self.depth = difficulty
        self.score = {1: 0, 2: 0}
        self.reset()
        return selected
    
    def change_board_size(self, value:tuple[str,int], *args) -> str:
        selected = value[0]
        board_size = [int(n) for n in selected[0].split('x')]
        self.init_window(board_size)
        self.init_menu()
        self.score = {1: 0, 2: 0}
        self.reset()
        return selected

    def reset(self) -> np.ndarray:
        #reset the state of the game
        self.state = np.zeros((self.n_rows, self.n_cols), dtype=int)
        self.terminated = False
        self.player_won = 0
        self.turn = 0
        self.b_down = False

        observation = np.copy(self.state)
        return observation

    def step(self, action:int) -> np.ndarray:
        #performs one action and checks if a player has won
        self.drop_piece(action, self.player)
        match self.check_win():
            case 0: self.player_won = 0
            case 1: self.player_won = 1
            case 2: self.player_won = 2
            case 3: self.player_won = 3

        self.turn += 1
        self.turn = self.turn % 2

        observation = np.copy(self.state)

        if self.player_won != 0:
            if self.player_won != 3:
                self.score[self.player_won] += 1
            self.terminated = True

        return observation

    def render(self) -> None:
        if self.menu.is_enabled():
            self.menu.draw(self.window)
            self.menu.update(pg.event.get())
        else:
            self.window.fill((40, 41, 35))
            self.window.blit(self.board_surface, (0, BLOCKSIZE))

            if self.terminated: 
                self.window.blit(self.win_screen, (0, 0))
            else:
                if self.player == 1:
                    pg.draw.circle(self.window, "yellow", (self.selection*BLOCKSIZE + BLOCKSIZE/2, BLOCKSIZE/2),BLOCKSIZE/2.3)
                else:
                    if not self.ai_on:
                        pg.draw.circle(self.window, "red", (self.selection*BLOCKSIZE + BLOCKSIZE/2, BLOCKSIZE/2), BLOCKSIZE/2.3)
                self.window.blit(self.score_screen, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.menu.enable()

            if event.type == pg.MOUSEBUTTONDOWN and not self.menu.is_enabled():
                if self.terminated:
                    self.reset()
                else:
                    self.b_down = True

        if pg.display.get_active():
            pg.display.update()
            self.clock.tick(60)

    def get_action(self, observation:np.ndarray) -> int:
        action = None
        if ((self.player == 1) or (self.player == 2 and not self.ai_on)) and self.b_down:
            self.b_down = False
            if self.selection in self.get_valid_locations():
                action = self.selection

        elif self.player == 2 and self.ai_on and not self.terminated:
            action = self.agent.minimax(Board(observation), self.depth, True)[0]

        return action



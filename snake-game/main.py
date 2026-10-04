"""
Terminal Snake Game (pure Python)

Usage:
  - Run with: uv main.py  (or: python snake-game/main.py)

Controls:
  - Arrow keys or WASD to move
  - P to pause
  - Q to quit

This implementation uses only the Python standard library. It supports Windows (msvcrt) and Unix-like systems (termios).
"""

import os
import sys
import time
import random

# Key reading helpers: Windows (msvcrt) or Unix (termios + tty)
IS_WINDOWS = sys.platform.startswith('win')

if IS_WINDOWS:
    import msvcrt

    def get_pressed_key():
        """Return a key string for an available key, or None if no key pressed."""
        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            # Arrow keys return a prefix then a code
            if ch == '\x00' or ch == '\xe0':
                ch2 = msvcrt.getwch()
                # Map common codes to words
                return {
                    'H': 'UP',    # arrow up
                    'P': 'DOWN',
                    'K': 'LEFT',
                    'M': 'RIGHT'
                }.get(ch2, ch2)
            else:
                return ch.upper()
        return None

else:
    import tty
    import termios
    import select

    def get_pressed_key():
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        if not dr:
            return None
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # possible escape sequence for arrows
                # read two more bytes if available
                ch2 = sys.stdin.read(2)
                seq = ch + ch2
                return {
                    '\x1b[A': 'UP',
                    '\x1b[B': 'DOWN',
                    '\x1b[D': 'LEFT',
                    '\x1b[C': 'RIGHT'
                }.get(seq, seq)
            return ch.upper()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# Game configuration
WIDTH = 30
HEIGHT = 16
START_LENGTH = 4
INITIAL_SPEED = 6.0  # steps per second
SPEED_INCREMENT = 0.3  # per food
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), 'highscore.txt')


def clear_screen():
    os.system('cls' if IS_WINDOWS else 'clear')


def load_highscore():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return int(f.read().strip() or 0)
    except Exception:
        return 0


def save_highscore(score):
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(score))
    except Exception:
        pass


class SnakeGame:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        mid_x = self.width // 2
        mid_y = self.height // 2
        self.snake = [(mid_x - i, mid_y) for i in range(START_LENGTH)]  # head is first
        self.direction = 'RIGHT'
        self.place_food()
        self.score = 0
        self.speed = INITIAL_SPEED
        self.game_over = False
        self.paused = False

    def place_food(self):
        positions = {(x, y) for x in range(1, self.width-1) for y in range(1, self.height-1)}
        positions -= set(self.snake)
        self.food = random.choice(list(positions)) if positions else None

    def step(self):
        if self.game_over or self.paused:
            return
        head_x, head_y = self.snake[0]
        dx, dy = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }[self.direction]

        new_head = (head_x + dx, head_y + dy)

        # Check collisions with walls
        if not (0 < new_head[0] < self.width-1 and 0 < new_head[1] < self.height-1):
            self.game_over = True
            return

        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Eat food?
        if self.food and new_head == self.food:
            self.score += 1
            self.speed += SPEED_INCREMENT
            self.place_food()
        else:
            self.snake.pop()

    def change_direction(self, new_dir):
        # prevent reversing
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_dir == opposites.get(self.direction):
            return
        self.direction = new_dir

    def draw(self):
        buf_lines = []
        top = '+' + '-' * (self.width - 2) + '+'
        buf_lines.append(top)
        for y in range(self.height):
            if y == 0 or y == self.height - 1:
                continue
            line = '|'
            for x in range(1, self.width-1):
                ch = ' '
                if (x, y) == self.snake[0]:
                    ch = 'O'
                elif (x, y) in self.snake[1:]:
                    ch = 'o'
                elif self.food and (x, y) == self.food:
                    ch = '*'
                line += ch
            line += '|'
            buf_lines.append(line)
        bottom = '+' + '-' * (self.width - 2) + '+'
        buf_lines.append(bottom)

        info = f"Score: {self.score}  Speed: {self.speed:.1f}  High: {load_highscore()}"
        return '\n'.join([info] + buf_lines)


def run():
    game = SnakeGame()
    highscore = load_highscore()

    last_time = time.time()
    acc = 0.0
    frame_time = 1.0 / game.speed

    if not IS_WINDOWS:
        # make stdin non-blocking by ensuring terminal raw mode handled in get_pressed_key
        pass

    try:
        while True:
            now = time.time()
            delta = now - last_time
            last_time = now
            acc += delta

            # handle input
            key = get_pressed_key()
            if key:
                if key in ('UP', 'W'):
                    game.change_direction('UP')
                elif key in ('DOWN', 'S'):
                    game.change_direction('DOWN')
                elif key in ('LEFT', 'A'):
                    game.change_direction('LEFT')
                elif key in ('RIGHT', 'D'):
                    game.change_direction('RIGHT')
                elif key == 'P':
                    game.paused = not game.paused
                elif key == 'Q':
                    break
                elif key == 'R' and game.game_over:
                    game.reset()

            # update speed-derived frame time each loop
            frame_time = 1.0 / max(1.0, game.speed)

            if acc >= frame_time:
                acc -= frame_time
                game.step()

            # Render
            clear_screen()
            print(game.draw())

            if game.game_over:
                print('\nGAME OVER!')
                print('Press R to restart, Q to quit')
                if game.score > highscore:
                    highscore = game.score
                    save_highscore(highscore)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        clear_screen()
        print('Thanks for playing!')


if __name__ == '__main__':
    run()

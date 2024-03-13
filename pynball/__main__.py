from pathlib import Path
import importlib.resources

import pygame
from pynball.pynball_env import PynBall
from pynball.viewer import Viewer


def main() -> None:
    """Runs an interactive instance of PynBall.

    Accelerate the ball using arrow keys. Close window to quit.
    """

    config = importlib.resources.files("pynball.configs") / "easy_config.toml"
    env = PynBall(Path(config))
    env.reset()
    pygame.init()
    viewer = Viewer(env)
    actions = {
        pygame.K_RIGHT: 0,
        pygame.K_UP: 3,
        pygame.K_LEFT: 2,
        pygame.K_DOWN: 1,
    }
    noop = 4
    running = True
    reward = 0

    while running:
        pygame.time.wait(50)
        user_action = noop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type in (pygame.KEYUP, pygame.KEYDOWN):
                user_action = actions.get(event.key, noop)
        _, r, t, _ = env.step(user_action)
        if t:
            running = False
        reward += r
        viewer.blit(env.ball)
        pygame.display.flip()

    pygame.quit()
    print(f"Score: {reward}")

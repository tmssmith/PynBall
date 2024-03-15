from pathlib import Path
import importlib.resources

import pygame
from pynball_rl.pynball_env import PynBall
from pynball_rl.viewer import Viewer


def main() -> None:
    """Runs an interactive instance of PynBall.

    Accelerate the ball using arrow keys. Close window to quit.
    """

    config_dict = {
        1: "very_easy",
        2: "easy",
        3: "hard",
    }

    difficulty = int(input("Enter difficulty between 1 (very easy) and 3 (hard)"))
    if difficulty not in [1, 2, 3]:
        difficulty = 2

    file = f"{config_dict[int(difficulty)]}_config.toml"
    # file = "four_rooms_config.toml"

    config = importlib.resources.files("pynball_rl.configs") / file
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
    reward = 0
    running = True
    terminal = False
    while running:
        pygame.time.wait(50)
        user_action = noop
        r = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                user_action = actions.get(event.key, noop)
        if user_action in env.action_space:
            _, r, terminal, _ = env.step(user_action)
        if terminal:
            running = False
        reward += r
        viewer.blit(env.ball)
        pygame.display.flip()

    pygame.quit()
    print(f"Score: {reward}")


if __name__ == "__main__":
    main()

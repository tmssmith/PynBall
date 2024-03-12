import random

# import pygame
from pynball.pynball_env import PynBall
from pynball.point import Point

# from pynball.viewer import Viewer


# def main():
#     env = PynBall("config.toml")
#     env.reset()
#     env.ball.set_position(-0.0006506808392933282, 0.662197840901113)
#     env.ball.set_velocity(Point(0.786074875 * 1.005, 0.7356048375889863 * 1.005))
#     for _ in range(20):
#         env.ball.step(20)
#     env.ball.set_velocity(Point(-0.786074875 * 1.005, -0.7356048375889863 * 1.005))
#     print(env.ball)
#     env.render()


def main():
    env = PynBall("config.toml")
    env.reset()
    for _ in range(int(1e6)):
        user_action = random.choice(range(5))
        _, _, t, _ = env.step(user_action)
        if t:
            env.reset()


# def main():
#     """Entry point if called as executable."""
#     env = PynBall("config.toml")
#     env.reset()
#     # pygame.init()
#     # screen = pygame.display.set_mode([500, 500])
#     # viewer = Viewer(screen, env)
#     # actions = {
#     #     pygame.K_RIGHT: 0,
#     #     pygame.K_UP: 3,
#     #     pygame.K_LEFT: 2,
#     #     pygame.K_DOWN: 1,
#     # }
#     # noop = 4
#     # running = True
#     # reward = 0
#     for _ in range(int(1e6)):
#         # while running:
#         # pygame.time.wait(50)
#         # user_action = noop
#         # for event in pygame.event.get():
#         #     if event.type == pygame.QUIT:
#         #         running = False
#         # if event.type in (pygame.KEYUP, pygame.KEYDOWN):
#         #     user_action = actions.get(event.key, noop)
#         user_action = random.choice(range(5))
#         _, _, t, _ = env.step(user_action)
#         if t:
#             env.reset()
#         # reward += r
#         # viewer.blit()
#         # pygame.display.flip()

#     # pygame.quit()
#     # print(f"Score: {reward}")


if __name__ == "__main__":
    main()

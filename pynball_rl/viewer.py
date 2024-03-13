try:
    import pygame
except ImportError as e:
    print(f"Pygame not available: {e}")
from pynball_rl.pynball_env import PynBall
from pynball_rl.point import Point
from pynball_rl.ball import Ball


class Viewer:
    """Tools for rendering a PynBall game using PyGame."""

    DARK_GREY: list[int] = [64, 64, 64]
    LIGHT_GREY: list[int] = [232, 232, 232]
    BALL_COLOR: list[int] = [0, 0, 255]
    TARGET_COLOR: list[int] = [255, 0, 0]

    def __init__(self, env: PynBall, size: list[int] | None = None) -> None:
        """Initialises a viewer instance.

        Args:
            env (PynBall): PynBall environment to render.
            size (list[int] | None, optional): Size of render window. If None a size
            of [750, 750] is used. Defaults to None.
        """
        if size is None:
            size = [750, 750]
        self.screen = pygame.display.set_mode(size)
        self.env = env
        self.surface = pygame.Surface(size)
        self.surface.fill(self.LIGHT_GREY)
        self.min_dim = min(size)
        for obstacle in self.env.obstacles:
            pygame.draw.polygon(
                self.surface,
                self.DARK_GREY,
                [self._to_pixels(point) for point in obstacle.points],
            )
        pygame.draw.circle(
            self.surface,
            self.TARGET_COLOR,
            self._to_pixels(self.env.target.point),
            int(self.env.target.radius * self.min_dim),
        )

    def blit(self, ball: Ball) -> None:
        """Draws the ball onto the surface.

        Args:
            ball (Ball): Ball to draw.
        """
        self.screen.blit(self.surface, (0, 0))
        pygame.draw.circle(
            self.screen,
            self.BALL_COLOR,
            self._to_pixels(ball.get_center()),
            int(ball.radius * self.min_dim),
        )

    def replay(self, states: list[tuple]) -> None:
        """Replay a trajectory of states.

        Args:
            states (list[tuple]): A list of ball states in the form:
                (x, y, xdot, ydot)
        """
        r = self.env.config["ball"]["radius"]
        for x, y, _, _ in states:
            pygame.time.wait(20)
            ball = Ball(Point(x, y), r)
            self.blit(ball)
            pygame.display.flip()

    def _to_pixels(self, point: Point) -> list[int]:
        """Converts point coordinates from 0-1 to pixel units in screen space.

        Args:
            point (Point): Point to convert to pixel.

        Returns:
            list[int]: Input point location in pixels
        """
        return [
            int(point.x * self.screen.get_width()),
            int(point.y * self.screen.get_height()),
        ]

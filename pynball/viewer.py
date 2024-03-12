# try:
import pygame

# except ImportError as e:
#     print(f"Pygame not available: {e}")
from pynball.pynball_env import PynBall
from pynball.point import Point


class Viewer:  # pylint: disable=too-few-public-methods
    """_summary_"""

    DARK_GREY: list[int] = [64, 64, 64]
    LIGHT_GREY: list[int] = [232, 232, 232]
    BALL_COLOR: list[int] = [0, 0, 255]
    TARGET_COLOR: list[int] = [255, 0, 0]

    def __init__(self, screen: pygame.Surface, env: PynBall) -> None:
        self.screen = screen
        self.env = env
        self.surface = pygame.Surface(screen.get_size())
        self.surface.fill(self.LIGHT_GREY)
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
            int(self.env.target.radius * self.screen.get_width()),
        )
        self.ball_radius = int(self.env.ball.radius * self.screen.get_width())

    def blit(self):
        """Draws the ball onto the surface."""
        self.screen.blit(self.surface, (0, 0))
        pygame.draw.circle(
            self.screen,
            self.BALL_COLOR,
            self._to_pixels(self.env.ball.get_center()),
            self.ball_radius,
        )

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

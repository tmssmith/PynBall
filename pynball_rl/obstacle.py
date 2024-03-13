from abc import ABC, abstractmethod
from pynball_rl.ball import Ball
from pynball_rl.point import Point


class Obstacle(ABC):
    """An interface for obstacles."""

    @abstractmethod
    def collision_effect(self, ball: Ball) -> Point:
        """Returns the new velocity of the ball after a collision with the obstacle.

        Args:
            ball (Ball): The ball.

        Returns:
            Point:  The new velocity.
        """

    @abstractmethod
    def collision(self, ball: Ball) -> bool:
        """Determine whether a collision with the ball has occured.

        Args:
            ball (Ball): The ball.

        Returns:
            bool: True if a collision occured, False otherwise.
        """

    @abstractmethod
    def inside(self, point: Point) -> bool:
        """Determine whether a point is inside the obstacle.

        Args:
            point (Point): The point the test.

        Returns:
            bool: True if the point is inside the obstacle, False otherwise.
        """

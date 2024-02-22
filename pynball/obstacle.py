from abc import ABC, abstractmethod
from pynball import Ball, Point


class Obstacle(ABC):
    """An interface for obstacles."""

    @abstractmethod
    def collision_effect(ball: Ball) -> list[float]:
        """Returns the change in velocity of the ball after a collision with the obstacle.

        Args:
            ball (Ball): The ball.

        Returns:
            list[float]: Change in the ball's X and Y velocities.
        """
        pass

    @abstractmethod
    def collision(ball: Ball) -> bool:
        """Determine whether a collision with the ball has occured.

        Args:
            ball (Ball): The ball.

        Returns:
            bool: True if a collision occured, False otherwise.
        """
        pass

    @abstractmethod
    def get_intercept() -> Point:
        """Get the intercept posiiton of the ball with the obstacle.

        Returns:
            Point: The point of collision.
        """
        pass

    @abstractmethod
    def inside(point: Point) -> bool:
        """Determine whether a point is inside the obstacle.

        Args:
            point (Point): The point the test.

        Returns:
            bool: True if the point is inside the obstacle, False otherwise.
        """
        pass

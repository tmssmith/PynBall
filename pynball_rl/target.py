from pynball_rl.obstacle import Obstacle
from pynball_rl.ball import Ball
from pynball_rl.point import Point


class Target(Obstacle):
    """The goal area in a PinBall game."""

    def __init__(self, point: Point, radius: float) -> None:
        """Creates a new target.

        Args:
            point (Point): center point of the target.
            radius (float): radius of the target.
        """
        self.point = point
        self.radius = radius

    def get_center(self) -> Point:
        """Gets the center of this target.

        Returns:
            Point: The center of this target.
        """
        return self.point

    def collision_effect(self, ball: Ball) -> Point:
        """Returns the change in velocity of the ball after a collision with the target.

        Args:
            ball (Ball): The ball.

        Returns:
            Point: [0.0, 0.0] as the target is absorbing.
        """
        return Point(0.0, 0.0)

    def collision(self, ball: Ball) -> bool:
        """Determine whether a collision with the ball has occurred.

        Args:
            ball (Ball): The ball.

        Returns:
            bool: True if there has been a collision, False otherwise.
        """
        return self.get_center().distance_to(ball.get_center()) < (
            self.radius + ball.radius
        )

    def inside(self, point: Point) -> bool:
        """Determine whether a point is inside the target.

        Args:
            point (Point): The point to test.

        Returns:
            bool: True if the point is inside the target, False otherwise.
        """
        return self.get_center().distance_to(point) < self.radius

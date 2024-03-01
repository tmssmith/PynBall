from . import Ball, Obstacle, Point


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
        return Point(self.x, self.y)

    def collision_effect(ball: Ball) -> list[float]:
        """Returns the change in velocity of the ball after a collision with the target.

        Args:
            ball (Ball): The ball.

        Returns:
            list[float]: [0.0, 0.0] as the target is absorbing.
        """
        return [0.0, 0.0]

    def collision(self, ball: Ball) -> bool:
        """Determine whether a collision with the ball has occured.

        Args:
            ball (Ball): The ball.

        Returns:
            bool: True if there has been a collision, False otherwise.
        """
        return self.get_center().distance_to(ball.get_center()) < self.radius

    def inside(self, point: Point) -> bool:
        """Determine whether a point is inside the target.

        Args:
            point (Point): The point to test.

        Returns:
            bool: True if the point is inside the target, False otherwise.
        """
        return self.get_center().distance_to(point) < self.radius

    def get_intercept() -> Point:
        """Get the intercept of the ball with the target. Returns None

        Returns:
            Point: None
        """
        return None

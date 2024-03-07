import math
from typing import Optional
from . import Ball, Obstacle, Point


class PolygonObstacle(Obstacle):
    """A polygon obstacle.

    Attributes:
        points (list[Point]): A list of points that define the vertices
        of the polygon.
        edges (list[list[Points]]): A list of the edges that make up
        this polygon, each edge represented as point pairs.
        num_collisions (int): Counts the number of collisions between
        the obstacle and a ball.
        intersect_edge (list[Point]): The edge that a ball collided with,
        represented as a pair of points.
    """

    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.edges = [
            [self.points[i], self.points[i - 1]] for i in range(len(self.points))
        ]
        self.compute_bounds()
        self.num_collisions: int = 0
        self.intersect_edge: list[Point] | None = None

    def collision(self, ball: Ball) -> bool:
        if self.outside_bounds(ball.get_center(), ball.radius):
            return False

        self.intersect_edge = None
        self.num_collisions = 0
        for edge in self.edges:
            if self.line_intersect(ball, edge):
                self.intersect_edge = edge
                self.num_collisions += 1

        return self.num_collisions >= 1

    def line_intersect(self, ball: Ball, edge: list[Point]) -> bool:
        # https://math.stackexchange.com/questions/311921/get-location-of-vector-circle-intersection
        # https://mathworld.wolfram.com/QuadraticFormula.html
        # https://math.stackexchange.com/questions/1340267/alternative-quadratic-formula

        p1, p2 = edge
        x0, y0 = p1.x, p1.y
        x1, y1 = p2.x, p2.y
        h, k = ball.x, ball.y
        a = (x1 - x0) ** 2 + (y1 - y0) ** 2
        b = 2 * (x1 - x0) * (x0 - h) + 2 * (y1, y0) * (y0 - k)
        c = (x0 - h) ** 2 + (y0 - k) ** 2 - ball.radius**2
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            # No intersection
            return False
        if discriminant == 0:
            # Tangential intersection, only one intersection point.
            t = (2 * c) / (-b)
            if not 0 < t < 1:
                # Intersection falls outside of the limits of this edge.
                return False
        # Two intersections, which only exist on edge if 0 < t < 1.
        sqrt_discriminant = math.sqrt(discriminant)
        t1 = (2 * c) / (-b + sqrt_discriminant)
        t2 = (2 * c) / (-b - sqrt_discriminant)
        return 0 < t1 < 1 or 0 < t2 < 1

    def collision_effect(self, ball: Ball) -> Point:
        if self.intersect_edge is None or self.num_collisions == 0:
            # No collision detected. This function should never be
            # called if no collisions have occured, but just in case...

            return Point(ball.xdot, ball.ydot)
        if self.num_collisions >= 1:
            # If there are multiple collisions, reverse velocity.
            return Point(-ball.xdot, -ball.ydot)

        ball_v1 = Point(ball.xdot, ball.ydot)
        e = self.intersect_edge[1].minus(self.intersect_edge[0])
        # Get unit vector normal to intersecting edge
        n = Point(e.y, -e.x).normalise()
        # vector reflection
        ball_v2 = ball_v1.minus(n.times(2).times(ball_v1.dot(n)))
        return ball_v2

    def inside(self, point: Point) -> bool:
        """Determines whether a point lies inside the polygon.
        See https://stackoverflow.com/a/23223947 for explanation.

        Args:
            point (Point): Point to test

        Returns:
            bool: True if the point lies inside the polygon, False
            otherwise.
        """

        if self.outside_bounds(point):
            return False

        inside = False

        for edge in self.edges:
            v1, v2 = edge
            if (
                v1.y > point.y != v2.y > point.y
                and point.x < (v2.x - v1.x) * (point.y - v1.y) / (v2.y - v1.y) + v1.x
            ):
                inside = not inside

        return inside

    def compute_bounds(self) -> None:
        """Precomputes a bounding box of the polygon for faster
        collision detection
        """
        min_x = 1.0
        min_y = 1.0
        max_x = 0.0
        max_y = 0.0

        for point in self.points:
            min_x = min(min_x, point.x)
            min_y = min(min_y, point.y)
            max_x = max(max_x, point.x)
            max_y = max(max_y, point.y)
        self.bounds = [min_x, min_y, max_x, max_y]

    def outside_bounds(self, point: Point, radius: Optional[float] = 0.0) -> bool:
        """Determines whether a point, or optionally a circle centered
        on the point, is entirely outside of the bounds of the polygon.

        Args:
            point (Point): The point to test
            radius (Optional[float], optional): If not 0.0, tests for a
            circle of radius centered on the point. Defaults to 0.0.

        Returns:
            bool: True if the point (or circle) lies entirely outside of
            the bounds of the polygon, False otherwise.
        """
        min_x, min_y, max_x, max_y = self.bounds
        return (
            point.x - radius > max_x
            or point.y - radius > max_y
            or point.x + radius < min_x
            or point.y + radius < min_y
        )

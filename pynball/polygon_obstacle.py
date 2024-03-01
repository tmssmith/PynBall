import math
from typing import Optional
from . import Ball, Obstacle, Point
from .utils import clip


class PolygonObstacle(Obstacle):
    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.edges = [[self.points[i], self.points[i - 1]] for i in range(len(self.points))]
        self.compute_bounds()
        self.intersect_point: Point = None

    def select_intercept(a: int, b: int, ball: Ball) -> int:
        pass

    def collision(self, ball: Ball) -> bool:
        if self.outside_bounds(ball.get_center(), ball.radius):
            return False

        self.intersect_point: Point = None
        self.num_collisions = 0
        for edge in self.edges:
            intersect_point = self.line_intersect(ball, edge)
            if intersect_point:
                self.intersect_point = intersect_point
                self.num_collisions += 1

        return self.num_collisions >= 1

    def line_intersect(ball: Ball, edge: list[Point]) -> Point | bool:
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
        elif discriminant == 0:
            # Tangential intersection, only one intersection point.
            t = 2 * c / -b
            if not 0 < t < 1:
                # Intersection point on line falls outside of the limits of this edge.
                return False
        else:
            # Two intersection points, which only exist on this edge for 0 < t < 1.
            sqrt_discriminant = math.sqrt(discriminant)
            t1 = 2 * c / (-b + sqrt_discriminant)
            t2 = 2 * c / (-b - sqrt_discriminant)
            if 0 < t1 < 1:
                if 0 < t2 < 1:
                    # Both intersection points are on this edge, take midpoint as collision point.
                    t = (t1 + t2) / 2
                else:
                    # Only one point lies on this edge.
                    t = t1
            elif 0 < t2 < 1:
                # Only one point lies on this edge.
                t = t2
            else:
                # Intersection points on line falls outside of the limits of this edge.
                return False

        xt = (x1 - x0) * t + x0
        yt = (y1 - y0) * t + y0
        return Point(xt, yt)

    def collision_effect(self, ball: Ball) -> list[float]:
        if self.intersect_point is None or self.num_collisions == 0:
            # No collision detected. This function should never be called if no collisions have occured, but just incase...
            return [ball.xdot, ball.ydot]
        if self.num_collisions >= 1:
            # If there are multiple collisions, reverse velocity.
            return [-ball.xdot, -ball.ydot]

        raise NotImplementedError

    def inside(self, test: Point) -> bool:
        """Determines whether a point lies inside the polygon.
        See https://stackoverflow.com/a/23223947 for explanation.

        Args:
            test (Point): Point to test

        Returns:
            bool: True if the point lies inside the polygon, False otherwise.
        """

        if self.outside_bounds(test):
            return False

        inside = False

        for edge in self.edges:
            v1, v2 = edge
            if v1.y > test.y != v2.y > test.y and test.x < (v2.x - v1.x) * (test.y - v1.y) / (v2.y - v1.y) + v1.x:
                inside = not inside

        return inside

    def compute_bounds(self) -> None:
        self.max_x = 0
        self.max_y = 0
        self.min_x = 1
        self.min_y = 1

        for point in self.points:
            self.max_x = max(self.max_x, point.x)
            self.max_y = max(self.max_y, point.y)
            self.min_x = min(self.min_x, point.x)
            self.min_y = min(self.min_y, point.y)

    def outside_bounds(self, point: Point, radius: Optional[float] = 0.0) -> bool:
        """Determines whether a point, or optionally a circle centered on the point, is entirely outside of the bounds of the polygon.

        Args:
            point (Point): The point to test
            radius (Optional[float], optional): If not 0.0, tests for a circle of this radius centered on the point. Defaults to 0.0.

        Returns:
            bool: True if the point (or circle) lies entirely outside of the bounds of the polygon, False otherwise.
        """

        return (
            point.x - radius > self.max_x
            or point.y - radius > self.max_y
            or point.x + radius < self.min_x
            or point.y + radius < self.min_y
        )

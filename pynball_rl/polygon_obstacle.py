import math
from typing import Optional
from pynball_rl.ball import Ball
from pynball_rl.obstacle import Obstacle
from pynball_rl.point import Point
from pynball_rl.utils import clip_if_close


def line_intersect(ball: Ball, edge: list[Point]) -> bool:
    """Determines whether a ball and an edge intersect.

    Represents the intersection point(s) of an infinite line and the
    circumference of the ball as the roots of a quadratic equation.
    Root is imaginary if the line and circumference do not intersect.
    Intersection(s) are on the edge (i.e a finite section of the
    inifinite line) if either root is between 0 and 1 (inclusive).

    See [1] for algorithmic details. Implementation uses the
    alternative quadratic formula [2].

    [1] https://math.stackexchange.com/questions/311921/get-location-of-vector-circle-intersection
    [2] https://math.stackexchange.com/questions/1340267/alternative-quadratic-formula

    Args:
        ball (Ball): The ball to test.
        edge (list[Point]): The edge to test.

    Returns:
        bool: True if the ball and the line intersect, False otherwise.
    """

    p1, p2 = edge
    assert p1.x != p2.x or p1.y != p2.y, f"Edge is undefined: vertices both equal {p1}."
    a = (p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2
    b = 2 * (p2.x - p1.x) * (p1.x - ball.x) + 2 * (p2.y - p1.y) * (p1.y - ball.y)
    c = (p1.x - ball.x) ** 2 + (p1.y - ball.y) ** 2 - ball.radius**2
    if math.isclose(c, 0.0, abs_tol=1e-12):
        # If c = 0 then t = 0 is a root and so there is an intersection.
        return True
    discriminant = b**2 - 4 * a * c
    if math.isclose(discriminant, 0, abs_tol=1e-12):
        # Tangential intersection, only one intersection point.
        t = clip_if_close((2 * c) / (-b))
        # Intersection is on this edge if 0 < t < 1.
        return 0 <= t <= 1
    if discriminant < 0:
        # No intersection
        return False
    # Two intersections, which only exist on edge if 0 < t < 1.
    sqrt_discriminant = math.sqrt(discriminant)
    t1 = (2 * c) / (-b + sqrt_discriminant)
    t2 = (2 * c) / (-b - sqrt_discriminant)
    return 0 <= clip_if_close(t1) <= 1 or 0 <= clip_if_close(t2) <= 1


def heading_towards(ball: Ball, edge: list[Point]) -> bool:
    """Checks whether a ball is heading towards an edge.

    The edge and ball velocity are represented as infinite lines.
    A scalar `t` representing how far down the velocity vector the
    intersection happens is found using Cramer's rule [1]. If `t>0` the
    ball is heading towards the edge.

    [1] https://math.stackexchange.com/questions/406864/intersection-of-two-lines-in-vector-form

    Args:
        ball (Ball): Ball to test.
        edge (list[Point]): Edge to test.

    Returns:
        bool: _description_
    """
    v = [ball.get_center(), ball.get_velocity()]
    if v[1].size() == 0.0:
        return True
    e = [edge[0], edge[1].minus(edge[0])]
    if v[1].is_parallel_to(e[1]):
        return False
    t = ((e[0].x - v[0].x) * e[1].y - e[1].x * (e[0].y - v[0].y)) / (
        v[1].x * e[1].y - e[1].x * v[1].y
    )

    return t > 0.0


class PolygonObstacle(Obstacle):
    """A polygon obstacle.

    Attributes:
        points (list[Point]): A list of points that define the vertices
        of the polygon.
        edges (list[list[Points]]): A list of the edges that make up
        this polygon, each edge represented as point pairs.
        num_collisions (int): Counts the number of collisions between
        the obstacle and a ball.
        intersect_edges (list[Point]): The edge that a ball collided with,
        represented as a pair of points.
    """

    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.edges = [
            [self.points[i], self.points[i - 1]] for i in range(len(self.points))
        ]
        self.bounds = self.get_bounds()
        self.num_collisions: int = 0
        self.intersect_edges: list[list[Point]] = []

    def collision(self, ball: Ball) -> bool:
        if self.outside_bounds(ball.get_center(), ball.radius):
            return False

        self.intersect_edges = []
        self.num_collisions = 0
        for edge in self.edges:
            if heading_towards(ball, edge) and line_intersect(ball, edge):
                if not self.intersect_edges:
                    self.intersect_edges.append(edge)
                    self.num_collisions += 1
                elif not self.any_parallel(edge, self.intersect_edges):
                    # Only consider edge intersect if no parallel edge
                    # intersections detected.
                    self.intersect_edges.append(edge)
                    self.num_collisions += 1

        return self.num_collisions >= 1

    def any_parallel(self, edge: list[Point], edges: list[list[Point]]) -> bool:
        """Checks if an edge is parallel to any of the input edges.

        Args:
            edge (list[Point]): Edge to check.
            edges (list[list[Point]]): List of edges to compare against.

        Returns:
            bool: True if none of the edges are parallel, False otherwise.
        """
        for test in edges:
            if test[1].minus(test[0]).is_parallel_to(edge[1].minus(edge[0])):
                return True
        return False

    def collision_effect(self, ball: Ball) -> Point:
        """Returns the new velocity of the ball after a collision with the obstacle.

        Must be called after PolygonObstacle.collision
        Uses the reflection vector of the ball velocity [1].

        [1] https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector

        Args:
            ball (Ball): The ball.

        Returns:
            Point: The new velocity.
        """
        assert (
            self.num_collisions != 0.0
        ), "No collisions detected, did you call .collision() first?"

        if self.num_collisions > 1:
            # If there are multiple collisions, reverse velocity.
            return Point(-ball.xdot, -ball.ydot)

        ball_v1 = Point(ball.xdot, ball.ydot)
        intersect_edge = self.intersect_edges[0]
        e = intersect_edge[1].minus(intersect_edge[0])
        # Get unit vector normal to intersecting edge
        n = Point(e.y, -e.x).normalise()
        # vector reflection
        ball_v2 = ball_v1.minus(n.times(2).times(ball_v1.dot(n)))
        return ball_v2

    def inside(self, point: Point) -> bool:
        """Determines whether a point lies inside the polygon.

        See https://stackoverflow.com/a/23223947 for explanation.
        Currently unused, should probably remove.

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
            if (v1.y > point.y) != (v2.y > point.y) and point.x < (v2.x - v1.x) * (
                point.y - v1.y
            ) / (v2.y - v1.y) + v1.x:
                inside = not inside

        return inside

    def get_bounds(self) -> list[float]:
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

        return [min_x, min_y, max_x, max_y]

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
            point.x + radius < min_x
            or point.y + radius < min_y
            or point.x - radius > max_x
            or point.y - radius > max_y
        )

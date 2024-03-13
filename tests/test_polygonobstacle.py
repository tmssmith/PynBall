# pylint: disable=missing-function-docstring

"""Test suite for the PolygonObstacle class.

Tests include:
    - Initiation of edges from points.
    - Bounds for square, triangle, and diamond obstacles.
    - Line intersect for vertical, horizontal and angled edges.
    - Line intersect from all directions (outside polygon).
    - Collision detection for vertical, horizontal and angled edges.
    - Collision detection from all directions (outside polygon).
    - Collision effect for vertical, horizontal and angled edges.
    - Collision effect from all directions (outside polygon).
"""

import math
import pytest
from pynball import PolygonObstacle, Ball, Point
from pynball.polygon_obstacle import line_intersect, heading_towards


@pytest.fixture(name="square_obstacle")
def square_obstacle_fixture():
    p1 = Point(0.4, 0.4)
    p2 = Point(0.6, 0.4)
    p3 = Point(0.6, 0.6)
    p4 = Point(0.4, 0.6)
    return PolygonObstacle([p1, p2, p3, p4])


@pytest.fixture(name="diamond_obstacle")
def diamond_obstacle_fixture():
    p1 = Point(0.5, 0.6)
    p2 = Point(0.4, 0.5)
    p3 = Point(0.5, 0.4)
    p4 = Point(0.6, 0.5)
    return PolygonObstacle([p1, p2, p3, p4])


@pytest.fixture(name="triangle_obstacle")
def triangle_obstacle_fixture():
    p1 = Point(0.5, 0.6)
    p2 = Point(0.3, 0.4)
    p3 = Point(0.7, 0.4)
    return PolygonObstacle([p1, p2, p3])


def test_square_obstacle(square_obstacle):
    edges = square_obstacle.edges
    assert len(edges) == 4
    assert square_obstacle.bounds == [0.4, 0.4, 0.6, 0.6]
    assert square_obstacle.inside(Point(0.5, 0.5)) is True
    assert square_obstacle.inside(Point(0.45, 0.55)) is True
    assert square_obstacle.inside(Point(0.55, 0.45)) is True
    assert square_obstacle.inside(Point(0.3, 0.3)) is False
    assert square_obstacle.inside(Point(0.5, 0.3)) is False
    assert square_obstacle.inside(Point(0.3, 0.5)) is False
    assert square_obstacle.inside(Point(0.5, 0.7)) is False
    assert square_obstacle.inside(Point(0.7, 0.5)) is False


def test_diamond_obstacle(diamond_obstacle):
    edges = diamond_obstacle.edges
    assert len(edges) == 4
    assert diamond_obstacle.bounds == [0.4, 0.4, 0.6, 0.6]
    assert diamond_obstacle.inside(Point(0.5, 0.5)) is True
    assert diamond_obstacle.inside(Point(0.45, 0.51)) is True
    assert diamond_obstacle.inside(Point(0.52, 0.45)) is True
    assert diamond_obstacle.inside(Point(0.3, 0.3)) is False
    assert diamond_obstacle.inside(Point(0.5, 0.3)) is False
    assert diamond_obstacle.inside(Point(0.3, 0.5)) is False
    assert diamond_obstacle.inside(Point(0.5, 0.7)) is False
    assert diamond_obstacle.inside(Point(0.7, 0.5)) is False


def test_triangle_obstacle(triangle_obstacle):
    edges = triangle_obstacle.edges
    assert len(edges) == 3
    assert triangle_obstacle.bounds == [0.3, 0.4, 0.7, 0.6]
    assert triangle_obstacle.inside(Point(0.5, 0.5)) is True
    assert triangle_obstacle.inside(Point(0.45, 0.53)) is True
    assert triangle_obstacle.inside(Point(0.55, 0.45)) is True
    assert triangle_obstacle.inside(Point(0.3, 0.3)) is False
    assert triangle_obstacle.inside(Point(0.5, 0.3)) is False
    assert triangle_obstacle.inside(Point(0.3, 0.5)) is False
    assert triangle_obstacle.inside(Point(0.5, 0.7)) is False
    assert triangle_obstacle.inside(Point(0.7, 0.5)) is False


def test_square_obstacle_intersect(square_obstacle):
    edge = square_obstacle.edges[0]
    ball_1 = Ball(Point(0.1, 0.1), 0.1)  # 'Outside' edge -> False
    ball_2 = Ball(Point(0.5, 0.5), 0.05)  # 'Inside' edge -> False
    ball_3 = Ball(Point(0.1, 0.1), 0.43)
    ball_4 = Ball(Point(0.3, 0.4), 0.15)
    ball_5 = Ball(Point(0.3, 0.5), 0.1)  # Tangential -> True
    ball_6 = Ball(Point(0.4, 0.3), 0.1)  # Vertex intersect at 0 -> True
    ball_7 = Ball(Point(0.4, 0.7), 0.1)  # Vertex intersect at 1 -> True
    assert line_intersect(ball_1, edge) is False
    assert line_intersect(ball_2, edge) is False
    assert line_intersect(ball_3, edge) is True
    assert line_intersect(ball_4, edge) is True
    assert line_intersect(ball_5, edge) is True
    assert line_intersect(ball_6, edge) is True
    assert line_intersect(ball_7, edge) is True

    edge = square_obstacle.edges[1]
    ball_1 = Ball(Point(0.1, 0.1), 0.1)  # 'Outside' edge -> False
    ball_2 = Ball(Point(0.5, 0.5), 0.05)  # 'Inside' edge -> False
    ball_3 = Ball(Point(0.1, 0.1), 0.43)
    ball_4 = Ball(Point(0.3, 0.4), 0.15)
    ball_5 = Ball(Point(0.6, 0.3), 0.1)  # Vertex intersect at 0 -> True
    ball_6 = Ball(Point(0.4, 0.3), 0.1)  # Vertex intersect at 1 -> True
    assert line_intersect(ball_1, edge) is False
    assert line_intersect(ball_2, edge) is False
    assert line_intersect(ball_3, edge) is True
    assert line_intersect(ball_4, edge) is True
    assert line_intersect(ball_5, edge) is True
    assert line_intersect(ball_6, edge) is True


def test_square_obstacle_heading_towards(square_obstacle):
    ball = Ball(Point(-0.2, 0.1), 0.01)

    ball.set_velocity(Point(0, 0))
    for edge in square_obstacle.edges:
        assert heading_towards(ball, edge) is False

    ball.set_velocity(Point(-1, 0))
    for edge in square_obstacle.edges:
        assert heading_towards(ball, edge) is False

    ball.set_velocity(Point(1, 1))
    for edge in square_obstacle.edges:
        print(f"({edge[0]}), ({edge[1]})")
        assert heading_towards(ball, edge) is True

    ball.set_velocity(Point(1, 0))
    for edge in square_obstacle.edges:
        if edge[1].minus(edge[0]).is_parallel_to(ball.get_velocity()):
            assert heading_towards(ball, edge) is False
        else:
            assert heading_towards(ball, edge) is True

    ball.set_velocity(Point(0, 1))
    for edge in square_obstacle.edges:
        if edge[1].minus(edge[0]).is_parallel_to(ball.get_velocity()):
            assert heading_towards(ball, edge) is False
        else:
            assert heading_towards(ball, edge) is True

    ball.set_velocity(Point(0, -1))
    for edge in square_obstacle.edges:
        assert heading_towards(ball, edge) is False


def test_square_collision(square_obstacle):
    ball_1 = Ball(Point(0.1, 0.1), 0.1)  # 'Outside' shape -> False
    ball_2 = Ball(Point(0.5, 0.5), 0.05)  # 'Inside' shape -> False
    ball_3 = Ball(Point(0.1, 0.1), 0.43)
    ball_4 = Ball(Point(0.3, 0.4), 0.1)
    ball_5 = Ball(Point(0.6, 0.3), 0.1)  # Vertex intersect at 0 -> True
    ball_6 = Ball(Point(0.4, 0.3), 0.1)  # Vertex intersect at 1 -> True
    ball_7 = Ball(Point(0.7, 0.5), 0.1)
    ball_8 = Ball(Point(0.5, 0.65), 0.1)
    assert square_obstacle.collision(ball_1) is False
    assert square_obstacle.collision(ball_2) is False
    assert square_obstacle.collision(ball_3) is True
    assert square_obstacle.collision(ball_4) is True
    assert square_obstacle.collision(ball_5) is True
    assert square_obstacle.collision(ball_6) is True
    assert square_obstacle.collision(ball_7) is True
    assert square_obstacle.collision(ball_8) is True


def test_any_parallel(square_obstacle):
    e1 = [Point(0, 0), Point(1, 0)]
    e2 = [Point(-1, 1), Point(5, 1)]
    e3 = [Point(0, 3), Point(1, 4)]
    assert square_obstacle.any_parallel(e1, [e2]) is True
    assert square_obstacle.any_parallel(e1, [e3]) is False
    assert square_obstacle.any_parallel(e1, [e2, e3]) is True
    e = square_obstacle.edges[0]
    assert square_obstacle.any_parallel(e, square_obstacle.edges[1:])


def test_square_collision_effect_1(square_obstacle):
    """Test a direct rightwards collision."""
    ball = Ball(Point(0.3, 0.5), 0.1)
    ball.set_velocity(Point(0.4, 0.0))
    square_obstacle.collision(ball)
    v = square_obstacle.collision_effect(ball)
    assert v.x == -0.4 and v.y == 0.0


def test_square_collision_effect_2(square_obstacle):
    """Test a rightwards collision"""
    ball = Ball(Point(0.3, 0.5), 0.1)
    ball.set_velocity(Point(0.1, 0.1))
    square_obstacle.collision(ball)
    v = square_obstacle.collision_effect(ball)
    assert v.x == -0.1 and v.y == 0.1


def test_square_collision_effect_3(square_obstacle):
    """Test a rightwards collision"""
    ball = Ball(Point(0.3, 0.5), 0.1)
    ball.set_velocity(Point(0.2, -0.1))
    square_obstacle.collision(ball)
    v = square_obstacle.collision_effect(ball)
    assert v.x == -0.2 and v.y == -0.1


def test_square_collision_effect_4(square_obstacle):
    """Test a double collision."""
    ball = Ball(Point(0.6, 0.3), 0.1)
    ball.set_velocity(Point(0.2, -0.1))
    square_obstacle.collision(ball)
    # Double collision
    v = square_obstacle.collision_effect(ball)
    assert v.x == -0.2 and v.y == 0.1


def test_square_collision_effect_5(square_obstacle):
    """Test an upwards collision."""
    ball = Ball(Point(0.5, 0.3), 0.1)
    ball.set_velocity(Point(0.2, 0.1))
    square_obstacle.collision(ball)
    v = square_obstacle.collision_effect(ball)
    assert v.x == 0.2 and v.y == -0.1


def test_square_collision_effect_6(square_obstacle):
    """Test a leftwards collision."""
    ball = Ball(Point(0.7, 0.5), 0.1)
    ball.set_velocity(Point(-0.2, 0.1))
    square_obstacle.collision(ball)
    v = square_obstacle.collision_effect(ball)
    assert v.x == 0.2 and v.y == 0.1


def test_square_collision_effect_7(square_obstacle):
    """Test a downwards collision."""
    ball = Ball(Point(0.5, 0.7), 0.1)
    ball.set_velocity(Point(-0.2, -0.1))
    square_obstacle.collision(ball)
    v = square_obstacle.collision_effect(ball)
    assert v.x == -0.2 and v.y == 0.1


def test_diamond_collision_effect_1(diamond_obstacle):
    """Test a direct rightwards collision."""
    ball = Ball(Point(0.4, 0.6), 0.08)
    ball.set_velocity(Point(0.4, 0.0))
    diamond_obstacle.collision(ball)
    v = diamond_obstacle.collision_effect(ball)
    assert (
        math.isclose(v.x, 0.0, abs_tol=1e-12) is True and math.isclose(v.y, 0.4) is True
    )


def test_diamond_collision_effect_2(diamond_obstacle):
    """Test a direct downwards collision."""
    ball = Ball(Point(0.4, 0.6), 0.08)
    ball.set_velocity(Point(0.0, -0.2))
    diamond_obstacle.collision(ball)
    v = diamond_obstacle.collision_effect(ball)
    assert (
        math.isclose(v.x, -0.2) is True and math.isclose(v.y, 0, abs_tol=1e-12) is True
    )

# pylint: disable=missing-function-docstring

import math
import pytest
from pynball import Point, Ball


@pytest.fixture(name="ball")
def ball_fixture():
    p = Point(0.1, 0.1)
    return Ball(p, 0.1)


def test_ball(ball):
    center = ball.get_center()
    assert isinstance(center, Point)
    assert center.x == 0.1 and center.y == 0.1
    assert ball.get_speed() == 0.0
    ball.set_velocity(Point(1.0, 0.0))
    assert ball.get_speed() == 1.0
    for _ in range(20):
        ball.step(20)
    assert ball.xdot == 1.0
    target = 0.1 + 20 * 0.1 / 20
    assert math.isclose(ball.x, target)
    assert ball.y == 0.1


def test_set_position(ball):
    ball.set_velocity(Point(1.0, 0.5))
    ball.set_position(0.5, 0.5)
    assert ball.x == 0.5 and ball.y == 0.5
    assert ball.xdot == 0.0 and ball.ydot == 0.0


def test_drag(ball):
    ball.set_velocity(Point(1.0, 0))
    ball.add_drag(0.995)
    assert ball.xdot == 0.995 and ball.ydot == 0.0


def test_impulse(ball):
    ball.add_impulse(1.0, 0.0)
    assert ball.xdot == 0.2 and ball.ydot == 0.0
    ball.add_impulse(10.0, 0.0)
    assert ball.xdot == 1.0 and ball.ydot == 0.0
    ball.add_impulse(0.0, 2.0)
    assert ball.xdot == 1.0 and ball.ydot == 0.4

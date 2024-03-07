from pynball import Target, Point, Ball
import pytest


@pytest.fixture(name="target")
def target_fixture():
    point = Point(0.1, 0.1)
    return Target(point, 0.1)


@pytest.fixture(name="ball")
def target_ball():
    point = Point(0.1, 0.1)
    return Ball(point, 0.1)


def test_inside(target):
    outside = [Point(0.2, 0.1), Point(0.0, 0.0)]
    inside = [Point(0.1, 0.1), Point(0.14, 0.14), Point(0.15, 0.1)]
    for point in outside:
        assert target.inside(point) is False
    for point in inside:
        assert target.inside(point) is True


def test_collision(target, ball):
    assert target.collision(ball) is True
    ball.set_position(0.1, 0.2)
    assert target.collision(ball) is True
    ball.set_position(0.1, 0.31)
    assert target.collision(ball) is False

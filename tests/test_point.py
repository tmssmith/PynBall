import math
import pytest
from pynball import Point


@pytest.fixture(name="first_point")
def first_point_fixture():
    return Point(0, 0)


@pytest.fixture(name="second_point")
def second_point_fixture():
    return Point(1, 1)


@pytest.fixture(name="third_point")
def third_point_fixture():
    return Point(-1, 0)


def test_add(first_point, second_point, third_point):
    p1 = first_point.add(second_point)
    assert isinstance(p1, Point)
    assert p1.x == 1 and p1.y == 1
    p2 = second_point.add(first_point)
    assert isinstance(p2, Point)
    assert p2.x == 1 and p2.y == 1
    p3 = first_point.add(third_point)
    assert isinstance(p3, Point)
    assert p3.x == -1 and p3.y == 0
    p4 = first_point.add(first_point)
    assert isinstance(p4, Point)
    assert p4.x == 0 and p4.y == 0


def test_point(first_point, second_point, third_point):
    assert first_point.x == 0
    assert first_point.y == 0
    assert second_point.x == 1
    assert second_point.y == 1
    assert third_point.x == -1
    assert third_point.y == 0


def test_minus(first_point, second_point, third_point):
    p1 = first_point.minus(second_point)
    assert isinstance(p1, Point)
    assert p1.x == -1
    assert p1.y == -1
    p2 = second_point.minus(first_point)
    assert isinstance(p2, Point)
    assert p2.x == 1
    assert p2.y == 1
    p3 = first_point.minus(third_point)
    assert isinstance(p3, Point)
    assert p3.x == 1
    assert p3.y == 0


def test_times(first_point, second_point, third_point):
    multipliers = [0, 5, -1, 5.2, -7 / 11]
    for multiplier in multipliers:
        res1 = first_point.times(multiplier)
        assert isinstance(res1, Point)
        res2 = first_point.times(multiplier)
        assert isinstance(res2, Point)
        res3 = first_point.times(multiplier)
        assert isinstance(res3, Point)


def test_dot(first_point, second_point, third_point):
    assert first_point.dot(third_point) == 0.0
    assert first_point.dot(first_point) == 0.0
    assert third_point.dot(third_point) == 1.0
    assert first_point.dot(second_point) == second_point.dot(first_point)


def test_add_point_to(first_point, second_point, third_point):
    first_point.add_point_to(second_point)
    assert first_point.x == 1 and first_point.y == 1
    second_point.add_point_to(first_point)
    assert second_point.x == 2 and second_point.y == 2
    third_point.add_point_to(first_point)
    assert third_point.x == 0 and third_point.y == 1
    second_point.add_point_to(second_point)
    assert second_point.x == 4 and second_point.y == 4


def test_distance(first_point, second_point, third_point):
    assert first_point.distance_to(second_point) == math.sqrt(2)
    assert second_point.distance_to(first_point) == math.sqrt(2)
    assert first_point.distance_to(third_point) == 1.0
    assert third_point.distance_to(first_point) == 1.0
    assert second_point.distance_to(third_point) == math.sqrt(5)

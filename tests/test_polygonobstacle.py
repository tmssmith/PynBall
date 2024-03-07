import pytest
from pynball import PolygonObstacle, Ball, Point


@pytest.fixture(name="obstacle")
def obstacle_fixture():
    # p1 = Point()
    # p2 = Point()
    # p3 = Point()
    return PolygonObstacle([p1, p2, p3])

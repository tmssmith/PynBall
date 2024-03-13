# pylint: disable=missing-function-docstring

from pathlib import Path
import random

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from pynball_rl import PolygonObstacle, Point, Ball, Target

CONFIG_PATH = "pynball_rl/configs/easy_config.toml"


def test_config(config_path=CONFIG_PATH):
    config_path = Path(config_path)
    with open(config_path, "rb") as fb:
        config = tomllib.load(fb)
    assert config["seed"] == 12345
    obstacles = [
        PolygonObstacle([Point(*p) for p in obstacle["points"]])
        for obstacle in config["obstacles"]
    ]
    print(obstacles)
    assert len(obstacles) == 10
    x, y = random.choice(config["ball"]["starts"])
    assert x == 0.2 and y == 0.9
    radius = config["ball"]["radius"]
    assert radius == 0.02
    ball = Ball(Point(*random.choice(config["ball"]["starts"])), radius)
    print(ball)

    target = Target(Point(*config["target"]["location"]), config["target"]["radius"])
    print(target)
    assert target.radius == 0.04
    assert target.get_center().x == 0.9 and target.get_center().y == 0.2

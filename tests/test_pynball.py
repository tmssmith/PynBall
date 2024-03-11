# pylint: disable=missing-function-docstring

import math
import pytest
from pynball import PynBall


@pytest.fixture(name="env")
def env_fixture():
    return PynBall("config.toml")


def test_init(env):
    assert env.step_duration == 20
    assert env.drag == 0.995
    with pytest.raises(AssertionError):
        env.step(4)


def test_reset(env):
    s = env.reset()
    assert env.reset_flag is True
    assert s == (0.2, 0.9, 0.0, 0.0)


def test_terminal(env):
    env.reset()
    assert env.terminal() is False
    env.ball.set_position(0.9, 0.2)
    assert env.terminal() is True


def test_step(env):
    env.reset()
    s, r, t, _ = env.step(4)
    assert s == (0.2, 0.9, 0.0, 0.0)
    assert r == -1.0
    assert t is False
    s, r, t, _ = env.step(0)
    assert math.isclose(s[0], 0.02 / 5 + 0.2) is True
    assert s[1] == 0.9
    assert math.isclose(s[2], 1 / 5 * 0.995) is True
    assert s[3] == 0.0
    assert r == -5.0
    assert t is False


def test_bounds(env):
    env.reset()
    env.check_bounds()
    env.ball.set_position(1.1, -0.1)
    with pytest.raises(RuntimeError):
        env.check_bounds()
    env.ball.set_position(1.1, 0.1)
    with pytest.raises(RuntimeError):
        env.check_bounds()
    env.ball.set_position(0.1, -2.1)
    with pytest.raises(RuntimeError):
        env.check_bounds()
    env.ball.set_position(-0.1, -0.1)
    with pytest.raises(RuntimeError):
        env.check_bounds()
    env.ball.set_position(-0.1, 0.21)
    with pytest.raises(RuntimeError):
        env.check_bounds()

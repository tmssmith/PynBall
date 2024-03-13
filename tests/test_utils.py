# pylint: disable=missing-function-docstring

import pytest
from pynball_rl.utils import clip

TEST_VALUES = [-100, -1.5, 0, 1.5, 50, 1e3, 5 / 83]
TEST_BOUNDS = [[0, 1], [-1, 1], [-100, -50], [0, 1e-3], [1, 5]]


def test_clip_defaults():
    for value in TEST_VALUES:
        assert 0.0 <= clip(value) <= 1.0


def test_clip_invalid_range():
    for value in TEST_VALUES:
        with pytest.raises(AssertionError):
            clip(value, 1, 0)
            clip(value, 0, 0)
            clip(value, "", None)


def test_clip_arguments():
    for value in TEST_VALUES:
        for lower, upper in TEST_BOUNDS:
            assert lower <= clip(value, lower, upper) <= upper

import math


def clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """A helper function to clip a variable.

    Args:
        value (float): Variable to clip.
        low (float, optional): Lower bound. Defaults to 0.0.
        high (float, optional): Upper bound. Defaults to 1.0.

    Returns:
        float: Clipped value.
    """
    assert low < high, "Lower bound is greater than upper bound."
    if value <= low:
        return low
    if value >= high:
        return high
    return value


def clip_if_close(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Clips a value to bounds if it's close to the bounds.

    Args:
        value (float): Value to clip.
        low (float, optional): Lower bound. Defaults to 0.0.
        high (float, optional): Upper bound. Defaults to 1.0.

    Returns:
        float: Clipped value
    """
    assert low < high, "Lower bound is greater than upper bound."
    if math.isclose(value, low, abs_tol=1e-12):
        return low
    if math.isclose(value, high, abs_tol=1e-12):
        return high
    return value

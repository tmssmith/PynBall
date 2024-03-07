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
    if value >= high:
        return high
    elif value <= low:
        return low
    else:
        return value

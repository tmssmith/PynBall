def clip(value: float, low: float, high: float) -> float:
    """A helper function to clip a variable.

    Args:
        value (float): variable to clip.
        low (float): lower bound.
        high (float): upper bound.

    Returns:
        float: Clipped value.
    """
    if value >= high:
        return high
    elif value <= low:
        return low
    else:
        return value

from pynball import Point
import math

DRAG = 0.995


class Ball:
    def __init__(self, p: Point, radius: float) -> None:
        """Constructs a new ball given a point and radius. Velocities are set to zero.

        Args:
            p (Point): X and Y coordinates of the ball.
            radius (float): ball radius.
        """
        self.x = p.x
        self.y = p.y
        self.xdot = 0.0
        self.ydot = 0.0
        self.radius = radius

    def step(self) -> None:
        """Moves the ball one step forward."""
        self.x += self.xdot * self.radius / 20.0
        self.y += self.ydot * self.radius / 20.0

    def addDrag(self) -> None:
        """Applies drag to the ball."""
        self.xdot *= DRAG
        self.ydot *= DRAG

    def get_velocity(self) -> float:
        """Returns the ball's speed.

        Returns:
            float: The speed of the ball.
        """
        p = Point(self.xdot, self.ydot)
        return p.size()

    def add_impulse(self, x_impulse: float, y_impulse: float) -> None:
        """Add a velocity impulse to the ball.

        Args:
            x_impulse (float): Impulse to add to xdot
            y_impulse (float): Impulse to add to ydot
        """
        self.xdot += x_impulse / 5.0
        self.ydot += y_impulse / 5.0

        self.xdot = clip(self.xdot, -1.0, 1.0)
        self.ydot = clip(self.ydot, -1.0, 1.0)

    def set_velocities(self, xdot: float, ydot: float) -> None:
        """Set the velocity of the ball.

        Args:
            xdot (float): X velocity to set.
            ydot (float): Y velocity to set.
        """
        self.xdot = xdot
        self.ydot = ydot

    def set_position(self, x: float, y: float) -> None:
        """Set the position of the ball. Sets velocity to zero.

        Args:
            x (float): X position to set.
            y (float): Y position to set.
        """
        self.x = x
        self.y = y
        self.xdot = 0.0
        self.ydot = 0.0

    def get_center(self) -> Point:
        """Get the center point of the ball.

        Returns:
            Point: A point corresponding to the center of the ball.
        """
        return Point(self.x, self.y)


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

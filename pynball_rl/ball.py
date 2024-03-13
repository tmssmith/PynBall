from pynball_rl.point import Point
from pynball_rl.utils import clip


class Ball:
    """A ball in the pinball domain.

    Attribute:
        x (float): X coordinate of the ball
        y (float): Y coordinate of the ball
        xdot (float): X velocity of the ball
        ydot (float): Y velocity of the ball
        radius (float): Ball radius
    """

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

    def step(self, step_duration) -> None:
        """Moves the ball one inner-step forward."""
        self.x += self.xdot * self.radius / step_duration
        self.y += self.ydot * self.radius / step_duration

    def add_drag(self, drag: float) -> None:
        """Applies drag to the ball."""
        self.xdot *= drag
        self.ydot *= drag

    def get_speed(self) -> float:
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

    def set_velocity(self, velocity: Point) -> None:
        """Set the velocity of the ball.

        Args:
            velocity (Point): Point vector of velocity to set.
        """
        self.xdot = velocity.x
        self.ydot = velocity.y

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

    def get_velocity(self) -> Point:
        """Get the velocity vector of the ball.

        Returns:
            Point: A point corresponding to the velocity of the ball.
        """
        return Point(self.xdot, self.ydot)

    def __str__(self):
        return f"{str(self.get_center())}, {self.get_velocity}"

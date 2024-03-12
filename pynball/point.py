import math


class Point:
    """Represents a 2D point.

    Attributes:
        x (float): X coordinate
        y (float): Y coordinate
    """

    def __init__(self, x: float, y: float) -> None:
        """Initialises the instance based on x and y coordinates.

        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
        """
        self.x = x
        self.y = y

    def add(self, point: "Point") -> "Point":
        """Get a new point that is this point plus the given point.

        Args:
            point (Point): The point to add.

        Returns:
            Point: The new point
        """
        return Point(self.x + point.x, self.y + point.y)

    def minus(self, point: "Point") -> "Point":
        """Get a new point that is the difference between this point and another.

        Args:
            point (Point): The point to subtract.

        Returns:
            Point: The new point.
        """
        return Point(self.x - point.x, self.y - point.y)

    def times(self, a: float) -> "Point":
        """Get a new point that is `a` times this point.

        Args:
            a (float): Multiplier.

        Returns:
            Point: The new point.
        """
        return Point(self.x * a, self.y * a)

    def dot(self, point: "Point") -> float:
        """Get the dot product of this point and a given point.

        Args:
            point (Point): The other point.

        Returns:
            float: The dot product between this point and the given point.
        """
        return (self.x * point.x) + (self.y * point.y)

    def add_point_to(self, point: "Point") -> "Point":
        """Add another point to this point.

        Args:
            point (Point): The other point.
        Returns:
            Point: This point.
        """
        self.x += point.x
        self.y += point.y
        return self

    def size(self) -> float:
        """Return the length of the vector corresponding to this point.

        Returns:
            float: The size of the vector corresponding to this point.
        """
        return math.sqrt(self.dot(self))

    def normalise(self) -> "Point":
        """Get a normalised version of this point.

        Returns:
            Point: A normalised version of this point.
        """
        norm = self.size()
        return Point(self.x / norm, self.y / norm)

    def distance_to(self, point: "Point") -> float:
        """Get the distance from this point to a given point.

        Args:
            point (Point): The other point.

        Returns:
            float: Distance from this point to the given point point.
        """
        distance = math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)
        return distance

    def is_parallel_to(self, point: "Point") -> bool:
        """Checks if the vector of this point is parallel to input point.

        Args:
            point (Point): The other point.

        Returns:
            bool: True if parallel, False otherwise.
        """
        return self.x * point.y == self.y * point.x

    def angle_between(self, point: "Point") -> float:
        """Compute the angle between this point and another.

        Args:
            point (Point): The other point.

        Returns:
            float: The angle between the vectors to the two points in radians.
        """
        angle = math.atan2(point.y, point.x) - math.atan2(self.y, self.x)
        if angle < 0:
            # Force angle in range 0 - 2$\pi$
            angle += 2 * math.pi
        return angle

    def __str__(self):
        return f"{self.x}, {self.y}"

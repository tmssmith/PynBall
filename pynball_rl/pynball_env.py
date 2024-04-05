import random
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from pynball_rl.point import Point
from pynball_rl.ball import Ball
from pynball_rl.polygon_obstacle import PolygonObstacle
from pynball_rl.target import Target


class PynBall:
    """A Pinball game domain.

    Attributes:
        config (dict): Configuration parameters.
        step_duration (int): The number of inner-steps per step.
        drag (float): Drag factor applied to ball each step.
        obstacles (list[PolygonObstacle]): Obstacles in the environment.
        target (Target): Target instance of the environment.
        ball (Ball): The ball that travels in the environment.
        reset_flag (bool): Tracks whether the environment has been reset.
    """

    ACTION_DICT = {
        0: (1.0, 0.0),
        1: (0.0, 1.0),
        2: (-1.0, 0.0),
        3: (0.0, -1.0),
        4: (0.0, 0.0),
    }
    # ACC_X, ACC_Y, DEC_X, DEC_Y, NOOP

    THRUST_PENALTY = -5.0
    NOP_PENALTY = -1.0
    GOAL_REWARD = 10_000

    def __init__(
        self,
        config_path: Path,
        exploration: bool = False,
    ) -> None:

        self.exploration = exploration
        with open(config_path, "rb") as fb:
            self.config = tomllib.load(fb)

        random.seed(self.config.get("seed", 42))
        self.step_duration: int = self.config.get("step_duration", 20)
        self.drag: float = self.config.get("drag", 0.995)
        self.stddev_x: float = self.config.get("stddev_x", 0.0)
        self.stddev_y: float = self.config.get("stddev_y", 0.0)
        self.allow_noop: bool = self.config.get("allow_noop", True)
        self.action_space = range(5) if self.allow_noop else range(4)
        self.obstacles = [
            PolygonObstacle([Point(*point) for point in obstacle["points"]])
            for obstacle in self.config["obstacles"]
        ]

        self.target = Target(
            Point(*self.config["target"]["location"]), self.config["target"]["radius"]
        )

        self.reset_flag: bool = False
        self.ball: Ball | None = None

    def reset(self, starting_ball: Ball | None = None) -> tuple:
        """Resets the environment.

        An optional argument allows a Ball object to be provided.
        Otherwise, a ball with zero velocity is created at one of the
        start locations in the config file.

        Args:
            starting_ball (Ball | None, optional): Ball to reset the
            environment with. Defaults to None.

        Returns:
            tuple: Current state as (ball.x, ball.y, ball.xdot, ball.ydot).
        """
        if starting_ball is None:
            self.ball = Ball(
                p=Point(*random.choice(self.config["ball"]["starts"])),
                radius=self.config["ball"]["radius"],
            )
        else:
            self.ball = starting_ball
        self.reset_flag = True
        return (self.ball.x, self.ball.y, self.ball.xdot, self.ball.ydot)

    def terminal(self) -> bool:
        """Checks if the the environment is in a terminal state.

        State is terminal if the ball has collided with the environment.

        Returns:
            bool: True if the state is terminal, False otherwise.
        """
        return self.target.collision(self.ball) and not self.exploration

    def step(self, action: int) -> tuple:
        """Advances the environment one timestep.

        Each timestep is divided into `self.step_duration` inner steps.
        Each inner step, all obstacles are checked for collision and the
        velocity updated accordingly.
        Drag is added after all inner steps are complete.

        Args:
            action (int): Action to take. Used as key for ACTION_DICT:
            0: ACC_X, 1: ACC_Y, 2: DEC_X, 3: DEC_Y, 4: NOP

        Returns:
            tuple: (state, reward, terminal, info)
        """
        assert self.reset_flag is True, "Environment requires resetting."
        if action == 4:
            impulse = (0.0, 0.0)
            reward = self.NOP_PENALTY
        else:
            x_imp, y_imp = self.ACTION_DICT[action]
            impulse = (
                random.gauss(x_imp, self.stddev_x),
                random.gauss(y_imp, self.stddev_y),
            )
            reward = self.THRUST_PENALTY
        terminal = False
        self.ball.add_impulse(*impulse)
        for i in range(self.step_duration):
            num_collisions = 0
            collidor: PolygonObstacle = None
            self.ball.step(self.step_duration)

            for obstacle in self.obstacles:
                if obstacle.collision(self.ball):
                    num_collisions += 1
                    collidor = obstacle

            if num_collisions == 1:
                new_vel = collidor.collision_effect(self.ball)
                self.ball.set_velocity(new_vel)
                if i == self.step_duration - 1:
                    # Add a bonus step to ensure ball bounces away from obstacle.
                    self.ball.step(self.step_duration)
            elif num_collisions > 1:
                # If there are multiple collisions, reverse velocity.
                new_vel = Point(-self.ball.xdot, -self.ball.ydot)
                self.ball.set_velocity(new_vel)

            if self.terminal():
                terminal = True
                self.reset_flag = False
                reward += self.GOAL_REWARD
                break

        self.ball.add_drag(self.drag)
        self._check_bounds()
        current_state = (self.ball.x, self.ball.y, self.ball.xdot, self.ball.ydot)
        return current_state, reward, terminal, None

    def _check_bounds(self) -> None:
        """Checks that the ball is within the bounds of the game area.

        Raises:
            RuntimeError: Ball out of bounds error.
        """
        if not (0.0 < self.ball.x < 1.0 and 0.0 < self.ball.y < 1.0):
            raise RuntimeError(
                "Ball out of bounds\n"
                f"x: {self.ball.x}\ny: {self.ball.y}\n"
                f"vel_x: {self.ball.xdot}\nvel_y: {self.ball.ydot}"
            )

    def render(self) -> plt.Figure:
        """Renders the current state of an environment.

        Args:
            env (PynBall): The environment to render.
        """
        _, ax = plt.subplots()
        for obstacle in self.obstacles:
            points = [(p.x, p.y) for p in obstacle.points]
            ax.add_patch(Polygon(points, facecolor="k"))
        ax.add_patch(
            Circle(
                [self.target.point.x, self.target.point.y],
                self.target.radius,
                facecolor="r",
            )
        )
        r = self.ball.radius
        ax.add_patch(Circle([self.ball.x, self.ball.y], r, facecolor="b"))
        if self.ball.get_speed() != 0.0:
            ax.arrow(
                self.ball.x,
                self.ball.y,
                self.ball.xdot * 2 * r,
                self.ball.ydot * 2 * r,
                head_width=0.03,
                head_length=0.03,
                facecolor="g",
                edgecolor="g",
            )
        ax.axis("equal")
        plt.gca().invert_yaxis()
        plt.show()

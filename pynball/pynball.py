import random
from pathlib import Path
from . import Ball, PolygonObstacle, Target, Point

ACTION_DICT = {
    0: (1.0, 0.0),
    1: (0.0, 1.0),
    2: (-1.0, 0.0),
    3: (0.0, -1.0),
    4: (0.0, 0.0),
}
# ACC_X, ACC_Y, DEC_X, DEC_Y, NOP

THRUST_PENALTY = -5.0
NOP_PENALTY = -1.0


class PynBall:
    def __init__(
        self,
        ball: Ball = None,
        target: Target = None,
        obstacles: list[PolygonObstacle] = None,
        seed: any = 12345,
    ) -> None:
        random.seed(seed)
        self.ball = ball if ball is not None else self.get_ball()
        self.target = target if target is not None else self.get_target()
        self.obstacles = obstacles if obstacles else self.get_obstacles()
        self.start_points: list[Point] = []
        self.step_duration: int = 20

    @classmethod
    def from_file(cls, filepath: Path) -> "PynBall":
        # TOML load stuff, then create ball
        ball = cls.get_ball()
        target = cls.get_target()
        obstacles = cls.get_obstacles()

        return cls(ball, target, obstacles)

    def get_ball(self, ball_config=None) -> Ball:
        if ball_config is None:
            self.start_points = [Point(0.1, 0.1)]
            radius = 0.1
        else:
            raise NotImplementedError()
        start_point = random.choice(self.start_points)
        return Ball(start_point, radius)

    def get_target(self, target_config=None) -> Target:
        if target_config is None:
            return Target(Point(0.9, 0.9), 0.1)
        else:
            raise NotImplementedError()

    def get_obstacles(self, obstacles_config=None) -> list[PolygonObstacle]:
        if obstacles_config is None:
            p1 = Point(0.0, 0.0)
            p2 = Point(0.0, 0.01)
            p3 = Point(0.01, 0.0)
            p4 = Point(1.0, 0.01)
            p5 = Point(0.01, 1.0)
            p6 = Point(1.0, 0.0)
            p7 = Point(0.0, 1.0)
            p8 = Point(0.0, 0.99)
            p9 = Point(0.99, 0.0)
            p10 = Point(1.0, 0.99)
            p11 = Point(0.99, 1.0)
            p12 = Point(1.0, 1.0)
            obstacles = [
                PolygonObstacle([p1, p2, p4, p6]),
                PolygonObstacle([p1, p3, p5, p7]),
                PolygonObstacle([p7, p8, p10, p2]),
                PolygonObstacle([p12, p11, p9, p6]),
            ]
            return obstacles
        else:
            raise NotImplementedError()

    def reset(self, start_state: Ball = None) -> tuple:
        if start_state is None:
            start_point = random.choice(self.start_points)

            self.ball = self.get_ball()
        else:
            self.ball = start_state
        return (self.ball.x, self.ball.y, self.ball.xdot, self.ball.ydot)

    def terminal(self) -> bool:
        return self.target.collision(self.ball)

    def step(self, action: int) -> tuple:
        x_impulse, y_impulse = ACTION_DICT[action]
        reward = NOP_PENALTY if action == 4 else THRUST_PENALTY
        terminal = False
        self.ball.add_impulse(x_impulse, y_impulse)
        for i in range(self.step_duration):
            num_collisions = 0
            self.ball.step()

            for obstacle in self.obstacles:
                if obstacle.collision(self.ball):
                    num_collisions += 1
                    # xdot, ydot = obstacle.collision_effect(self.ball)

            if num_collisions == 1:
                new_vel = obstacle.collision_effect(self.ball)
                self.ball.set_velocities(new_vel.x, new_vel.y)
                if i == self.step_duration - 1:
                    # Add a bonus step to ensure ball bounces away from obstacle.
                    self.ball.step()
            elif num_collisions > 1:
                # If there are multiple collisions, reverse velocity.
                self.ball.set_velocities(-self.ball.xdot, -self.ball.ydot)

            if self.terminal():
                terminal = True
                break

        self.ball.add_drag()
        self.check_bounds()
        current_state = (self.ball.x, self.ball.y, self.ball.xdot, self.ball.ydot)
        return current_state, reward, terminal, None

    def check_bounds(self) -> None:
        point = self.ball.get_center()
        if not (0.0 < point.x < 1.0 and 0.0 < point.y < 1.0):
            raise RuntimeError("Ball out of bounds")

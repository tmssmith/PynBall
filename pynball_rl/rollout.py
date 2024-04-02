from pathlib import Path
import importlib.resources
import random
import json
from pynball_rl import PynBall



def rollout(
    config_file: str,
    num_steps: int,
    seed: int | float | str | bytes | bytearray | None = None,
):
    """Generate a rollout in the pynball environment.

    Args:
        config (str): config file to use
        num_steps (int): Number of steps to rollout.
        seed (int | float | str | bytes | bytearray | None, optional): Seed for RNG. Defaults to None.
    """

    random.seed(seed)
    replay_buffer = {
        "state": [],
        "action": [],
        "next_state": [],
        "reward": [],
        "terminal": [],
    }
    config = importlib.resources.files("pynball_rl.configs") / config_file
    env = PynBall(Path(config))
    s1 = env.reset()
    for _ in range(num_steps):
        a = random.choice(env.action_space)
        s2, r, terminal, _ = env.step(a)
        transition = {
            "state": s1,
            "action": a,
            "next_state": s2,
            "reward": r,
            "terminal": terminal,
        }
        for key, value in transition.items():
            replay_buffer[key].append(value)
        s1 = s2
        if terminal:
            s1 = env.reset()
    with open("rollout.json", "w", encoding="utf8") as f:
        json.dump(replay_buffer, f)


if __name__ == "__main__":
    rollout("four_rooms_config.toml", 1_000_000, None)

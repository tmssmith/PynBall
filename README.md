# PynBall
Python implementation of the classic Pinball domain. State is representated as the ball position and velocity: (x, y, xdot, ydot).

To play interactively run `python -m pynball_rl`

The pinball domain was introduced in:

    G.D. Konidaris and A.G. Barto. Skill Discovery in Continuous Reinforcement Learning Domains using Skill Chaining. Advances in Neural Information Processing Systems 22, pages 1015-1023, December 2009.

This implementation is heavily based on:
- Original Java implementation at http://irl.cs.brown.edu/pinball/
- Python2 implementation at https://github.com/amarack/python-rl
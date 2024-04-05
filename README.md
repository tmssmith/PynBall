# PynBall
Python implementation of the classic Pinball domain. 

The goal is to navigate a physically modelled ball around a number of obstacles to reach a target. The ball will bounce elastically off obstacles. The agent can apply small forces to the ball, accelerating it in the $x$ or $y$ axes. 

### Dynamics
The domain has a 4-dimensional continuous state space and a 1-dimensional discrete action space. Transition dynamics are stochastic with configuration.
#### State space:
State is representated as the ball position and velocity: $(x, y, \dot{x}, \dot{y})$.
#### Action space:
There are five integer actions available to the agent in each state:
- 0: Increase velocity in $x$,
- 1: Increase velocity in $y$,
- 2: Decrease velocity in $x$,
- 3: Decrease velocity in $y$,
- 4: No-Operation (configurable).

Changes to velocity are stochastic, modelled as normal distribution centered around the requested change, with a configurable standard deviation.

 #### Rewards:
- -1 for No-Operation action,
- -5 for all other actions,
- +10,000 for reaching the goal.

### Have a go
To play interactively run `python -m pynball_rl` and select a difficulty between 1 and 3. 

### Configurations
A number of configuration files are provided in  `pynball_rl.configs`. Configuration parameters are:
- `seed`: Seed for random number generator
- `step_duration`: Number of dynamics calculations per step. A larger value will improve robustness but reduce FPS.
- `drag`: Drag coefficient. The ball velocity is multiplied by this at the end of each step. Setting to 0.0 will effectively make the state space 2-dimensional $(x,y)$.
- `stddev_x`: The standard deviation of the normal distribution from which the change in $x$-velocity is sampled. Set to 0.0 for deterministic dynamics. 
- `stddev_y`: The standard deviation of the normal distribution from which the change in $y$-velocity is sampled. Set to 0.0 for deterministic dynamics. 
- `allow_noop` : Whether to include the no-operation action in the state space.

Additionally ball start location and radius, target location and radius, and obstacle placements can be set through configuration.

### Acknowledgements
The pinball domain was introduced in:

    G.D. Konidaris and A.G. Barto. Skill Discovery in Continuous Reinforcement Learning Domains using Skill Chaining. Advances in Neural Information Processing Systems 22, December 2009.

This implementation is based on:
- Original Java implementation at http://irl.cs.brown.edu/pinball/
- Python2 implementation at https://github.com/amarack/python-rl

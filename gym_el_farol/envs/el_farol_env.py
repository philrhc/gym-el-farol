from __future__ import print_function

from gymnasium import Env
from gymnasium.spaces import Discrete


class ElFarolEnv(Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, n_agents=100, threshold=60, g=10, s=5, b=1):
        if g < s or s < b:
            raise Exception("rewards must be ordered g > s > b")

        self.n_agents = n_agents
        self.action_space = Discrete(2)
        self.observation_space = Discrete(n_agents)
        self.reward_range = (b, g)
        self.threshold = threshold
        self.s = s
        self.g = g
        self.b = b
        self.prev_action = [self.action_space.sample() for _ in range(n_agents)]

    def modify_threshold(self, change):
        self.threshold = self.threshold + self.threshold * change
        print("new threshold: " + str(self.threshold) + ", change: " + str(change))

    def reward_func(self, action, n_attended):
        if action == 0:
            return self.s
        elif n_attended <= self.threshold:
            return self.g
        else:
            return self.b

    def step(self, action):
        n_attended = sum(action)
        observation = n_attended
        reward = [self.reward_func(a, n_attended) for a in action]

        self.prev_action = action
        return observation, reward, False, ()

    def render(self, mode='human', close=False):
        if mode == 'human':
            print(str(sum(self.prev_action)))

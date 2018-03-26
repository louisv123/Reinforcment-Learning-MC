import numpy as np
import random
import matplotlib.pyplot as plt
import time

"""
Contains the definition of the agent that will run in an
environment.
"""


class RandomAgent:
    def __init__(self):
        """Init a new agent.
        """

    def reset(self, x_range):
        """Reset the state of the agent for the start of new game.

        Parameters of the environment do not change when starting a new
        episode of the same game, but your initial location is randomized.

        x_range = [xmin, xmax] contains the range of possible values for x

        range for vx is always [-20, 20]
        """
        self.state_bucket = (41, 41)
        self.state_space = [[x_range[0] + x_range[0] * i / (state_bucket[0] - 1) for i in range(state_bucket[0])], [-20 + j * 40 / (state_bucket[1] - 1) for j in range(state_bucket[1])]]

    def act(self, observation):
        """Acts given an observation of the environment.

        Takes as argument an observation of the current state, and
        returns the chosen action.

        observation = (x, vx)
        """

        # run your code

        observation_ = self.state_to_bucket(observation)

        return np.random.choice([-1, 0, 1])

    def reward(self, observation, action, reward):
        """Receive a reward for performing given action on
        given observation.

        This is where your agent can learn.
        """
        pass

    def state_to_bucket(self, state):
        new_state = ()
        for dim in range(len(self.state_bucket)):
            distance = list()
            for state_ in self.state_space[dim]:
                distance.append(np.abs(state_ - state[dim]))
                new_state += (self.state_space[dim][np.argmin(distance)],)


class q_learning_agent_2:
    def __init__(self):
        """Init a new agent.
        """
        self.epsilon = 0.1
        self.state_bucket = (12, 12)

        self.action_space = [-1, 0, 1]

        self.discount_factor = 0.9
        self.learning_rate = 0.002
        self.lambda_ = 0.8
        self.t = 1
        self.last_observation = (-100, 0)
        self.last_last_action = 0
        self.last_action = 0
        x_range = [-150, 0]
        self.state_space = [[x_range[0] + -x_range[0] * i / (self.state_bucket[0] - 1) for i in range(self.state_bucket[0])], [-20 + j * 40 / (self.state_bucket[1] - 1) for j in range(self.state_bucket[1])]]
        """
        self.W = np.random.rand(self.state_bucket[0] * self.state_bucket[1] * len(self.action_space) + 1)
        """
        self.W_ = np.random.rand(len(self.action_space), self.state_bucket[0] * self.state_bucket[1] + 1)

        self.Phi_ = np.ones(self.state_bucket[0] * self.state_bucket[1] + 1)

    def reset(self, x_range):
        """Reset the state of the agent for the start of new game.

        Parameters of the environment do not change when starting a new
        episode of the same game, but your initial location is randomized.

        x_range = [xmin, xmax] contains the range of possible values for x

        range for vx is always [-20, 20]
        """
        print(self.t)
        """
        if self.t < 500:
            self.W_ = np.random.rand(len(self.action_space), self.state_bucket[0] * self.state_bucket[1] + 1)
        """

        self.t = 1
        self.time_start = time.clock()

        """
        print(self.Phi_function(self.last_observation, self.last_action))
        print(self.W_)
        plt.subplot(3, 1, 1)
        plt.contour(self.state_space[0], self.state_space[1], self.q_matrix(-1))
        plt.colorbar()
        plt.subplot(3, 1, 2)
        plt.contour(self.state_space[0], self.state_space[1], self.q_matrix(0))
        plt.colorbar()
        plt.subplot(3, 1, 3)
        plt.contour(self.state_space[0], self.state_space[1], self.q_matrix(1))
        plt.colorbar()
        plt.show()
        """

    def act(self, observation):
        """Acts given an observation of the environment.

        Takes as argument an observation of the current state, and
        returns the chosen action.

        observation = (x, vx)



        observation_ = self.state_to_bucket(observation)

        index_observation = ()
        for dim in range(len(self.state_bucket)):
            index_observation += (self.state_space[dim].index(observation_[dim]),)

        time_elapsed = (time.clock() - self.time_start)
        print(time_elapsed)
        self.time_start = time.clock()
        """

        if random.random() < self.epsilon:
            return np.random.choice([-1, 0, 1])
        else:
            q = self.Q_function(observation, None)
            return self.action_space[np.random.choice(np.flatnonzero(q == q.max()))]

    def reward(self, observation, action, reward):
        """Receive a reward for performing given action on
        given observation.

        This is where your agent can learn.
        """
        action_ = action
        if action == None:
            action_ = 0

        """
        observation_ = self.state_to_bucket(observation)



        index_observation = ()
        for dim in range(len(self.state_bucket)):
            index_observation += (self.state_space[dim].index(observation_[dim]),)
        """
        index_action = (self.action_space.index(action_),)
        index_last_action = (self.action_space.index(self.last_action),)
        index_last_last_action = (self.action_space.index(self.last_last_action),)

        if self.t == 1:
            self.last_action = np.random.choice(self.action_space)
            self.e_1 = 0
            self.e_2 = 0
        elif self.t == 2:

            best_q = np.amax(self.Q_function(observation, None))

            target = self.last_reward + self.discount_factor * (best_q)
            self.e_2 = self.discount_factor * self.lambda_ * self.e_2 + self.Phi_function(self.last_observation)
            delta_2 = target - np.dot(self.W_[index_last_action, :], self.Phi_)
            self.W_[index_last_action, :] += self.learning_rate * delta_2 * self.e_2

        else:
            """
            best_q = np.amax(self.q_table[index_observation])
            self.q_table[self.last_observation + self.last_action] += self.learning_rate * (reward + self.discount_factor * (best_q) - self.q_table[self.last_observation + self.last_action])
            """

            best_q = np.amax(self.Q_function(observation, None))

            target_1 = self.last_last_reward + self.discount_factor * self.last_reward + self.discount_factor * (best_q)
            target_2 = self.last_reward + self.discount_factor * (best_q)
            self.e_1 = self.discount_factor * self.lambda_ * self.e_1 + self.Phi_function(self.last_last_observation)
            delta_1 = target_1 - np.dot(self.W_[index_last_last_action, :], self.Phi_)
            self.e_2 = self.discount_factor * self.lambda_ * self.e_2 + self.Phi_function(self.last_observation)

            delta_2 = target_2 - np.dot(self.W_[index_last_action, :], self.Phi_)
            self.W_[index_last_last_action, :] += self.learning_rate * delta_1 * self.e_1
            self.W_[index_last_action, :] += self.learning_rate * delta_2 * self.e_2

        self.t += 1
        self.last_action = action_
        self.last_observation = observation
        self.last_reward = reward
        self.last_last_reward = self.last_reward
        self.last_last_action = self.last_action
        self.last_last_observation = self.last_observation
    """
    def state_to_bucket(self, state):
        observation_ = ()
        for dim in range(len(self.state_bucket)):
            distance = list()
            for state_ in self.state_space[dim]:
                distance.append(np.abs(state_ - state[dim]))
            observation_ += (self.state_space[dim][np.argmin(distance)],)

        return observation_


    def set_q_table(self):
        seq_dim = ()
        for dim in range(len(self.state_space)):
            seq_dim = seq_dim + (len(self.state_space[dim]),)
        seq_dim = seq_dim + (len(self.action_space),)
        self.q_table = np.zeros(seq_dim)

    """

    def Phi_function(self, state):
        """

        action_ = action
        if action == None:
            action_ = 0



        index_action = self.action_space.index(action_)



        self.Phi = np.ones(self.state_bucket[0] * self.state_bucket[1] * len(self.action_space) + 1)
        self.coef_act = np.zeros(self.state_bucket[0] * self.state_bucket[1] * len(self.action_space) + 1)

        self.coef_act[-1] = 1

        for i in range(self.state_bucket[0]):
            for j in range(self.state_bucket[1]):
                for a in range(len(self.action_space)):
                    self.Phi[i + self.state_bucket[0] * j + self.state_bucket[0] * self.state_bucket[1] * a] = (np.exp(-((state[0] - self.state_space[0][i]) / (self.state_bucket[0]))**2) * np.exp(-((state[1] - self.state_space[1][j]) / (self.state_bucket[1]))**2))

        self.coef_act[index_action * self.state_bucket[0] * self.state_bucket[1]:(index_action + 1) * self.state_bucket[0] * self.state_bucket[1]] = 1

        self.Phi = np.multiply(self.coef_act, self.Phi)

        return self.Phi

        """

        for i in range(self.state_bucket[0]):
            for j in range(self.state_bucket[1]):
                self.Phi_[i + self.state_bucket[0] * j] = (np.exp(-((state[0] - self.state_space[0][i]) / (self.state_bucket[0]))**2) * np.exp(-((state[1] - self.state_space[1][j]) / (self.state_bucket[1]))**2))

        return self.Phi_

        """

        self.Phi_ = {}
        for i in range(self.state_bucket[0]):
            for j in range(self.state_bucket[1]):
                self.Phi_[(i, j)] = (np.exp(-((state[0] - self.state_space[0][i]) / (self.state_bucket[0]))**2) * np.exp(-((state[1] - self.state_space[1][j]) / (self.state_bucket[1]))**2))
        self.Phi_[(40, 39)] = 1
        return np.array(self.Phi_.values())


        Ph[state,action]=[0,0,0,ph_1(state,action),ph_2(state,action),ph_(state,action),0,0,0,1]
        Ph_size=1+nstate*naction

        W=[wa=1_1,...wa=1_ns,wa=2_1,...,wa=2_ns,wa=3_1,...,wa=3_ns,w0]
        """

    def Q_function(self, state, action):
        """
        return np.dot(self.W, self.Phi_function(state, action))

        """

        return np.dot(self.W_, self.Phi_function(state))
    """
        else:

            index_action = self.action_space.index(action)
            return np.dot(self.W_[index_action, :], self.Phi_function(state))



    def q_matrix(self, action):

        return [[self.Q_function((self.state_space[0][i], self.state_space[1][j]), action) for i in range(self.state_bucket[0])] for j in range(self.state_bucket[1])]
    """


class q_learning_agent:
    def __init__(self):
        """Init a new agent.
        """
        self.epsilon = 0.1
        self.state_bucket = (12, 12)

        self.action_space = [-1, 0, 1]

        self.discount_factor = 0.9
        self.learning_rate = 0.002
        self.lambda_ = 0.8
        self.t = 1
        self.last_observation = (-100, 0)
        self.last_action = 0

        x_range = [-150, 0]
        self.state_space = [[x_range[0] + -x_range[0] * i / (self.state_bucket[0] - 1) for i in range(self.state_bucket[0])], [-20 + j * 40 / (self.state_bucket[1] - 1) for j in range(self.state_bucket[1])]]

        self.W_ = np.random.rand(len(self.action_space), self.state_bucket[0] * self.state_bucket[1] + 1)

        self.Phi_ = np.ones(self.state_bucket[0] * self.state_bucket[1] + 1)

    def reset(self, x_range):

        print(self.t)
        self.t = 1

        """
        print(self.Phi_function(self.last_observation, self.last_action))
        print(self.W_)
        plt.subplot(3, 1, 1)
        plt.contour(self.state_space[0], self.state_space[1], self.q_matrix(-1))
        plt.colorbar()
        plt.subplot(3, 1, 2)
        plt.contour(self.state_space[0], self.state_space[1], self.q_matrix(0))
        plt.colorbar()
        plt.subplot(3, 1, 3)
        plt.contour(self.state_space[0], self.state_space[1], self.q_matrix(1))
        plt.colorbar()
        plt.show()
        """

    def act(self, observation):
        """Acts given an observation of the environment.

        Takes as argument an observation of the current state, and
        returns the chosen action.

        observation = (x, vx)
        """
        if random.random() < self.epsilon:
            return np.random.choice([-1, 0, 1])
        else:
            q = self.Q_function(observation, None)
            return self.action_space[np.random.choice(np.flatnonzero(q == q.max()))]

    def reward(self, observation, action, reward):
        """Receive a reward for performing given action on
        given observation.

        This is where your agent can learn.
        """
        action_ = action
        if action == None:
            action_ = 0

        index_action = (self.action_space.index(action_),)
        index_last_action = (self.action_space.index(self.last_action),)

        if self.t == 1:
            self.last_action = np.random.choice(self.action_space)
            self.e = 0

        else:
            """
            best_q = np.amax(self.q_table[index_observation])
            self.q_table[self.last_observation + self.last_action] += self.learning_rate * (reward + self.discount_factor * (best_q) - self.q_table[self.last_observation + self.last_action])
            """

            best_q = np.amax(self.Q_function(observation, None))

            target = self.last_reward + self.discount_factor * (best_q)
            self.e = self.discount_factor * self.lambda_ * self.e + self.Phi_function(self.last_observation)
            delta = target - np.dot(self.W_[index_last_action, :], self.Phi_)
            self.W_[index_last_action, :] += self.learning_rate * delta * self.e

        self.t += 1
        self.last_action = action_
        self.last_observation = observation
        self.last_reward = reward

    def Phi_function(self, state):

        for i in range(self.state_bucket[0]):
            for j in range(self.state_bucket[1]):
                self.Phi_[i + self.state_bucket[0] * j] = (np.exp(-((state[0] - self.state_space[0][i]) / (self.state_bucket[0]))**2) * np.exp(-((state[1] - self.state_space[1][j]) / (self.state_bucket[1]))**2))

        return self.Phi_

    def Q_function(self, state, action):

        return np.dot(self.W_, self.Phi_function(state))


Agent = q_learning_agent

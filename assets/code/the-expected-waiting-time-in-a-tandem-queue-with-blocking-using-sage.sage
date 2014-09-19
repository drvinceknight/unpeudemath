"""
Sage script for  example in blog post.
"""
class Tandem_Queue():
    """
    A class for an instance of the tandem_queue
    """
    def __init__(self, c_1, N, c_2, Lambda, mu_1, mu_2, p):
        self.c_1 = c_1
        self.c_2 = c_2
        self.N = N
        self.Lambda = Lambda
        self.mu_1 = mu_1
        self.mu_2 = mu_2
        self.p = p
        self.m = c_1 + c_2 + 1
        self.n = c_2 + 1
        self.state_space = [(i, j)  for j in range(c_1 + c_2 + 1) for i in range(self.c_1 + self.N - max(j - self.c_2, 0) + 1)]
        if p == 1:  # Reduces state space in particular case of p = 1
            self.state_space = [state for state in self.state_space if state[1] == 0]
        Q = [[self.q(state1, state2) for state2 in self.state_space] for state1 in self.state_space]
        for i in range(len(Q)):
            Q[i][i] = - sum(Q[i])
        self.Q = matrix(QQ, Q)
        self.expected_wait_cache = {}

    def q(self, state1, state2):
        """
        Returns the rate of transition between to given states.
        """
        delta = list(vector(state2) - vector(state1))
        if delta == [1, 0]:
            return self.Lambda
        if delta == [-1, 1]:
            return min(self.c_1 - max(state1[1] - self.c_2, 0), state1[0]) * self.mu_1 * (1 - self.p)
        if delta == [-1, 0]:
            return min(self.c_1 - max(state1[1] - self.c_2, 0), state1[0]) * self.mu_1 * self.p
        if delta == [0, -1]:
            return min(state1[1], self.c_2) * self.mu_2
        return 0

    def pi(self):
        """
        Solves linear system.
        """
        A = transpose(self.Q).stack(vector([1 for state in self.state_space]))
        return A.solve_right(vector([0 for state in self.state_space] + [1]))

    def _pi_dict(self):
        """
        Obtain a dictionary which indexes the states.
        """
            self.pi_list = self.pi()
            return {state:self.pi_list[index] for index, state in enumerate(self.state_space)}

    def p_service_1(self, state):
        """
        Returns the discretized probability of a service occurring at first station
        """
        if self.p == 1:
            return 1
        return min(self.c_1 - max(state[1]- self.c_2, 0), state[0]) * self.mu_1 / (min(self.c_1 - max(state[1]- self.c_2, 0), state[0]) * self.mu_1 + min(self.c_2, state[1]) * self.mu_2)

    def p_service_2(self, state):
        """
        Returns the discretized probability of a service occurring at second station
        """
        if self.p == 1:
            return 0
        return  min(self.c_2, state[1]) * self.mu_2 / (min(self.c_1 - max(state[1]- self.c_2, 0), state[0]) * self.mu_1 + min(self.c_2, state[1]) * self.mu_2)

    def mean_time_in_state(self, state):
        """
        Returns the mean time in any given state before a transition occurs
        """
        return  1 / (min(self.c_1 - max(state[1]- self.c_2, 0), state[0]) * self.mu_1 + min(self.c_2, state[1]) * self.mu_2)

    def expected_wait(self, state):
        """
        Function that returns the expected time till absorption for a given state
        """
        if state in self.expected_wait_cache:
            return self.expected_wait_cache[state]
        if state not in self.state_space:  # If state outside of boundary. (Might not need this after new conditions below)
            return 0
        if state[0] + max(state[1] - self.c_2, 0) < self.c_1:  # If absorbing state
            self.expected_wait_cache[state] = 0
            return 0
        self.expected_wait_cache[state] =  (self.mean_time_in_state(state) + self.p * self.p_service_1(state) * self.expected_wait((state[0] - 1, state[1])))
        if (state[0] - 1, state[1] + 1) in self.state_space:
            self.expected_wait_cache[state] += (1-self.p) * self.p_service_1(state) * self.expected_wait((state[0] - 1, state[1] + 1))
        if (state[0], state[1] - 1) in self.state_space:
            self.expected_wait_cache[state] += self.p_service_2(state) * self.expected_wait((state[0], state[1] - 1))
        return self.expected_wait_cache[state]

    def mean_expected_wait(self):
        """
        Returns the mean wait
        """
        self.pi_dict = self._pi_dict()
        accepting_states = [state for state in [s for s in self.state_space if s[0] + max(s[1] - self.c_2, 0) < self.c_1 + self.N]]
        prob_of_accepting = sum([self.pi_dict[state] for state in accepting_states])
        return sum([self.expected_wait(state) * self.pi_dict[state] for state in accepting_states]) / prob_of_accepting

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


from math import atan2, cos, sqrt, sin, pi
import numpy as np


class Leg:
    q_0 = 0
    q_1 = pi / 2
    q_2 = - pi / 2

    def __init__(self, l_0, l_1, l_2, plot=None):
        self.l_0 = l_0
        self.l_1 = l_1
        self.l_2 = l_2
        self.plot = plot

    def go_to_coords(self, x: float, y: float, z: float):
        self.q_0 = atan2(y, x)
        r_0 = sqrt(x ** 2 + y ** 2)  # projected distance from q0 to end-effector
        r_1 = sqrt(r_0 ** 2 + z ** 2)  # absolute distance from q0 to end-effector
        r_2 = sqrt(self.l_0 ** 2 + r_0 ** 2 + z ** 2 - 2 * self.l_0 * r_1 * cos(atan2(z, r_0)))  # abs. dist. q1 -> EE
        cos_a = ((self.l_1 ** 2 + r_2 ** 2 - self.l_2 ** 2) / (2 * self.l_1 * r_2))  # (q1,q2,EE) triangle (l1,r2) angle
        self.q_1 = atan2(z, r_0 - self.l_0) + atan2(sqrt(1 - cos_a ** 2), cos_a)  # angle a + (q1,EE,r) triang. q1 angle
        cos_q_2 = (r_2 ** 2 - self.l_1 ** 2 - self.l_2 ** 2) / (2 * self.l_1 * self.l_2)  # same but different
        self.q_2 = atan2(sqrt(1 - cos_q_2 ** 2), cos_q_2)
        return self.q_0, self.q_1, self.q_2

    def show(self):
        p_0 = np.array([[0], [0], [0], [1]])
        print(p_0)
        p_1 = np.matmul(calc_transform(pi / 2, self.l_0, self.q_0, 0), p_0)
        print(p_1)
        p_2 = np.matmul(calc_transform(0, self.l_1, self.q_1, 0), p_1)
        print(p_2)
        p_3 = np.matmul(calc_transform(0, self.l_2, self.q_2, 0), p_2)
        print(p_3)
        # Ne marche pas, ne renvoie pas les bonnes valeurs


def calc_transform(alpha: float, r: float, theta: float, d: float) -> np.array:
    """
    return the DH matrix from n-1 to n joint
    :param alpha: the metal rotation
    :param r: the metal translation
    :param theta: the rotation actuator
    :param d: the linear actuator
    :return: the DH matrix in numpy array
    """
    return np.array([[cos(theta), -1 * cos(alpha) * sin(theta), sin(alpha) * sin(theta), r * cos(theta)],
                     [sin(theta), cos(alpha) * cos(theta), -1 * sin(alpha) * cos(theta), r * sin(theta)],
                     [0, sin(alpha), cos(alpha), d],
                     [0, 0, 0, 1]])


def main():
    leg = Leg(1, 10, 10)
    leg.go_to_coords(10, 0, 1)
    leg.show()


if __name__ == '__main__':
    main()

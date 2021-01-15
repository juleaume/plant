from math import atan2, degrees

from numpy import array, cos, sqrt, sin, matmul, pi


class Leg:
    q_0 = 0
    q_1 = 0
    q_2 = 0

    def __init__(self, l_0: float, l_1: float, l_2: float):
        """
        Create a leg with three lengths
        :param l_0: the length from the base to the shoulder
        :param l_1: the length from the shoulder to the elbow
        :param l_2: the length from the elbow to the end-effector
        """
        self.l_0 = l_0
        self.l_1 = l_1
        self.l_2 = l_2

    def go_to_coordinates(self, x: float, y: float, z: float, deg=False):
        self.q_0 = atan2(y, x)
        r_0 = sqrt(x ** 2 + y ** 2)  # projected distance from q0 to end-effector
        r_1 = sqrt(r_0 ** 2 + z ** 2)  # absolute distance from q0 to end-effector
        r_2 = sqrt(self.l_0 ** 2 + r_0 ** 2 + z ** 2 - 2 * self.l_0 * r_1 * cos(atan2(z, r_0)))  # abs. dist. q1 -> EE
        cos_a = ((self.l_1 ** 2 + r_2 ** 2 - self.l_2 ** 2) / (2 * self.l_1 * r_2))  # (q1,q2,EE) triangle (l1,r2) angle
        self.q_1 = atan2(z, r_0 - self.l_0) + atan2(sqrt(1 - cos_a ** 2), cos_a)  # angle a + (q1,EE,r) triang. q1 angle
        cos_q_2 = (r_2 ** 2 - self.l_1 ** 2 - self.l_2 ** 2) / (2 * self.l_1 * self.l_2)  # same but different
        self.q_2 = -atan2(sqrt(1 - cos_q_2 ** 2), cos_q_2)
        if not deg:
            return self.q_0, self.q_1, self.q_2
        else:
            return degrees(self.q_0), degrees(self.q_1), degrees(self.q_2)

    def get_coord(self):
        # p_0 = array([[0], [0], [0], [1]])
        # p_1 = matmul(calc_transform(0, self.l_0, self.q_0, 0), p_0)
        # p_2 = matmul(calc_transform(pi / 2, self.l_1, self.q_1, 0), p_1)
        # p_3 = matmul(calc_transform(0, self.l_2, self.q_2, 0), p_2)
        # return p_3
        x_0, y_0, z_0 = 0.0, 0.0, 0.0
        x_1 = x_0 + self.l_0 * cos(self.q_0)
        y_1 = y_0 + self.l_0 * sin(self.q_0)
        z_1 = z_0
        x_2 = x_1 + self.l_1 * cos(self.q_1) * cos(self.q_0)
        y_2 = y_1 + self.l_1 * cos(self.q_1) * sin(self.q_0)
        z_2 = z_1 + self.l_1 * sin(self.q_1)
        x_3 = x_2 + self.l_2 * cos(self.q_1 + self.q_2) * cos(self.q_0)
        y_3 = y_2 + self.l_2 * cos(self.q_1 + self.q_2) * sin(self.q_0)
        z_3 = z_2 + self.l_2 * sin(self.q_1 + self.q_2)
        return x_3, y_3, z_3


def calc_transform(alpha: float, r: float, theta: float, d: float) -> array:
    """
    return the DH matrix from n-1 to n joint
    :param alpha:   the metal rotation
    :param r:       the metal translation
    :param theta:   the rotation actuator
    :param d:       the linear actuator
    :return: the DH matrix in numpy array
    """
    return array(
        [[cos(theta), -1 * cos(alpha) * sin(theta), sin(alpha) * sin(theta), r * cos(theta)],
         [sin(theta), cos(alpha) * cos(theta), sin(alpha) * cos(theta), r * sin(theta)],
         [0, sin(alpha), cos(alpha), d],
         [0, 0, 0, 1]]
    )


def main():
    leg = Leg(1, 10, 10)
    print(leg.go_to_coordinates(1 + 10 * sqrt(2), 0, 0, deg=True))
    print(leg.get_coord())


if __name__ == '__main__':
    main()

from math import cos, sqrt, sin, atan2, degrees

from numpy import linspace

import matplotlib.pyplot as plt


class Leg:
    q_0 = 0
    q_1 = 0
    q_2 = 0
    last_move = list()

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

    def go_to_coord(self, x: float, y: float, z: float, deg=False):
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

    def move_to(self, x: float, y: float, z: float, freq: int) -> list:
        x_0, y_0, z_0 = self.get_coord()
        positions = list()
        for dx, dy, dz in zip(
                linspace(x_0, x, freq),
                linspace(y_0, y, freq),
                linspace(z_0, z, freq)):
            positions.append(self.go_to_coord(dx, dy, dz))
            self.last_move.append(self.get_coord(True))
        return positions

    def get_coord(self, give_all=False):
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
        if give_all:
            return [x_0, x_1, x_2, x_3], [y_0, y_1, y_2, y_3], [z_0, z_1, z_2, z_3]
        else:
            return x_3, y_3, z_3

    def show(self, movement=False):
        plt.gca(projection='3d')
        if movement:
            for coord in self.last_move:
                x, y, z = coord
                plt.plot(x, y, z)
        else:
            x, y, z = self.get_coord(give_all=True)
            plt.plot(x, y, z)  # [x0, x1, x3], [y0, y1, y3], [z0, z1, z3]
        plt.show()


def main():
    leg = Leg(1, 10, 10)
    leg.go_to_coord(2, 10, 0, deg=True)
    leg.move_to(5, 0, 1, 50)
    leg.move_to(2, -10, 0, 50)
    leg.move_to(2, 10, 0, 50)
    leg.show(True)


if __name__ == '__main__':
    main()

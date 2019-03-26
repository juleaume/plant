# -*- coding: utf-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt

class Leg:
    def __init__(self, n, alpha, r, l0, l1, l2):
        self.n = n
        self.l0=l0
        self.l1=l1
        self.l2=l2
        self.tr = np.array([[math.cos(alpha), -math.sin(alpha), 0, r*math.cos(alpha)],
                            [math.sin(alpha), math.cos(alpha), 0, r*math.sin(alpha)],
                            [0,0,1,0],
                            [0,0,0,1]])
        self.theta0=0
        self.theta1=0
        self.theta2=0
    
    def goToXYZ(self,x,y,z):
        r = math.sqrt(x**2+y**2)
        theta0=math.atan2(y,x)
        
        c2 = -(r**2+z**2-self.l1**2-self.l2**2)/(2*self.l1*self.l2)
        theta2 = self.cos2atan2(c2)

        theta1p = math.atan2(z,r)
        theta1s = math.atan2(self.l2*math.sin(theta2),self.l1+self.l2*c2)
        
        theta1 = theta1p+theta1s
        
        return [theta0, theta1, theta2]
        
    
    def cos2atan2(self, cos):
        return math.atan2(math.sqrt(1-cos**2),cos)
        


def main():
    x=10
    y=0
    z=-10
    l1=10
    l2=10
    leg1 = Leg(0, 0, 1, 0, l1, l2)
    pwm = leg1.goToXYZ(x,y,z)
    print(pwm)
    x1=math.cos(pwm[1])*l1
    x2=math.cos(pwm[1]+pwm[2])*l2
    y1=math.sin(pwm[1])*l1
    y2=math.sin(pwm[1]+pwm[2])*l2
    print(0,0, x1,y1,x2,y2)
    plt.plot([0,x1,x2],[0,y1,y2])
    
if __name__ == '__main__':
    main()

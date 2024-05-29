import math
from calibrators import Calibrators
pival = math.pi

class Kinematics:
    def __init__(self, x_coordinate, y_coordinate, z_coordinate, initTheta1,
                 initTheta2, initTheta3, initTheta4, baseOffset, linkLength1,
                 linkLength2, endEffectorOffset, endEffectorOrientation = 0, linkLengthSum = 12.42):
        self.x_coord = x_coordinate
        self.y_coord = y_coordinate
        self.z_coord = z_coordinate
        self.hypotenuse = linkLengthSum
        self.phi = endEffectorOrientation
        self.calibrators = Calibrators()
        self.d1 = baseOffset
        self.a2 = linkLength1
        self.a3 = linkLength2
        self.d4 = endEffectorOffset
        self.guessInit = [-(pival / 3), -(pival / 3)]
        self.permissibleErr = 0.0000000001
        self.DHtable = [[0, 0, initTheta1, self.d1],
                        [(3*(pival/2)), 0, initTheta2, 0],
                        [0, self.a2, initTheta3, 0],
                        [0, self.a3, initTheta4, 0],
                        [0, 0, 0, self.d4]]

    def transformationMatrix(self, th1, th2, th3, th4):
        ychc = (self.a2 * math.cos(th2)) + (self.a3 * math.cos(th2 + th3)) + (self.d4 * math.cos(th2 + th3 + th4))
        zchc = (self.a2 * math.sin(th2)) + (self.a3 * math.sin(th2 + th3)) + (self.d4 * math.sin(th2 + th3 + th4))
        T5 = [[math.cos(th2 + th3 + th4), -math.sin(th2 + th3 + th4), 0, ychc],
               [math.sin(th2 + th3 + th4), math.cos(th2 + th3 + th4), 0, zchc],
               [0, 0, 1, 0],
               [0, 0, 0, 1]]
        xchc = self.hypotenuse * math.sin(th1)

        return xchc, ychc, zchc

    def populateDH(self, theta1, theta2, theta3, theta4):
        self.DHtable[0][-2] = theta1
        self.DHtable[1][-2] = theta2
        self.DHtable[2][-2] = theta3
        self.DHtable[3][-2] = theta4
   
    def invKinematics(self):
        theta_1 = math.asin(self.x_coord / self.hypotenuse)
        y1 = self.y_coord - (self.d4 * math.cos(self.phi))
        z1 = self.z_coord - (self.d4 * math.sin(self.phi))
        q = (y1**2) + (z1**2) - ((self.a2)**2) - ((self.a3)**2)
        cosq = q / (2 * (self.a2) * (self.a3))
        sinq = math.sqrt(1 - (cosq**2))
        theta_3 = math.atan(sinq / cosq)
        alp = math.atan(z1 / y1)
        quo = self.a3 * math.sin(theta_3) 
        div = self.a2 + (self.a3 * math.cos(theta_3))
        bet = math.atan(div / quo)
        theta_2 = alp - bet
        theta_4 = self.phi - (theta_2 + theta_3) 
        
        self.populateDH(theta_1, theta_2, theta_3, theta_4)

        theta_1_act = self.calibrators.toDegrees(theta_1)
        theta_2_act = self.calibrators.toDegrees(theta_2)
        theta_3_act = self.calibrators.toDegrees(theta_3)
        theta_4_act = self.calibrators.toDegrees(theta_4)

        return theta_1_act, theta_2_act, theta_3_act, theta_4_act

    def forwardKinematics(self):
        th_1 = self.DHtable[0][-2]
        th_2 = self.DHtable[1][-2]
        th_3 = self.DHtable[2][-2]
        th_4 = self.DHtable[3][-2]
        
        xchc, ychc, zchc = self.transformationMatrix(th_1, th_2, th_3, th_4)
        print("\nFrom fwd kinematics, checked coordinates at " + str(xchc) + " "+str(ychc)+ " " +str(zchc))

    def coordEstimator(self, angle1, angle2):
        y = round(float(self.a2 * math.cos(angle1) + self.a3 * math.cos(angle1 + angle2)), 1)
        z = round(float(self.a2 * math.sin(angle1) + self.a3 * math.sin(angle1 + angle2)), 1)
        coordinates = [y, z]
        
        return coordinates
    
    def iterativeSolver(self):
        angle1 = self.guessInit[0]
        angle2 = self.guessInit[1]
        i = 0
        err = 100.0
        deltaCr = [0, 0]
        angleInit = [angle1, angle2]
        angleFin = [0, 0]
        frameRef = [self.y_coord, self.z_coord]
        angle_1_indeg, _, _, _ = self.invKinematics()

        while(err > self.permissibleErr or i < 20):
            
            deltaCr[0] = frameRef[0] - (self.a2 * math.cos(angle1) + (self.a3 * math.cos(angle1 + angle2)))
            deltaCr[1] = frameRef[1] - (self.a2 * math.sin(angle1) + (self.a3 * math.sin(angle1 + angle2)))

            J = [[(-((self.a2 * math.sin(angle1)) + self.a3 * math.sin(angle1 + angle2))), (-self.a3 * math.sin(angle1 + angle2))],
                [(((self.a2 * math.cos(angle1)) + self.a3 * math.cos(angle1 + angle2))), (self.a3 * math.cos(angle1 + angle2))]]

            adj = ((self.a2 * self.a3) * ((math.cos(angle1) * math.sin(angle1 + angle2))-(math.sin(angle2) * math.cos(angle1 + angle2))))

            if (adj <= self.permissibleErr):
                _, angle_2_indeg, angle_3_indeg, _ = self.invKinematics() 
                break

            det = 1 / adj

            invJ = [[det * (self.a3 * math.cos(angle1 + angle2)), det * -(((self.a2 * math.cos(angle1)) + self.a3 * math.cos(angle1 + angle2)))],
                [det * -(-self.a3 * math.sin(angle1 + angle2)), det * ((self.a2 * math.sin(angle1)) + self.a3 * math.sin(angle1 + angle2))]]
            
            adder = [(invJ[0][0] * deltaCr[0]) + (invJ[0][1] * deltaCr[1]),
                     (invJ[1][0] * deltaCr[0]) + (invJ[1][1] * deltaCr[1])]

            angleFin[0] = angleInit[0] + adder[0]
            angleFin[1] = angleInit[1] + adder[1]
            
            print("\nIn iteration 1 " +str(angleFin[0]))
            print("\nIn iteration 2 " +str(angleFin[1]))

            angleInit = angleFin

            angle1 = angleInit[0]
            angle2 = angleInit[1]

            if deltaCr[0] >= deltaCr[1]:
                err = deltaCr[0] 
            elif deltaCr[1] > deltaCr[0]:
                err = deltaCr[1]    

            angle_2_indeg = self.calibrators.toDegrees(angleFin[0])
            angle_3_indeg = self.calibrators.toDegrees(angleFin[1])

            i += 1

        angle_4_indeg = - angle_2_indeg - angle_3_indeg

        return angle_1_indeg, angle_2_indeg, angle_3_indeg, angle_4_indeg

instance_Kinematics = Kinematics(0, 0,0, 0, (pival/2), (pival/6), (pival/3), 4, 12, 12, 4)
    
def main():
    print(instance_Kinematics.invKinematics())
    print(instance_Kinematics.iterativeSolver())
    instance_Kinematics.forwardKinematics()

if __name__ == "__main__":
    main()
    


        

import time
from servo import Servo
from machine import Pin

class Actuators:
    def __init__(self, gripSw, relSw):
        self.minAngle = 0
        self.maxAngle = 90
        self.effectorAngle = 0
        self.bslp = 0.03
        self.slp = 0.1
        self.gripSw = gripSw
        self.relSw = relSw
        self.angleRes = 3
        self.endEffector = Servo(Pin(15))

    def releaserDebouncer(self):
        for i in range(3):
            time.sleep(self.bslp)
            tR = self.gripSw.value()
            if tR == 0:
                time.sleep(self.slp)
                break

    def gripperDebouncer(self):
        for i in range(3):
            time.sleep(self.bslp)
            tG = self.relSw.value()
            if tG == 0:
                time.sleep(self.slp)
                break

    def gripper(self,angleGrp):
        while True:
            print("servo written at " +str(angleGrp))
            self.endEffector.write(angleGrp)
            angleGrp += self.angleRes
            tmpG = self.gripSw.value()
            time.sleep(self.slp)
            tmpG2 = self.gripSw.value()
            if (angleGrp >= 90 or tmpG == 0 or tmpG2 == 0):
                self.gripperDebouncer()
                break

        return angleGrp

    def releaser(self,angleRel):
        while True:
            print("servo written at " +str(angleRel))
            self.endEffector.write(angleRel)
            angleRel -= self.angleRes
            tmpR = self.relSw.value()
            time.sleep(self.slp)
            tmpR2 = self.relSw.value()
            if (angleRel <= 0 or tmpR == 0 or tmpR2 == 0):
                self.releaserDebouncer()
                break

        return angleRel




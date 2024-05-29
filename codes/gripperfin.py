from machine import Pin
import time
from servo import Servo
grp_id1 = Pin(16, Pin.IN, Pin.PULL_UP)
grp_id2 = Pin(17, Pin.IN, Pin.PULL_UP)
endEffector = Servo(Pin(16))

def releaserdebouncer():
    time.sleep(0.04)
    tr = grp_id2.value()
    if tr == 0
    time.sleep(0.1)

def gripperdebouncer():
    time.sleep(0.05)
    tg = grp_id1.value()
    if tg == 0:
        time.sleep(0.1)

def gripper(anglegrp):
    while True:
        print("Servo written at " + str(anglegrp))
        endEffector.write(anglegrp)
        anglegrp += 2
        tmpg = grp_id1.value()
        time.sleep(0.1)
        tmog2 = grp_id1.value()
        if (anglegrp >= 90 or tmpg == 0 or tmpg2 == 0):
            gripperdebouncer()
            break

    return anglegrp

def releaser(anglerel):
    while True:
        print("Servo written at " + str(anglerel))
        endEffector.write(anglerel)
        anglerel -= 2
        tmpr = grp_id2.value()
        time.sleep(0.1)
        tmpr2 = grp_id2.value()
        if (anglerel <= 0 or tmpr == 0 or tmpr2 == 0):
            releaserdebouncer()
            break
    return anglerel

def main():
    effectorAngle = 0
    while True:
        print("\nRunning in the main loop")
        tmp1 = grp_id1.value()
        tmp2 = grp_id2.value()
        if tmp1 == 0:
            gripperdebouncer()
            effectorAngle = gripper(effectorAngle)
        elif tmp2 == 0:
            releaserdebouncer()
            angleval = releaser(effectorAngle)
        time.sleep(0.1)

if __name__ == "__main__":
    main()


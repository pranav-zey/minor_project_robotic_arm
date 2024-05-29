from machine import Pin
import utime
grip = Pin(16, Pin.IN, Pin.PULL_UP)
release = Pin(17, Pin.IN, Pin.PULL_UP)

def gripperLogic(flag):
    flag = (flag + 1 ) % 4
    if flag == 1 and clenchAngle<minAngle:
        print("\nServo is gripping the object") #servowrite to be written here
    elif flag == 2 and clenchAngle <= minAngle:
        print("\nServo has gripped the object") #servowrite to be written here
    elif flag == 3 and clenchAngle >= minAngle and clenchAngle < maxAngle:
        print("\nServo is releasing the object") #servowrite to be written here
    elif flag == 0 and clenchAngle <= maxAngle and clenchAngle > minAngle:
        print("\nServo has now released the object") #servowrite to be written here
    
def main():
    flag = 0
    while True:
        grptmp = grip.value()
        reltmp = release.value()
        print("\n Gripper state " +str(grptmp) + "releaser state " + str(reltmp))
        utime.sleep(0.1)
        grpcmp = grip.value()
        relcmp = release.value()
        
        if grptmp != grpcmp or relcmp != reltmp:
            flag = gripperLogic(flag)     
            
        
if __name__ == "__main__":
    main()
    

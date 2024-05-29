from machine import Pin, ADC
import utime
from calibrators import Calibrators

xAxis = ADC(26)
yAxis = ADC(27)
zAxis = ADC(28)
gripperClench = Pin(16, Pin.IN, Pin.PULL_UP)
#gripperRelease = Pin(17, Pin.IN, Pin.PULL_UP)
instance_calib = Calibrators()
flag =0
final_frame = ()
def getvalues():
    xinit = xAxis.read_u16()
    yinit = yAxis.read_u16()
    zinit = zAxis.read_u16()
    grpc = gripperClench.value()
    #grpr = gripperRelease.value()
    
    return xinit, yinit, zinit, grpc
    
def gripper_checker(flg):
    
#     flg = (flg+1) % 4
#     while True:
# 
#         if (flg == 1):
#             print("The servo is now clenching the object\n")
#             break
#         elif (flg == 2):
#             print("The servo is now at rest after it has clenched the object\n")
#             break
#         elif (flg == 3):
#             print("The servo is releasing the object\n")
#             break
#         elif (flg == 0):
#             print("The servo is at rest after release\n")
#             break
#     return flg
    while True:
        print("It is running in the gripper loop\n")
        _,_,_,_, checkerswitch = getvalues()
        temp = checkerswitch
        utime.sleep(0.1)
        _,_,_,_, checkerswitch = getvalues()
        if checkerswitch != temp:
            break 

def coordinate_mapper_x(xval, movement):
    if xval>=0 and xval<=10:
        if movement == 5:
            xval -=1
        elif movement == 4:
            xval -=0.5
        elif movement == 2:
            xval += 0.5
        elif movement == 1:
            xval +=1
    if xval <= 0:
        xval = 0
    if xval >= 10:
        xval = 10
    return xval

def coordinate_mapper_yz(yzval, movement):
    if yzval >=0 and yzval <=10:
        if movement == 2:
            yzval += 0.5
        elif movement == 1:
            yzval += 1
        elif movement == 4:
            yzval -= 0.5
        elif movement == 5:
            yzval -=1
    if yzval <= 0:
        yzval = 0
    if yzval >= 10:
        yzval = 10
    return yzval
    
def main():
    init_frame = (5,0,0)
    while True:
    #     print("It is running in the main loop\n")
    #     values = (xValue, yValue, zValue)
        
    #     print("value of x axis : " +str(xValue)+ "value of y axis : " +str(yValue)+ "value of z axis : " + str(zValue) +" status of swxc "+ str(swxc) + " grst" + str(swg))
        
    #     crvalues = instance_calib.js_corrected_steps(values)
        
    #     print("corrected value of x axis : "+str(crvalues[0])+ " corrected value of y-axis : " +str(crvalues[1])+ " corrected value of z-axis : " +str(crvalues[2]))
    #     utime.sleep(0.1)
    #     xValue, yValue, zValue, swxc, grp = getvalues()
    #     if swg != tmp:
    #         flag = gripper_checker(flag)
    #     utime.sleep(0.1)

        x1, y1, z1, clstate1 = getvalues()
        values_init = (x1, y1, z1)
        crvalues_init = instance_calib.js_corrected_steps(values_init)
        print("Initial configuration\n")
        print("x axis : "+str(crvalues_init[0]) + " y axis :" +str(crvalues_init[1])+ "zaxis :" +str(crvalues_init[-1]))
        utime.sleep(1)
        x2, y2, z2, clstate2 = getvalues()
        values_sec = (x2, y2, z2)
        crvalues_sec = instance_calib.js_corrected_steps(values_sec)
        print("Secondary Configuration\n")
        print("x axis : "+str(crvalues_sec[0]) + " y axis :" +str(crvalues_sec[1])+ " zaxis :" +str(crvalues_sec[-1]))
        print("\nInitial value of end-effector ", init_frame)
        x_fin = coordinate_mapper_x(init_frame[0], crvalues_sec[1])
        y_fin = coordinate_mapper_yz(init_frame[1], crvalues_sec[0])
        z_fin = coordinate_mapper_yz(init_frame[-1], crvalues_sec[-1])
        temp_frame = (x_fin, y_fin, z_fin)
        final_frame = temp_frame
        init_frame = temp_frame
        print("\nFinal value of end effector ", final_frame)
        
        
if __name__ == "__main__":
    main()

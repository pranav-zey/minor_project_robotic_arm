from machine import Pin, ADC
from calibrators import Calibrators
import utime 

class InputPipeline:
    def __init__(self, xAxisPin, yAxisPin, zAxisPin, gripperFastenPin,
                 gripperReleasePin):
        self.xAxis = ADC(xAxisPin)
        self.yAxis = ADC(yAxisPin)
        self.zAxis = ADC(zAxisPin)
        self.grpT = Pin(16, Pin.IN, PULL_UP)
        self.grpL = Pin(17, Pin.IN, PULL_UP)
        self.flagVal = 0
        self.calibrator = Calibrators()

    def getValues(self):
        xVal = self.xAxis.read_u16()
        yVal = self.yAxis.read_u16()
        zVal = self.zAxis.read_u16()
        grpT = self.grpT.value()
        grpL = self.grpL.value()
        return xVal, yVal, zVal, grpT, grpL

    def gripperFlagOffset(self):
        self.flagVal = (self.flagVal + 1) % 4
        return self.flagVal

    def gripperChecker(self, flag):
        while True:
            print("It is running in the gripper loop\n")
            _,_,_,_,checkerswitch = self.getValues()
            temp = checkerswitch 
            utime.sleep(0.1)
            _,_,_,_,checkerswitch = self.getValues()
            if temp != checkerswitch:
                break

    def calibratedValues(self):
        x1, y1, z1, _, _ = self.getValues()
        values = (x1, y1, z1)
        crValues = calibrator.correctedSteps(valuesInit)
        
        return crValues[0], crValues[1], crValues[2]


class CoordinateMapper:
    def __init__(self):
        self.xNegLim = -12
        self.PosLim = 12
        self.ext1 = 5
        self.ext2 = 1
        self.mid1 = 4
        self.mid2 = 2
        self.yzMin = 0
        self.initFrame = (0, 0, 0)

       def coordinatex_Mapper(self, xVal, movement):
        if xVal >= self.xNegLim and xVal <= self.xPosLim:
            if movement == self.ext1:
                xVal -= 1
            elif movement == self.mid1:
                xVal -= 0.5
            elif movement == self.mid2:
                xVal += 0.5
            elif movement== self.ext2:
                xVal += 1

        if xVal <= -xNegLim:
            xVal = -xNegLim
        if xVal >= PosLim:
            xVal = PosLim

        return xVal

    def coordinateyz_Mapper(self, yzVal, movement):
        if yzVal >= yzmin and yzVal <= PosLim:
            if movement == self.ext1:
                yzVal -= 1
            elif movement == self.mid1:
                yzVal -= 0.5
            elif movement == self.mid2:
                yzVal += 0.5
            elif movement == self.ext2:
                yzVal += 1

        if yzVal <= self.yzMin:
            yzVal = self.yzMin
        if yzVal >= self.PosLim:
            yzVal = self.PosLim

        return yzVal

    def frameReturner(self, crValues):
        xFin = self.coordinatex_Mapper(self.initFrame[0], crValues[1])
        yFin = self.coordinateyz_Mapper(self.initFrame[1], crValues[0])
        zFin = self.coordinateyz_Mapper(self.initFrame[-1], crValues[-1])
        tempFrame = (xFin, yFin, zFin)
        finFrame = tempFrame
        self.initFrame = tempFrame

        return finFrame


def main():
inputInterface = InputPipeline(26, 27, 28, 16, 17)
coordinateMapper = CoordinateMapper()

    while True:
        x1, y1, z1 = inputInterface.calibratedValues() 
        correctedMovement = (x1, y1, z1)
        endEffectorPos = coordinateMapper.frameReturner(correctedMovement)
        print("\nThe final position of end coordinator is " + str(endEffectorPos))
        utime.sleep(0.2)
        
if __name__ == "__main__" :
    main()


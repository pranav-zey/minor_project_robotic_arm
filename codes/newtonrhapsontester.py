import math
pival = math.pi
from calibrators import Calibrators
instance_calib = Calibrators()

def newtonRhapson(x, y):
    linkLen1 = 9.5
    linkLen2 = 5.5
    initGuess1 = pival / 3
    initGuess2 = -pival / 2
    errVal = 0.0001
    count = 0
    err = 100
    while errVal <= err:
        delX = x - (math.cos(initGuess1) + math.cos(initGuess1 + initGuess2))
        delY = y - (math.sin(initGuess1) + math.sin(initGuess1 + initGuess2))
        if delX <= delY:
            err = delX
        elif delY < delX:
            err = delY
        print("\n Iteration " + str(count))
        print("\n delX initially " +str(delX))
        print("\n delY initially " +str(delY))
        adj = (linkLen1 * linkLen2) * ((math.cos(initGuess1)*math.sin(initGuess1+initGuess2))-
                                       (math.sin(initGuess1)*math.cos(initGuess1+initGuess2)))
        if adj <= errVal:
            print("\nError while solving numerically")
            break

        det = 1 / adj

        cofacJ = [[linkLen2 * math.cos(initGuess1 + initGuess2), (linkLen2 * math.sin(initGuess1 + initGuess2))],
                [-((linkLen1 * math.cos(initGuess1)) + linkLen2 * math.cos(initGuess1 + initGuess2)), -((linkLen1 * math.sin(initGuess1)) + linkLen2 * math.sin(initGuess1 + initGuess2))]]

        invJ = [[det * cofacJ[0][0], det * cofacJ[0][1]],
                [det * cofacJ[1][0], det * cofacJ[1][1]]]
        
        guess1 = invJ[0][0] * delX + invJ[0][1] * delY
        guess2 = invJ[1][0] * delX + invJ[1][1] * delY

        finGuess1 = initGuess1 + guess1
        finGuess2 = initGuess2 + guess2

        in_deg1 = instance_calib.toDegrees(finGuess1)
        in_deg2 = instance_calib.toDegrees(finGuess2)

        print("\n Degree 1 " + str(in_deg1))
        print("\n Degree 2 " + str(in_deg2))

        initGuess1 = finGuess1
        initGuess2 = finGuess2

        count += 1

def main():
    newtonRhapson(12, 12)

if __name__ == "__main__":
    main()


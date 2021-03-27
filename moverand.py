import random
import math
import numpy as np

#setting numb of slimes and pixels in grid

WIDTH=50
HEIGHT=50
SLIMES=10
MOVELENGTH=5

#setting start coords

START_X=25
START_Y=25

#creating arrays for the coords and direction of each slime. also for strength of trail for each coord

TRAILSTRENGTH=10
DEGREECHANGE=0.5

LOOK=10

xSlime=np.array([START_X for _ in range(SLIMES)])
ySlime=np.array([START_Y for _ in range(SLIMES)])
direction=np.array([random.uniform(0, math.pi*2) for _ in range(SLIMES)])
trail=np.array([0 for _ in range(WIDTH*HEIGHT)])

def CoordsToIndex(xCord, yCord):
    result=xCord+yCord*WIDTH
    return result

def IndexToCoords(index):
    xCord=index%WIDTH
    yCord=(index-xCord)/WIDTH
    return(xCord, yCord)

def distanceIndex(index1, index2):

    x1, y1=IndexToCoords(index1)
    x2, y2=IndexToCoords(index2)

    if math.sqrt((x1-x2)**2+(y1-y2)**2)<=LOOK:
        return True

def Update(xSlime, ySlime, direction, trail): # TODO: add path of trail

    #lower strength everywhere by 1

    for counter in range(len(trail)):
        if trail[counter]>=1:
            trail[counter]-=1

    for i in range(SLIMES):

        #leave behind trail where slime was

        trail[CoordsToIndex(xSlime, ySlime)]+=100

        #change the slimes position

        xSlime[i]+=int(math.cos(direction[i])*MOVELENGTH)
        ySlime[i]+=int(math.sin(direction[i])*MOVELENGTH)

        direction[i]+=random.uniform(-DEGREECHANGE, DEGREECHANGE)

    #change direction for next run if there is a trail at most LOOK away from slime

    for i in range(SLIMES):

        slimeIndex=CoordsToIndex(xSlime[i], ySlime[i])
        surroundingTrailStrength=[]
        indexOfSurroundingTrailStrength=[]

        #cycles through all cords in sqare shape with radius look to see if they are in range

        for xMovement in range(-LOOK, LOOK+1):
            for yMovement in range(-LOOK*WIDTH, LOOK*WIDTH+1, WIDTH):
                possibleIndex=xMovement+yMovement+slimeIndex

                #checks to see if they are at most LOOK away from slime

                if distanceIndex(slimeIndex, possibleIndex):
                    surroundingTrailStrength.append(trail[possibleIndex])
                    indexOfSurroundingTrailStrength.append(possibleIndex)

        #sees which trail around it has highest strength. finds the coords of that trail and points slime towards it

        if max(surroundingTrailStrength)>0:

            goalIndex=surroundingTrailStrength.index(max(surroundingTrailStrength))
            goalIndex=indexOfSurroundingTrailStrength[goalIndex]

            xGoal, yGoal=IndexToCoords(goalIndex)

            direction[i]=random.uniform(-DEGREECHANGE, DEGREECHANGE)+math.atan2(yGoal-ySlime[i], xGoal-xSlime[i])

        return (xSlime, ySlime, direction, trail)

for _ in range(4):
    xSlime, ySlime, direction, trail=Update(xSlime, ySlime, direction, trail)

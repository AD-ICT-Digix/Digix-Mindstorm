#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Image
import time

# Initalize the ev3 object
ev3 = EV3Brick()
# Initialize the motors
LEFT_WHEEL = Motor(Port.B)
RIGHT_WHEEL = Motor(Port.C)
FEED_MOTOR = Motor(Port.A)  # dispenser motor for color squares
# Set the speed of the motors (These values are larger than they were in C because they are measured differently)
SPEED_SLOW = -100
SPEED_FAST = 200
# (-80, 200) Two values that also work for SPEED_SLOW and SPEED_FAST respectively
# Initalize the Sensors
COLOUR_SENSOR = ColorSensor(Port.S3)
ULTRASOUND_SENSOR = UltrasonicSensor(Port.S2)

# The tolerance for the colour sensor to activate
LIGHT_TOLERANCE = 22

# init feed motor
FEED_MOTOR.run_until_stalled(120)
FEED_MOTOR.run_angle(450, -180)

lastSeenColour = 0
# 0 - None
# 1 - Red

# What to do when it sees a Red marker


def handleRed():
    print("Red is starting")
    LEFT_WHEEL.stop()
    RIGHT_WHEEL.stop()
    ev3.speaker.play_file(SoundFile.LASER)
    # Feed the color square 2 TIMES USING FOR LOOP
    for i in range(2):
        FEED_MOTOR.run_until_stalled(120)
        FEED_MOTOR.run_angle(450, -180)
    return None

# Returns true if the colour sensor is over a line (The variable shifts the tolerance which is necessary for precision)


def senseColour(offset=0):
    global lastSeenColour
    # Find the RGB values and the average of all 3
    R, G, B = COLOUR_SENSOR.rgb()
    print("R: " + str(R) + " G: " + str(G) + " B: " + str(B))
    average = (R + G + B) / 3
    print("Average: " + str(average))

    # If the average is less than the tolerance, the sensor is over a line
    if average < LIGHT_TOLERANCE + offset:
        if R > G and R > B:
            lastSeenColour = 1
        else:
            print("Line is detected")
        return True
    else:
        print("Line is not detected")
        return False

# Main loop that follows the line


def mainLoop():
    print("Main loop is starting")
    while True:
        # If it sees the line, go right
        if senseColour():
            LEFT_WHEEL.run(SPEED_FAST)
            RIGHT_WHEEL.run(SPEED_SLOW)
        else:  # Otherwise go left
            LEFT_WHEEL.run(SPEED_SLOW)
            RIGHT_WHEEL.run(SPEED_FAST)


LEFT_WHEEL.stop()
RIGHT_WHEEL.stop()
mainLoop()
#Play a sound of 500Hz for 2 seconds
ev3.speaker.beep(500, 1000)
#After playing a sound check the last seen colour and call the appropriate function
if lastSeenColour == 1:
    handleRed()
else:
    print("No red marker detected")

#Go back to following the line
mainLoop()
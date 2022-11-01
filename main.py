#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

# Initalize the ev3 object
ev3 = EV3Brick()

# Initialize the motors
LEFT_WHEEL = Motor(Port.B)
RIGHT_WHEEL = Motor(Port.C)
FEED_MOTOR = Motor(Port.A)  # dispenser motor for color squares
# Set the speed of the motors (These values are larger than they were in C because they are measured differently)
SPEED_SLOW = -200
SPEED_FAST = 300
# (-80, 200) Two values that also work for SPEED_SLOW and SPEED_FAST respectively
# Initalize the Sensors
COLOUR_SENSOR = ColorSensor(Port.S3)
ULTRASOUND_SENSOR = UltrasonicSensor(Port.S2)

# The tolerance for the colour sensor to activate
LIGHT_TOLERANCE = 22
lastSeenColour = 0
# 0 - Green
# 1 - Blue

# init feed motor
FEED_MOTOR.run_until_stalled(120)
FEED_MOTOR.run_angle(450, -180)

# feed motor function.

def feedMotor():
    LEFT_WHEEL.stop()
    RIGHT_WHEEL.stop()
    ev3.speaker.play_file(SoundFile.LASER)
    # when sorting_machine in position , dispense a color square
    # repeat 6 times
    for i in range(8):
        # dispense a color square
        FEED_MOTOR.run_until_stalled(120)
        FEED_MOTOR.run_angle(450, -180)
        # wait 1 second
        time.sleep(1)
    wait(1000)


# Returns true if the colour sensor is over a line (The variable shifts the tolerance which is necessary for precision)
def senseColour(offset=0):
    # Global is used to access the variable outside of the function and not define a new variable
    global lastSeenColour
    # Find the RGB values and the average of all 3
    R, G, B = COLOUR_SENSOR.rgb()
    print("R: " + str(R) + " G: " + str(G) + " B: " + str(B))

    average = (R + G + B) / 3
    # If the average is less than the tolerance, the sensor is over a line
    if average < LIGHT_TOLERANCE + offset:
        if R > G and R > B:
            lastSeenColour = 1
        return True
    return False
# Main loop that follows the line


def mainLoop():
    while True:
        # If it sees the line, go right
        if senseColour():
            LEFT_WHEEL.run(SPEED_FAST)
            RIGHT_WHEEL.run(SPEED_SLOW)
        else:  # Otherwise go left
            LEFT_WHEEL.run(SPEED_SLOW)
            RIGHT_WHEEL.run(SPEED_FAST)
        # If it sees the red line, handle it
        if lastSeenColour == 1:
            handleRed()
        # If it sees an obstacle, handle it
        if ULTRASOUND_SENSOR.distance() < 100:
            handleObstacle()

# What to do when it sees a Red marker


def handleRed():
    feedMotor()

# What to do when it sees a GREEN obstacle


def handleObstacle():
    RIGHT_WHEEL.reset_angle(0)
    # Turn right a small amount to make sure it is on the line
    RIGHT_WHEEL.run_target(SPEED_SLOW, -55)

    # Turn right until it is no longer on the line
    while not senseColour():
        LEFT_WHEEL.run(SPEED_SLOW / 2)
        RIGHT_WHEEL.run(SPEED_FAST / 2)
    # Slowly turn left until it is on the line
    while senseColour(-2):
        LEFT_WHEEL.run(SPEED_FAST / 2)
        RIGHT_WHEEL.run(SPEED_SLOW / 2)
    # Go forward until it is close to the obstacle (40mm)
    while ULTRASOUND_SENSOR.distance() > 40:
        LEFT_WHEEL.run(SPEED_FAST / 2)
        RIGHT_WHEEL.run(SPEED_FAST / 2)
    # Stop
    LEFT_WHEEL.stop()
    RIGHT_WHEEL.stop()
    # Reset Encoder
    LEFT_WHEEL.reset_angle(0)
    # Run off to the right with the obstacle and then return
    LEFT_WHEEL.run_target(SPEED_FAST, 360)
    LEFT_WHEEL.run_target(SPEED_FAST, 70)


# This is where the code truly starts
# Make sure the motors aren't breaking and then call the line following function
LEFT_WHEEL.stop()
RIGHT_WHEEL.stop()
mainLoop()

# Play a sound of 500Hz for 2 seconds
ev3.speaker.beep(500, 2000)
# After playing a sound check the last seen colour and call the appropriate function
if lastSeenColour == 1:
    handleRed()
else:
    handleObstacle()

# Go back to following the line
mainLoop()

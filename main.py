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
LEFT_WHEEL = Motor(Port.B) # left wheel that is connected to port B
RIGHT_WHEEL = Motor(Port.C) # right wheel that is connected to port C
FEED_MOTOR = Motor(Port.A)  # dispenser motor for color squares
# Initalize the Sensors
COLOUR_SENSOR = ColorSensor(Port.S3) # color sensor that is connected to port S3
ULTRASOUND_SENSOR = UltrasonicSensor(Port.S2) # ultrasound sensor that is connected to port S2

# Set the speed of the motors (These values are larger than they were in C because they are measured differently)
# (-80, 200) Two values that also work for SPEED_SLOW and SPEED_FAST respectively
SPEED_SLOW = -100  # The speed that the robot will drive at
SPEED_FAST = 200 # The speed that the robot will drive at
LIGHT_TOLERANCE = 22 # The tolerance for the colour sensor to activate

# Initialize the robot drive base
ROBOT = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# init feed motor
FEED_MOTOR.run_until_stalled(120) # run until the motor stalls
FEED_MOTOR.run_angle(450, -180) # run the motor at 450 degrees per second until it returns to its original position

lastSeenColour = 0
# 0 - None
# 1 - Red

def handleRed(): # What to do when it sees a Red marker
    print("Red is starting") # Print to the console
    LEFT_WHEEL.stop() # Stop the left wheel
    RIGHT_WHEEL.stop() # Stop the right wheel 
    ev3.speaker.play_file(SoundFile.ACTIVATE) # Play a sound 
    for i in range(2): # For loop that runs twice
        FEED_MOTOR.run_until_stalled(120) # Run the motor until it stalls
        FEED_MOTOR.run_angle(450, -180) # Run the motor at 450 degrees per second until it returns to its original position
    ROBOT.drive_time(100, 0, 1000) # Drive forward for 1 second

# Returns true if the colour sensor is over a line (The variable shifts the tolerance which is necessary for precision)
def senseColour(offset=0):
    global lastSeenColour # Make the variable global so that it can be accessed outside of the function
    R, G, B = COLOUR_SENSOR.rgb() # Get the RGB values from the colour sensor
    print("R: " + str(R) + " G: " + str(G) + " B: " + str(B)) # Print the RGB values to the console
    average = (R + G + B) / 3 # Calculate the average of the RGB values
    print("Average: " + str(average)) # Print the average to the console

    # If the average is less than the tolerance, the sensor is over a line
    if average < LIGHT_TOLERANCE + offset: # If the average is less than the tolerance, the sensor is over a line
        if R > G and R > B: # If the red value is the highest, it is a red marker
            lastSeenColour = 1 # Set the last seen colour to red
            print("Red marker detected") # Print to the console
        else: # Otherwise it is not a red marker
            print("Line is detected") # Print to the console
        return True # Return true
    else: # Otherwise it is not over a line
        print("Line is not detected") # Print to the console
        return False # Return false

# Main loop that follows the line
def mainLoop(): # Main loop that follows the line
    while True: # Infinite loop
        print("Main loop is running") # Print to the console
        if senseColour(): # If it sees the line, go right
            LEFT_WHEEL.run(SPEED_FAST) # Run the left wheel at the fast speed
            RIGHT_WHEEL.run(SPEED_SLOW) # Run the right wheel at the slow speed
        else:  # Otherwise go left
            LEFT_WHEEL.run(SPEED_SLOW) # Run the left wheel at the slow speed
            RIGHT_WHEEL.run(SPEED_FAST) # Run the right wheel at the fast speed
        # If it sees a red marker, handle it
        if lastSeenColour == 1: # If it sees a red marker, handle it
            ev3.speaker.play_file(SoundFile.DETECTED) # Play a sound 
            handleRed() # Handle the red marker
            print("Red has been handled") # Print to the console
            lastSeenColour = 0 # Reset the last seen colour
        # If the ultrasonic sensor sees an object, stop the robot and turn around
        if obstacle_sensor.distance() < 100: # If the ultrasonic sensor sees an object, stop the robot and turn around
            ROBOT.stop() # Stop the robot
            ev3.speaker.play_file(SoundFile.SONAR) # Play a sound
            ROBOT.drive_time(-100, 0, 1000) # Drive backwards for 1 second
            ROBOT.drive_time(100, 180, 1000) # Turn around for 1 second
            ROBOT.drive_time(100, 0, 1000) # Drive forward for 1 second

mainLoop() # Run the main loop function when the program starts running
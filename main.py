#!/usr/bin/env pybricks-micropython
#   Author: N. Heutz
#   Author: J. Reinartz 
#   Author: D. Nellesen
#   Author: V. Pelxer
#   Creation Date:    Friday 9 September 2022   By: N.Heutz
#   Last edited at    Thursday 3 November 2022    By: N.Heutz

from pybricks.hubs import EV3Brick

from pybricks.ev3devices import (
    ColorSensor, 
    GyroSensor
    InfraredSensor, 
    Motor, 
    TouchSensor, 
    UltrasonicSensor, 
)

from pybricks.parameters import 
    Button, 
    Color
    Direction, 
    Stop, 
    Port, 

from pybricks.tools import 
    DataLog
    StopWatch, 
    wait, 

from pybricks.robotics import 
    DriveBase

from pybricks.media.ev3dev import 
    Image
    ImageFile, 
    SoundFile, 

import time
from menu import wait_for_button

# Initalize the ev3 object
ev3 = EV3Brick()
# Initialize the motors & sensors
LEFT_WHEEL = Motor(Port.B) # left wheel that is connected to port B
RIGHT_WHEEL = Motor(Port.C) # right wheel that is connected to port C
FEED_MOTOR = Motor(Port.A)  # dispenser motor for color squares
COLOUR_SENSOR = ColorSensor(Port.S3) # color sensor that is connected to port S3
ULTRASOUND_SENSOR = UltrasonicSensor(Port.S2) # ultrasound sensor that is connected to port S2

# Set the speed of the motors (These values are larger than they were in C because they are measured differently)
# (-80, 200) Two values that also work for SPEED_SLOW and SPEED_FAST respectively
SPEED_SLOW = -100  # The speed that the robot will drive at
SPEED_FAST = 200 # The speed that the robot will drive at
LIGHT_TOLERANCE = 22 # The tolerance for the colour sensor to activate

# Initialize the robot drive base
ROBOT = DriveBase(LEFT_WHEEL, RIGHT_WHEEL, wheel_diameter=55.5, axle_track=104)

def handleRed(): # What to do when it sees a Red marker
    global TURNS # Get the TURNS variable
    TURNS.append(0) # Add a turn to the TURNS variable
    ROBOT.stop() # Stop the robot
    print("HandleRed is initializing") # Print to the console
    ev3.speaker.play_file(SoundFile.SONAR) # Play a sound 
    for i in range(2): # For loop that runs twice
        FEED_MOTOR.run_until_stalled(120) # Run the motor until it stalls
        FEED_MOTOR.run_angle(450, -180) # Run the motor at 450 degrees per second until it returns to its original position
    ROBOT.drive_time(100, 0, 500) # Drive forward for 0.5 second

TURNS = [] # Create a list to store the TURNS
# Returns true if the colour sensor is over a line (The variable shifts the tolerance which is necessary for precision)
def senseColour(offset=0): 
    R, G, B = COLOUR_SENSOR.rgb() # Get the RGB values from the colour sensor
    print("R: " + str(R) + " G: " + str(G) + " B: " + str(B)) # Print the RGB values to the console
    average = (R + G + B) / 3 # Calculate the average of the RGB values
    print("Average: " + str(average)) # Print the average to the console

    # If the average is less than the tolerance, the sensor is over a line
    if average < LIGHT_TOLERANCE + offset: # If the average is less than the tolerance, the sensor is over a line
        if R > G and R > B: # If the red value is the highest, it is a red marker
            handleRed() # Handle the red marker
            if len(turns) == 3: # If there are 3 turns, stop the robot
                ev3.speaker.play_file(SoundFile.CONFIRM) # Play a sound
                ROBOT.stop() # Stop the robot
                raise SystemExit # Exit the program
        else: # Otherwise it is not a red marker
            print("Line is detected") # Print to the console
        return True # Return true
    else: # Otherwise it is not over a line
        print("Line is not detected") # Print to the console
        return False # Return false

# Main loop that follows the line
def mainLoop(): # Main loop that follows the line
    print("Main loop is starting") # Print to the console
    while True: # Infinite loop
        if senseColour(): # If it sees the line, go right
            LEFT_WHEEL.run(SPEED_FAST) # Run the left wheel at the fast speed
            RIGHT_WHEEL.run(SPEED_SLOW) # Run the right wheel at the slow speed
        else:  # Otherwise go left
            LEFT_WHEEL.run(SPEED_SLOW) # Run the left wheel at the slow speed
            RIGHT_WHEEL.run(SPEED_FAST) # Run the right wheel at the fast speed
        # If the ultrasonic sensor sees an object, stop the robot and turn around
        if ULTRASOUND_SENSOR.distance() < 100: # If the ultrasonic sensor sees an object, stop the robot and turn around
            ROBOT.stop() # Stop the robot
            ev3.speaker.play_file(SoundFile.BACKING_ALERT) # Play a sound
            ROBOT.drive_time(-100, 0, 1000) # Drive backwards for 1 second
            ROBOT.drive_time(100, 90, 1000) # Turn around for 1 second
            ROBOT.drive_time(100, 0, 500) # Drive forward for 1 second
            ROBOT.drive_time(100, 90, 1000) # Turn around for 1 second
            ROBOT.drive_time(100, 0, 500) # Drive forward for 1 second

#The loop wich runs the menu loop. This loop keeps running while the robot is active
while True: #Start of the menu loop
    button = wait_for_button(ev3) #Wait define buttons
    if button == Button.LEFT: #If the left button is clicked
        ev3.speaker.beep(1000) #Sound with frequency 1000
    elif button == Button.RIGHT: #If the right button is clicked
        ev3.speaker.beep(1000) #Sound with frequency 1000                
    elif button == Button.UP: #Sound with frequency 120
        ev3.speaker.beep(1000) #Sound with frequency 1000
    elif button == Button.DOWN: #If the down button is clicked
        ev3.speaker.beep(1000) #Sound with frequency 1000
    elif button == Button.CENTER: #If the center button is clicked
        mainLoop() # Run the main loop function when the program starts running


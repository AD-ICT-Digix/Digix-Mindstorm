#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Color Sensor Down Program
----------------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""

#!/usr/bin/env pybricks-micropython

ev3 = EV3Brick()
left_motor = Motor(Port.B)  # left motor
right_motor = Motor(Port.C)  # right motor
feed_motor = Motor(Port.A)  # dispenser motor for color squares
line_sensor = ColorSensor(Port.S3)  # color sensor for line following
# ultrasonic sensor for obstacle avoidance
obstacle_sensor = UltrasonicSensor(Port.S2)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Calculate the light threshold. Choose values based on your measurements.
BLACK = 9  # TODO: log the black tape value
WHITE = 85
threshold = (BLACK + WHITE) / 2

# Set the drive speed at 100 millimeters per second.
DRIVE_SPEED = 200

# Set the gain of the proportional line controller. This means that for every
# percentage point of light deviating from the threshold, we set the turn
# rate of the drivebase to 1.2 degrees per second.

# For example, if the light value deviates from the threshold by 10, the robot
# steers at 10*1.2 = 12 degrees per second.
PROPORTIONAL_GAIN = 1.2

# Start following the line endlessly.
while True:
    # Calculate the deviation from the threshold.
    deviation = line_sensor.reflection() - threshold

    # Calculate the turn rate.
    turn_rate = PROPORTIONAL_GAIN * deviation

    # Set the drive base speed and turn rate.
    robot.drive(DRIVE_SPEED, turn_rate)

    # You can wait for a short time or do other things in this loop.
    wait(10)
    # If the ultrasonic sensor sees an obstacle, stop the robot and beep then turn around.
    if obstacle_sensor.distance() < 200:
        robot.stop()
        ev3.speaker.beep()
        robot.drive_time(-100, 0, 1000)
        #turns around 180 degrees
        robot.drive_time(100, 180, 1000)
        robot.drive_time(100, 0, 1000)

    # If the touch sensor is pressed, stop the robot until button pressed again.
    if Button.CENTER in ev3.buttons.pressed():
        robot.stop()
        ev3.speaker.beep()
        ev3.screen.print("Press any button to continue")
        while not ev3.buttons.pressed():
            wait(10)
        ev3.screen.clear()

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
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
BLACK = 9
WHITE = 85
threshold = (BLACK + WHITE) / 2

# Set the drive speed at 100 millimeters per second.
DRIVE_SPEED = 100

# Set the gain of the proportional line controller. This means that for every
# percentage point of light deviating from the threshold, we set the turn
# rate of the drivebase to 1.2 degrees per second.

# For example, if the light value deviates from the threshold by 10, the robot
# steers at 10*1.2 = 12 degrees per second.
PROPORTIONAL_GAIN = 1.2
# initialize the feed motor
feed_motor.run_until_stalled(120)
feed_motor.run_angle(450, -180)
    
# Initialize robot movement.
def feedMotor():
    robot.stop()
    ev3.speaker.play_file(SoundFile.LASER)
    # when sorting_machine in position , dispense a color square
    feed_motor.run_angle(1500, 90)
    feed_motor.run_angle(1500, -90)
    wait(1000)

# initialize the loop by pressing the center button
while not Button.CENTER in ev3.buttons.pressed():
    pass
while True:
    # Start the line following loop.
    # Calculate the deviation from the threshold.
    deviation = line_sensor.reflection() - threshold
    # Calculate the turn rate.
    turn_rate = PROPORTIONAL_GAIN * deviation
    # Set the drive base speed and turn rate.
    robot.drive(DRIVE_SPEED, turn_rate)
    # If the ultrasonic sensor sees an obstacle, stop the robot and beep then turn around.
    if obstacle_sensor.distance() < 0:
        robot.stop()
        ev3.speaker.play_file(SoundFile.BACKING_ALERT)
        robot.drive_time(-100, 0, 1000)
        # turns around 180 degrees
        robot.drive_time(100, 180, 1000)
        robot.drive_time(100, 0, 1000)

    # if the color sensor sees a red square, stop the robot and beep then dispense a color square.
    if line_sensor.color() == Color.RED:
        feedMotor()
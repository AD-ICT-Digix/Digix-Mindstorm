#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()
motorA = Motor(Port.B)  # left motor
motorB = Motor(Port.C)  # right motor
feed_motor = Motor(Port.A)  # dispenser motor for color squares
line_sensor = ColorSensor(Port.S3)  # color sensor for line following
# ultrasonic sensor for obstacle avoidance
obstacle_sensor = UltrasonicSensor(Port.S2)

POSSIBLE_COLORS = (Color.RED, Color.GREEN, Color.BLUE,
                   Color.YELLOW)  # colors of the color squares

ev3.speaker.beep()  # beep to indicate program start
robot = DriveBase(motorA, motorB, wheel_diameter=55.5,
                  axle_track=104)  # create robot object
BLACK = 9  # black line threshold
WHITE = 85  # white line threshold
threshold = (BLACK + WHITE) / 2  # midpoint of black and white

DRIVE_SPEED = 100  # speed of robot
5  # speed of dispenser motor
PROPORTIONAL_GAIN = 1.2  # proportional gain for line following

while True:
    deviation = line_sensor.reflection() - threshold  # deviation from midpoint
    turn_rate = PROPORTIONAL_GAIN * deviation  # turn rate for line following
    robot.drive(DRIVE_SPEED, turn_rate)  # drive robot

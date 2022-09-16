#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

motorA = Motor(Port.B)
motorB = Motor(Port.C)
line_sensor = ColorSensor(Port.S3)
obstacle_sensor = UltrasonicSensor(Port.S2)

ev3.speaker.beep()
robot = DriveBase(motorA, motorB, wheel_diameter=55.5, axle_track=104)

# while True:

# while obstacle_sensor.distance() > 100:
#robot.drive(200, 0)
# while obstacle_sensor.distance() < 100:
# robot.turn(50)
# robot.drive(20,0)
# robot.turn(-50)
# robot.drive(20,0)
# robot.turn(-50)
# robot.drive(20,0)
# robot.turn(-50)

BLACK = 9
WHITE = 85
threshold = (BLACK + WHITE) / 2

DRIVE_SPEED = 100
5
PROPORTIONAL_GAIN = 1.2

while True:
    deviation = line_sensor.reflection() - threshold
    turn_rate = PROPORTIONAL_GAIN * deviation
    robot.drive(DRIVE_SPEED, turn_rate)

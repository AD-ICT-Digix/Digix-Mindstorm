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

# create a program follow a line using the line_sensor and then when it detechts a color it descends the color into the feed_motor
# the obstacle_sensor is used to avoid obstacles
# feed_motor is used to dispense the color squares

POSSIBLE_COLORS = (Color.RED, Color.GREEN, Color.BLUE,
                   Color.YELLOW)  # colors of the color squares

ev3.speaker.beep()  # beep to indicate program start
robot = DriveBase(motorA, motorB, wheel_diameter=55.5,
                  axle_track=104)  # create robot object
BLACK = 85  # black line threshold
WHITE = 9  # white line threshold
threshold = (BLACK + WHITE) / 2  # midpoint of black and white
DRIVE_SPEED = 100  # speed of robot
PROPORTIONAL_GAIN = 1.2  # proportional gain for line following

while True:
while obstacle_sensor.distance() > 100:
robot.drive(200, 0)
while obstacle_sensor.distance() < 100:
robot.turn(50)
robot.drive(20, 0)
robot.turn(-50)
robot.drive(20, 0)
robot.turn(-50)
robot.drive(20, 0)

while True:
    deviation = line_sensor.reflection() - threshold  # deviation from midpoint
    turn_rate = PROPORTIONAL_GAIN * deviation  # turn rate for line following
    robot.drive(DRIVE_SPEED, turn_rate)  # drive robot
    # if the color sensor detects a color square, dispense it
    if line_sensor.color() in POSSIBLE_COLORS:  # if color square is detected
        robot.stop()  # stop robot
        feed_motor.run_angle(200, 180)  # dispense color square
        ev3.screen.print("Ejecting...")
        ev3.speaker.say("Ejecting...")
    robot.drive(DRIVE_SPEED, turn_rate)  # continue line following


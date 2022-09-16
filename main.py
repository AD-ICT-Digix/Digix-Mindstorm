from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()
motorA = Motor(Port.B)  # left motor
motorB = Motor(Port.C)  # right motor
feed_motor = Motor(Port.A)  # dispenser motor for color squares
line_sensor = ColorSensor(Port.S3)  # color sensor for line following
obstacle_sensor = UltrasonicSensor(Port.S2)# ultrasonic sensor for obstacle avoidance

# create a program follow a line using the line_sensor and then when it detechts a color it descends the color into the feed_motor
# the obstacle_sensor is used to avoid obstacles
# feed_motor is used to dispense the color squares

possible_colors = (Color.RED, Color.GREEN, Color.BLUE,Color.YELLOW)  # colors of the color squares
ev3.speaker.beep()  # beep to indicate program start

# drive forward until the line is detected
robot = DriveBase(motorA, motorB, wheel_diameter=55.5,axle_track=104)  # create robot object
black = 85  # black line threshold
white = 9  # white line threshold
threshold = (black + white) / 2  # midpoint of black and white
turn_speed = 100  # speed of turning
drive_speed = 100  # speed of robot
proportional_gain = 1.2  # proportional gain for line following

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
    feed_motor.run_until_stalled(120) # initialize feed_motor
    feed_motor.run_angle(450, -180) # initialize feed_motor
    deviation = line_sensor.reflection() - threshold  # deviation from midpoint
    turn_rate = proportional_gain * deviation  # turn rate for line following
    robot.drive(drive_speed, turn_rate)  # drive robot
    # if the color sensor detects a color square, dispense it
    #switch sensor mode to color
    if line_sensor.color() in possible_colors:  # if color square is detected
        brick.sound.file(SoundFile.STOP)  # stop sound
        brick.display.image(ImageFile.STOP_1)  # stop image
        robot.stop()  # stop robot
        feed_motor.run_angle(1500, 90) # dispense color square
        feed_motor.run_angle(1500, -90) # reset feed_motor
        ev3.screen.print("Ejecting...")
        ev3.speaker.say("Ejecting...")
        robot.drive(drive_speed, turn_rate)  # continue line following

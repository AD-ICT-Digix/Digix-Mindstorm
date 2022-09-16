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
# motor a and b are used to move the robot
# feed_motor is used to dispense the color squares

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

# dispense color squares from dispenser when color sensor detects a color
brick.display.clear()

# Scanning a Color Square stores the color in a list.  The list is
# empty to start.  It will grow as colors are added to it.
color_list = []

# This loop scans the colors of the objects.  It repeats until 8
# objects are scanned and placed in the chute.  This is done by
# repeating the loop while the length of the list is less than 8.
while len(color_list) < 8:

    # Display an arrow that points to the Color Sensor.
    brick.display.image(ImageFile.FORWARD)

    # Display how many Color Squares have been scanned so far.
    brick.display.text(len(color_list))

    # Wait until the Center Button is pressed or a Color Square is
    # scanned.
    while True:
        # Store "True" if the Center Button is pressed or "False"
        # if not.
        pressed = Button.CENTER in brick.buttons()
        # Store the color measured by the Color Sensor.
        color = color_sensor.color()
        # If the Center Button is pressed or one of the possible
        # colors is detected, break out of the loop.
        if pressed or color in POSSIBLE_COLORS:
            break

    if pressed:
        # If the button was pressed, end the loop early.  It will
        # no longer wait for any Color Squares to be scanned and
        # added to the chute.
        break
    else:
        # Otherwise, a color was scanned, so it is added (appended)
        # to the list.
        color_list.append(color)

        # It should not register the same color again if it is
        # still looking at the same Color Square.  So, before
        # continuing, wait until the sensor no longer sees the
        # Color Square.
        while color_sensor.color() in POSSIBLE_COLORS:
            pass

        # Display the color that was scanned.
        brick.display.image(color)

        # Move the Color Square into the chute.
        feed_motor.run_time(1000, 1000, Stop.BRAKE)

        # Wait until the Color Square is no longer in the chute.
        while feed_motor.angle() > 0:
            pass

        # Display an arrow that points to the Color Sensor.
        brick.display.image(ImageFile.FORWARD)

        # Display how many Color Squares have been scanned so far.
        brick.display.text(len(color_list))

        # Wait until the Center Button is pressed or a Color Square
        # is scanned.
        while True:

            # Store "True" if the Center Button is pressed or
            # "False" if not.
            pressed = Button.CENTER in brick.buttons()

            # Store the color measured by the Color Sensor.
            color = color_sensor.color()

            # If the Center Button is pressed or one of the
            # possible colors is detected, break out of the loop.
            if pressed or color in POSSIBLE_COLORS:
                break

        if pressed:
            # If the button was pressed, end the loop early.  It
            # will no longer wait for any Color Squares to be
            # scanned and added to the chute.
            break

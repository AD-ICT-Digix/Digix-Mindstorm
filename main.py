#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

# Create your objects here

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize a motor at port B.
test_motor = Motor(Port.B)

# Write your program here

# Let LCD show text
ev3.screen.draw_text(40, 50, "wat ben je aan t kijken jong")

# Play a sound.
ev3.speaker.beep()

# Play a sound
ev3.speaker.beep(400, 300)
ev3.speaker.beep(500, 300)
ev3.speaker.beep(550, 300)
ev3.speaker.beep(650, 300)
ev3.speaker.beep(630, 450)
ev3.speaker.beep(630, 420)
ev3.speaker.beep(570, 600)


# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
test_motor.run_target(2000, 720)
test_motor.run_target(420, 80)

# Play music file


ev3.screen.load_image('406.png')

# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
test_motor.run_target(500, 180)
test_motor.run_target(420, 80)

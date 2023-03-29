# LEGO type:standard slot:7 autostart

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
from math import pi

hub = PrimeHub()

motl = Motor("A")


pocitadlo = 1
brambora = 0

while True:
    if (hub.left_button.was_pressed()):
        pocitadlo += 1
        if pocitadlo == 5:
            pocitadlo = 1
#    print(1)
    if pocitadlo == 1:
        hub.light_matrix.show_image('CLOCK12')

    if pocitadlo == 1 and hub.right_button.was_pressed():
        motl.start(30)
        wait_for_seconds(5)
        motl.stop()
#    print(2)
    if pocitadlo == 2:
        hub.light_matrix.show_image('CLOCK3')

    if pocitadlo == 2 and hub.right_button.was_pressed():
        motl.start(50)
        wait_for_seconds(5)
        motl.stop()
#    print(3)
    if pocitadlo == 3:
        hub.light_matrix.show_image('CLOCK6')
#    print(4)
    if pocitadlo == 4:
        hub.light_matrix.show_image('CLOCK9')
#    hub.light_matrix.off()
#    print(5)
    print("a", pocitadlo)
    
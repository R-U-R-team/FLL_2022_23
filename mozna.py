# LEGO type:standard slot:12 autostart

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from spike.operator import greater_than_or_equal_to
from math import *
from math import pi

import hub

l = hub.port.A.motor
r = hub.port.B.motor
rad = hub.port.C.motor

l.run_for_degrees(1000,50)
rad.run_for_degrees(100,-100)
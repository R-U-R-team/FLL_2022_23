# LEGO type:standard slot:12 autostart

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
from math import pi

hub = PrimeHub()
sekundy = 0
rychlost = 0
cerna = 25
bila = 99
cerna_zarovnani = cerna + 5
stred = (cerna + bila) // 2


cl = ColorSensor("E")
cr = ColorSensor("F")
mot = MotorPair("A", "B")
motr = Motor("B")
motl = Motor("A")
vzv = Motor("D")
rad = Motor("C")
timer = Timer()
yaw = hub.motion_sensor.get_yaw_angle()
resgyr = hub.motion_sensor.reset_yaw_angle()
resmot = motr.set_degrees_counted(0)
mot.set_default_speed(30)

mot.set_motor_rotation(17.6, "cm")
hub.motion_sensor.reset_yaw_angle()

def move_gyro(dalka, smer, rychl = 0, mensivetsi = "mensi", kp = 0.6, kd = 0.1, rampup="n", kon_rych = 90, reset_gyro = "y"):
    motr.set_degrees_counted(0)
    
    if(reset_gyro=="y"):
        hub.motion_sensor.reset_yaw_angle()
    
    last_error = 0

    if rampup == "y":
        if (mensivetsi == "mensi"):
            #tento loop projede jednou za 2,2222222 milisekund
            while motr.get_degrees_counted() < dalka:
                error = smer - hub.motion_sensor.get_yaw_angle()
                integracni = (smer - hub.motion_sensor.get_yaw_angle()) * kp
                derivacni = (error - last_error) * kd
                errorsteer = integracni + derivacni
                speedl = int(rychl + errorsteer)
                speedr = int(rychl - errorsteer)
                mot.start_tank_at_power(speedl, speedr)
                if rychl< kon_rych:
                    rychl = rychl + 0.25   
                last_error = error         
            mot.stop()

        elif(mensivetsi == "vetsi"):
            while motr.get_degrees_counted() > dalka:           
                errorsteer = (smer - hub.motion_sensor.get_yaw_angle())*kp
                speedl = int(rychl + errorsteer)
                speedr = int(rychl - errorsteer)
                mot.start_tank_at_power(speedl, speedr)
                print(errorsteer)
            mot.stop()

    elif rampup == "n":
        if (mensivetsi == "mensi"):
            while motr.get_degrees_counted() < dalka:            
                errorsteer = (smer - hub.motion_sensor.get_yaw_angle())*kp
                speedl = int(rychl + errorsteer)
                speedr = int(rychl - errorsteer)
                mot.start_tank_at_power(speedl, speedr)
                print(errorsteer)
            mot.stop()

        elif(mensivetsi == "vetsi"):
            while motr.get_degrees_counted() > dalka:           
                errorsteer = (smer - hub.motion_sensor.get_yaw_angle())*kp
                speedl = int(rychl + errorsteer)
                speedr = int(rychl - errorsteer)
                mot.start_tank_at_power(speedl, speedr)
                print(errorsteer)
            mot.stop()


def gyro_steer_r(pozitivni_zatacka, levy, pravy, moc_dlouho = 2):
    hub.motion_sensor.reset_yaw_angle()
    timer.reset()
    while hub.motion_sensor.get_yaw_angle() <= pozitivni_zatacka and timer.now()<moc_dlouho:
        mot.start_tank_at_power(levy, pravy)
    mot.stop()
    if levy == 0:
        while hub.motion_sensor.get_yaw_angle() >= pozitivni_zatacka + 1 and timer.now()<moc_dlouho:
            mot.start_tank_at_power(0, 30)
    elif pravy == 0:
        while hub.motion_sensor.get_yaw_angle() >= pozitivni_zatacka + 1 and timer.now()<moc_dlouho:
            mot.start_tank_at_power(-30, 0)
    elif levy > 0 and pravy < 0:
        while hub.motion_sensor.get_yaw_angle() >= pozitivni_zatacka + 1 and timer.now()<moc_dlouho:
            mot.start_tank_at_power(-25, 25)
    mot.stop()
    print(hub.motion_sensor.get_yaw_angle())



#ta věc se otáčí jen do 179 stupnu a do -179 stupnu neexistuje 180 stupnu


def gyro_steer_l(negativni_zatacka, levy, pravy, moc_dlouho = 2):
    hub.motion_sensor.reset_yaw_angle()
    timer.reset()
    while hub.motion_sensor.get_yaw_angle()>=negativni_zatacka and timer.now() < moc_dlouho:
        mot.start_tank_at_power(levy, pravy)
    if levy == 0:
        while hub.motion_sensor.get_yaw_angle() <= negativni_zatacka - 1 and timer.now() < moc_dlouho:
            mot.start_tank_at_power(0, -30)
    elif pravy == 0:
        while hub.motion_sensor.get_yaw_angle() <= negativni_zatacka - 1 and timer.now() < moc_dlouho:
            mot.start_tank_at_power(30, 0)
    elif levy < 0 and pravy > 0:
        while hub.motion_sensor.get_yaw_angle() <= negativni_zatacka - 1 and timer.now() < moc_dlouho:
            mot.start_tank_at_power(25, -25)
    mot.stop()
    print(hub.motion_sensor.get_yaw_angle())

hub.motion_sensor.reset_yaw_angle()


gyro_steer_r(90, 80, 0)

raise SystemExit()
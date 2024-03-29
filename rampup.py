# LEGO type:standard slot:8 autostart

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
from math import pi


class Motor_RUR(Motor):

    def rampup_sec(self, poc_rych, kon_rych, za_jak_dlouho):
        rychlosti = kon_rych - poc_rych
        za_jak_dlouho = za_jak_dlouho / rychlosti
        abs_za_jak_dlouho = abs(za_jak_dlouho)
        posun = za_jak_dlouho / abs_za_jak_dlouho
        jeste_poc = 0
        jeste_kon = 1
        while(jeste_poc < jeste_kon):
            self.start(poc_rych)
            wait_for_seconds(abs_za_jak_dlouho)
            poc_rych = int(poc_rych + posun)
            jeste_poc = poc_rych * posun
            jeste_kon = kon_rych * posun
        self.stop()

class Motor_Rur(MotorPair):
    def move_gyro(self, dalka, smer, rychl):
        self.set_degrees_counted(0)
        PrimeHub().motion_sensor.reset_yaw_angle()

        while self.get_degrees_counted() < dalka:
            Prop = 0.6
            errorsteer = (smer - PrimeHub().motion_sensor.get_yaw_angle())*Prop
            speedl = int(rychl + errorsteer)
            speedr = int(rychl - errorsteer)
            self.start_tank_at_power(speedl, speedr)
            print(errorsteer)
        self.stop()

hub = PrimeHub()
sekundy = 0
rychlost = 0
cerna = 37
bila = 99
cerna_zarovnani = cerna + 5
stred = (cerna + bila) // 2


cl = ColorSensor("E")
cr = ColorSensor("F")
mot = Motor_Rur("A", "B")
motr = Motor("B")
motl = Motor("A")
vzv = Motor_RUR("D")
rad = Motor("C")
yaw = hub.motion_sensor.get_yaw_angle()
resgyr = hub.motion_sensor.reset_yaw_angle()
resmot = motr.set_degrees_counted(0)
mot.set_default_speed(30)

mot.set_motor_rotation(17.6, "cm") 
hub.motion_sensor.reset_yaw_angle()

def move_sec(rychlostl, rychlostr, sekundy):
    mot.start_tank(rychlostl, rychlostr)
    wait_for_seconds(sekundy)
    mot.stop()

def move_gyro(dalka, smer, rychl):
    motr.set_degrees_counted(0)
    hub.motion_sensor.reset_yaw_angle()

    while motr.get_degrees_counted() < dalka:
        Prop = 0.6
        errorsteer = (smer - hub.motion_sensor.get_yaw_angle())*Prop
        speedl = int(rychl + errorsteer)
        speedr = int(rychl - errorsteer)
        mot.start_tank_at_power(speedl, speedr)
        print(errorsteer)
    mot.stop()

def gyro_steer_r(pozitivni_zatacka, levy, pravy):
    hub.motion_sensor.reset_yaw_angle()
    while hub.motion_sensor.get_yaw_angle()<pozitivni_zatacka:
        mot.start_tank_at_power(levy, pravy)
    mot.stop()
#ta věc se otáčí jen do 179 stupnu a do -179 stupnu neexistuje 180 stupnu
def gyro_steer_l(negativni_zatacka, levy, pravy):
    hub.motion_sensor.reset_yaw_angle()
    while hub.motion_sensor.get_yaw_angle()>negativni_zatacka:
        mot.start_tank_at_power(levy, pravy)
    mot.stop()

def zarovnani_l(rychlost_leva, rychlost_prava):
    while cl.get_reflected_light()>cerna_zarovnani:
        mot.start_tank_at_power(rychlost_leva, rychlost_prava)
    mot.stop()
    while cr.get_reflected_light()>stred:
        mot.start_tank_at_power(0, rychlost_prava)
    mot.stop()
    while cl.get_reflected_light()<cerna_zarovnani:
        mot.start_tank_at_power(-15, 0)
    mot.stop()
    while cl.get_reflected_light()<stred:
        mot.start_tank_at_power(-10, 0)
    mot.stop()
    while cr.get_reflected_light()<stred:
        mot.start_tank_at_power(0, -15)
    mot.stop()

def zarovnani_r(rychlost_leva, rychlost_prava):
    while cr.get_reflected_light()>cerna_zarovnani:
        mot.start_tank_at_power(rychlost_leva, rychlost_prava)
    mot.stop()
    while cl.get_reflected_light()>stred:
        mot.start_tank_at_power(rychlost_leva, 0)
    mot.stop()
    while cr.get_reflected_light()<cerna_zarovnani:
        mot.start_tank_at_power(0, -15)
    mot.stop()
    while cr.get_reflected_light()<stred:
        mot.start_tank_at_power(0, -10)
    mot.stop()
    while cl.get_reflected_light()<stred:
        mot.start_tank_at_power(-15, 0)
    mot.stop()

def jizda_po_care(jak_daleko, jak_rychle = 30, jaky_senzor = "r", strana = "r", kp = 0.075, ki = 0.001, kd = 0.1):
    motr.set_degrees_counted(0)
    error = 0
    integracni = 0
    derivacni = 0
    soucet_kp = 0
    soucet_ki = 0
    soucet_kd = 0
    last_error = 0
    soucet = 0
    while motr.get_degrees_counted()< jak_daleko:
        if jaky_senzor == "l":
            error = cl.get_reflected_light() - stred
        elif jaky_senzor == "r":
            error = cr.get_reflected_light() - stred
        integracni = integracni + error
        derivacni = error - last_error
        soucet_kp = kp * error
        soucet_ki = ki * integracni
        soucet_kd = kd * derivacni
        soucet = soucet_kp + soucet_ki + soucet_kd
        if strana == "l":
            motor_levy = int(jak_rychle + soucet)
            motor_pravy = int(jak_rychle - soucet)
            mot.start_tank_at_power(motor_levy, motor_pravy)
        elif strana == "r":
            motor_levy = int(jak_rychle - soucet)
            motor_pravy = int(jak_rychle + soucet)
            mot.start_tank_at_power(motor_levy, motor_pravy)
        last_error = error
        print(soucet)
    mot.stop()

mot.move_gyro(1500, 0, 30)
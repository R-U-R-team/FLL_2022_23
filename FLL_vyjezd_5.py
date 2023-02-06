# LEGO type:standard slot:5 autostart

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from spike.operator import less_than
from math import *
from math import pi

hub = PrimeHub()
sekundy = 0
rychlost = 0
cerna = 37
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

def move_gyro(dalka, smer, rychl, mensivetsi = "mensi"):
    motr.set_degrees_counted(0)
    hub.motion_sensor.reset_yaw_angle()

    if (mensivetsi == "mensi"):
        while motr.get_degrees_counted() < dalka:
            Prop = 0.6
            errorsteer = (smer - hub.motion_sensor.get_yaw_angle())*Prop
            speedl = int(rychl + errorsteer)
            speedr = int(rychl - errorsteer)
            mot.start_tank_at_power(speedl, speedr)
            print(errorsteer)
        mot.stop()

    elif(mensivetsi == "vetsi"):
        while motr.get_degrees_counted() > dalka:
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
    while cl.get_reflected_light()>=cerna_zarovnani:
        mot.start_tank_at_power(rychlost_leva, rychlost_prava)
    mot.stop()
    while cr.get_reflected_light()>=stred:
        mot.start_tank_at_power(0, rychlost_prava)
    mot.stop()
    while cl.get_reflected_light()<=cerna_zarovnani:
        mot.start_tank_at_power(-25, 0)
    mot.stop()
    while cl.get_reflected_light()<=stred:
        mot.start_tank_at_power(-25, 0)
    mot.stop()
    while cr.get_reflected_light()<=stred:
        mot.start_tank_at_power(0, -25)
    mot.stop()

def zarovnani_r(rychlost_leva, rychlost_prava):
    while cr.get_reflected_light()>=cerna_zarovnani:
        mot.start_tank_at_power(rychlost_leva, rychlost_prava)
    mot.stop()
    while cl.get_reflected_light()>=stred:
        mot.start_tank_at_power(rychlost_leva, 0)
    mot.stop()
    while cr.get_reflected_light()<=cerna_zarovnani:
        mot.start_tank_at_power(0, -25)
    mot.stop()
    while cr.get_reflected_light()<=stred:
        mot.start_tank_at_power(0, -25)
    mot.stop()
    while cl.get_reflected_light()<=stred:
        mot.start_tank_at_power(-25, 0)
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

hub.motion_sensor.reset_yaw_angle()

move_gyro(650, 0, 50)
wait_for_seconds(0.3)
gyro_steer_l(-40, 0, 50)

move_gyro(500, 0, 50)
vzv.run_for_degrees(360, 100)
#wait_for_seconds(0.3)
vzv.run_for_degrees(350, -100)
move_gyro(350, 0, 50)
vzv.run_for_degrees(330, 100)
gyro_steer_l(-15, -30, 30)
move_gyro(590, 0, 50)
gyro_steer_l(-28, -40, 0)
mot.start_tank(40, 40)
wait_until(cl.get_reflected_light, less_than, cerna_zarovnani)
mot.stop()
#zarovnani_l(30, 30)
move_gyro(150, 0, 50)
vzv.run_for_degrees(340, -100)
move_gyro(-80, 0, -50, "vetsi")
wait_for_seconds(0.8)
vzv.run_for_degrees(340, 100)
move_gyro(-180, 0, -50, "vetsi")
gyro_steer_r(35, 30, -30)
vzv.run_for_degrees(340, -100)
move_gyro(400, 0, 50)
rad.run_for_seconds(0.7, -50)
wait_for_seconds(1)
rad.run_for_seconds(0.5, 100)
#gyro_steer_l(-10, -30, 30)
move_gyro(120, 0, 50)
vzv.run_for_seconds(0.9, 100)




#zarovnani_l(30, 30)
#move_gyro(200, 0, 50)
#vzv.run_for_degrees(340, -100)
#move_gyro(-130, 0, -50, "vetsi")
##vzv.run_for_degrees(330, 100)
##move_gyro(-100, 0, -50, "vetsi")
#vzv.run_for_degrees(330, -100)
#gyro_steer_r(45, 30, -30)





#wait_for_seconds(0.3)
#move_gyro(-150, 0, -30, "vetsi")
#vzv.run_for_degrees(380, 30)
#mot.move_tank(230, "degrees", -40, -35)
#vzv.run_for_degrees(120, -100)
#wait_for_seconds(0.3)
#move_gyro(250, 0, 30)







#move_gyro(-180, 0, -30, "vetsi")
#vzv.run_for_degrees(100, -100)
#move_gyro(300, 0, 50)

#vzv.run_for_degrees(280, -100)
#move_gyro(400, 0, 50)

#move_gyro(150, 0, 50)

#gyro_steer_l(-20, 0, 50)

#mot.start_tank(50, 50)
#wait_until(cl.get_reflected_light, less_than, cerna_zarovnani)
#mot.stop()
#gyro_steer_l(-40, -30, 30)


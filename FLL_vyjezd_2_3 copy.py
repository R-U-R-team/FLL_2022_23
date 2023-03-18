# LEGO type:standard slot:12 autostart

from spike import PrimeHub, ColorSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until
from spike.operator import *
from spike.control import Timer

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

def move_sec(rychlostl, rychlostr, sekundy):
    mot.start_tank(rychlostl, rychlostr)
    wait_for_seconds(sekundy)
    mot.stop()

def move_gyro(dalka, smer, rychl, mensivetsi = "mensi", Prop=0.6, rampup="n", kon_rych = 90,):
    motr.set_degrees_counted(0)
    hub.motion_sensor.reset_yaw_angle()
    if rampup == "y":

        if (mensivetsi == "mensi"):
            timer.reset()
            #tento loop projede jednou za 2,2222222 milisekund
            while motr.get_degrees_counted() < dalka:
                errorsteer = (smer - hub.motion_sensor.get_yaw_angle())*Prop
                speedl = int(rychl + errorsteer)
                speedr = int(rychl - errorsteer)
                mot.start_tank_at_power(speedl, speedr)
                if rychl< kon_rych:
                    rychl = rychl + 0.5
                elif rychl == kon_rych:
                    cas = timer.now()
            print(cas)
            mot.stop()

        elif(mensivetsi == "vetsi"):
            while motr.get_degrees_counted() > dalka:           
                errorsteer = (smer - hub.motion_sensor.get_yaw_angle())*Prop
                speedl = int(rychl + errorsteer)
                speedr = int(rychl - errorsteer)
                mot.start_tank_at_power(speedl, speedr)
                print(errorsteer)
            mot.stop()

    elif rampup == "n":
        if (mensivetsi == "mensi"):
            while motr.get_degrees_counted() < dalka:            
                errorsteer = (smer - hub.motion_sensor.get_yaw_angle())*Prop
                speedl = int(rychl + errorsteer)
                speedr = int(rychl - errorsteer)
                mot.start_tank_at_power(speedl, speedr)
                print(errorsteer)
            mot.stop()

        elif(mensivetsi == "vetsi"):
            while motr.get_degrees_counted() > dalka:           
                errorsteer = (smer - hub.motion_sensor.get_yaw_angle())*Prop
                speedl = int(rychl + errorsteer)
                speedr = int(rychl - errorsteer)
                mot.start_tank_at_power(speedl, speedr)
                print(errorsteer)
            mot.stop()


def gyro_steer_r(pozitivni_zatacka, levy, pravy):
    hub.motion_sensor.reset_yaw_angle()
    while hub.motion_sensor.get_yaw_angle()<=pozitivni_zatacka:
        mot.start_tank_at_power(levy, pravy)
    mot.stop()
#ta věc se otáčí jen do 179 stupnu a do -179 stupnu neexistuje 180 stupnu
def gyro_steer_l(negativni_zatacka, levy, pravy):
    hub.motion_sensor.reset_yaw_angle()
    timer.reset()
    while hub.motion_sensor.get_yaw_angle()>=negativni_zatacka and timer.now()<3:
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

def zarovnani_rozpoznani(rychlost_leva, rychlost_prava):
    while(cr.get_reflected_light()>=cerna_zarovnani and cl.get_reflected_light()>=cerna_zarovnani):
        mot.start_tank(rychlost_leva, rychlost_prava)
    if(cl.get_reflected_light()<=cerna_zarovnani):
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
    elif(cr.get_reflected_light()<=cerna_zarovnani):
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

hub.status_light.on('red')
hub.light_matrix.show_image('CLOCK3')
hub.right_button.wait_until_pressed()
hub.light_matrix.off()
hub.status_light.on("green")
wait_for_seconds(0.5)

move_gyro(1290, 2.5, 0, "mensi", 2, "y")
rad.run_for_degrees(120, 100)
mot.move_tank(4, "cm", 25, 25)
jizda_po_care(400, 30, "l", "l", 0.2)
move_gyro(630, 0, 80, "mensi", 2)
gyro_steer_r(40, 65, 0)
move_gyro(150, 0, 80)
vzv.run_for_degrees(250, 100)
gyro_steer_r(6, 40, -40)
wait_for_seconds(0.5)
gyro_steer_l(-2, -40, 40)
vzv.run_for_degrees(250, -100)
gyro_steer_l(-45, -60, 30)
move_gyro(800, 0, 95)

raise SystemExit
#koneeec
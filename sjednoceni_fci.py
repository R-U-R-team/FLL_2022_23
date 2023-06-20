from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from spike.operator import greater_than_or_equal_to
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
timer = Timer()


def move_gyro(dalka, smer, rychl, mensivetsi = "mensi", Prop=0.6, rampup="n", kon_rych = 90, reset_gyro = "y"):
    motr.set_degrees_counted(0)
    
    if(reset_gyro=="y"):
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


def gyro_steer_r(pozitivni_zatacka, levy, pravy, reset_gyro="y"):
    if(reset_gyro=="y"):
        hub.motion_sensor.reset_yaw_angle()
    timer.reset()
    while hub.motion_sensor.get_yaw_angle()<=pozitivni_zatacka and timer.now()<3:
        mot.start_tank_at_power(levy, pravy)
    mot.stop()
#ta věc se otáčí jen do 179 stupnu a do -179 stupnu neexistuje 180 stupnu
def gyro_steer_l(negativni_zatacka, levy, pravy, reset_gyro="y"):
    if(reset_gyro=="y"):
        hub.motion_sensor.reset_yaw_angle()
    timer.reset()
    while hub.motion_sensor.get_yaw_angle()>=negativni_zatacka and timer.now()<3:
        mot.start_tank_at_power(levy, pravy)
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

def jizda_po_care_na_senzor(zastavovaci_senzor = "l", jak_rychle = 30, jaky_senzor = "r", strana = "r", kp = 0.075, ki = 0.001, kd = 0.1):
    motr.set_degrees_counted(0)
    error = 0
    integracni = 0
    derivacni = 0
    soucet_kp = 0
    soucet_ki = 0
    soucet_kd = 0
    last_error = 0
    soucet = 0
    if zastavovaci_senzor == "l":
        zastavovaci_strana=cl
    elif zastavovaci_senzor =="r":
        zastavovaci_strana=cr
    while zastavovaci_strana.get_reflected_light()>=cerna_zarovnani:
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


def jizda_po_care(zastavovani = "degrees", **kwargs):
    if zastavovani == "degrees":
        return kwargs.get(jak_daleko = 0, jak_rychle = 30, jaky_senzor = "r", strana = "r", kp = 0.075, ki = 0.001, kd = 0.1)
    elif zastavovani == "senzor":
        return kwargs.get(zastavovaci_senzor = "l", jak_rychle = 30, jaky_senzor = "r", strana = "r", kp = 0.075, ki = 0.001, kd = 0.1)
    
    motr.set_degrees_counted(0)
    error = 0
    integracni = 0
    derivacni = 0
    soucet_kp = 0
    soucet_ki = 0
    soucet_kd = 0
    last_error = 0
    soucet = 0
    if zastavovani =="degrees":
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

    elif zastavovani == "senzor":
        if zastavovaci_senzor == "l":
            zastavovaci_strana=cl
        elif zastavovaci_senzor =="r":
            zastavovaci_strana=cr
        while zastavovaci_strana.get_reflected_light()>=cerna_zarovnani:
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




#jede_ropa
        mot.move_tank(10, "cm", 50, 50)
        #vzv.run_for_degrees(-280, 100)
        jizda_po_care(1150, 50, "l", "l", 0.36)
        wait_for_seconds(0.3)
        mot.move_tank(5, "cm", -30, -30)
        vzv.run_for_degrees(280, 100)
        vzv.run_for_degrees(-280, 100)
        for i in range(2):
            vzv.run_for_degrees(280, 100)
            vzv.run_for_degrees(-280, 100)

        #jede RUR
        mot.move_tank(4, "cm", 40, 40)
        vzv.run_for_degrees(280, 100)
        move_sec(30, 30, 1.2)
        mot.move_tank(5, "cm", -30, -30)
        vzv.run_for_degrees(-300, 100)
        mot.move_tank(10, "cm", -40, -40)
        gyro_steer_r(33.5, 30, -30)
        wait_for_seconds(0.3)

        #jede mochyta
        mot.move_tank(23, "cm", 35, 35)
        gyro_steer_r(60, 35, 0)
        wait_for_seconds(0.1)
        mot.move_tank(10, "cm", -40, -40)
        wait_for_seconds(0.1)
        gyro_steer_r(33, 40, -40)
        wait_for_seconds(0.1)
        mot.start_tank_at_power(50, 50)
        wait_until(cl.get_reflected_light, greater_than_or_equal_to, 90)
        mot.move_tank(5, "cm", 50, 50)
        wait_for_seconds(0.1)
        gyro_steer_l(-35, 0, 50)
        jizda_po_care(620, 50, "r", "r", 0.40)

        #vrací se se vším
        rad.run_for_seconds(0.4, -100)
        mot.move_tank(21.5, "cm", -40, -40)
        wait_for_seconds(0.1)
        gyro_steer_l(-37, -50, 0)
        wait_for_seconds(0.1)
        mot.move_tank(30, "cm", -50, -50)
        wait_for_seconds(0.1)
        gyro_steer_l(-20, -40, 0)
        mot.move_tank(17, "cm", -50, -50)
        gyro_steer_l(-25, -50, 50)
        mot.move_tank(20, "cm", -50, -50)
        rad.run_for_seconds(0.5, 100)
        mot.move_tank(30, "cm", -100, -100)
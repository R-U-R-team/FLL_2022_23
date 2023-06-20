# LEGO type:standard slot:5 autostart

from spike import PrimeHub, ColorSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from spike.operator import less_than, greater_than_or_equal_to, less_than_or_equal_to

#zakladni definice
hub = PrimeHub()
sekundy = 0
rychlost = 0
cerna = 25
bila = 99
cerna_zarovnani = cerna + 5
stred = (cerna + bila) // 2
pocitadlo = 1

cl = ColorSensor("E")
cr = ColorSensor("F")
mot = MotorPair("A", "B")
motr = Motor("B")
motl = Motor("A")
vzv = Motor("D")
rad = Motor("C")
timer = Timer()


#funkce

#pokus se to odstranit
def move_sec(rychlostl, rychlostr, sekundy):
    mot.start_tank(rychlostl, rychlostr)
    wait_for_seconds(sekundy)
    mot.stop()
#pokus se to odstranit

def move_gyro(dalka, smer, rychl = 0, mensivetsi = "mensi", kp = 0.6, kd = 0.15, rampup="n", kon_rych = 90, reset_gyro = "y"):
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
                    rychl = rychl + 0.5 
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


def gyro_steer_r(pozitivni_zatacka, levy, pravy, dorovnani = "y", mot_stop = "y", moc_dlouho = 2):
    hub.motion_sensor.reset_yaw_angle()
    timer.reset()
    while hub.motion_sensor.get_yaw_angle() <= pozitivni_zatacka and timer.now()<moc_dlouho:
        mot.start_tank_at_power(levy, pravy)
    if mot_stop == "y":
        mot.stop()
    if dorovnani == "y":
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

def gyro_steer_l(negativni_zatacka, levy, pravy, dorovnani = "y", mot_stop = "y", moc_dlouho = 2):
    hub.motion_sensor.reset_yaw_angle()
    timer.reset()
    while hub.motion_sensor.get_yaw_angle()>=negativni_zatacka and timer.now() < moc_dlouho:
        mot.start_tank_at_power(levy, pravy)
    if mot_stop == "y":
        mot.stop()
    if dorovnani == "y":
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


#nadprogram
while True:
    if hub.left_button.was_pressed():
        pocitadlo += 1
        if pocitadlo >= 3:
            pocitadlo = 1

    #jednicka
    if pocitadlo == 1:
        hub.speaker.set_volume(100)
        hub.speaker.start_beep(70)
        hub.status_light.on('red')
        hub.light_matrix.write('1')

    if pocitadlo == 1 and hub.right_button.was_pressed():

        hub.speaker.stop()
        hub.light_matrix.off()
        hub.status_light.on("green")

        hub.motion_sensor.reset_yaw_angle()

        #mot.move_tank(10, "cm", 50, 50)
        #jizda_po_care(1150, 50, "l", "l", 0.36)
        #gyro_steer_r(34, 30, -30)
        #mot.move_tank(20, "cm", 35, 35)
        #vzv.run_for_seconds(1, -100)
        #mot.move_tank(120, "cm", -90, -90)


        move_gyro(1650, 0.1, 0, "mensi", 4, 0.2, "y")
        vzv.run_for_seconds(1, -100)
        mot.move_tank(120, "cm", -90, -90)
        #mot.move_tank(1, "seconds", 50, 50)
        #wait_for_seconds(0.3)
        #mot.move_tank(120, "degrees", -50, -50)
        #hub.motion_sensor.reset_yaw_angle()
        #gyro_steer_r(45, 60, 0)
        #mot.move_tank(2, "cm", 40, 40)
        #vzv.run_for_seconds(0.5, 100)
        #gyro_steer_r(44, 60, 40)
        #move_gyro(1600, 0.1, 0, "mensi", 4, 0.2, "y")
        #vzv.run_for_seconds(0.5, -100)
        #move_gyro(-2000, 0.1, -90, "vetsi", 4, 0.2)
        #gyro_steer_r(95, 40, -40)
        #move_gyro(1600, 0.1, 95, "mensi", 4, 0.2)

        pocitadlo = pocitadlo + 1
    if pocitadlo == 2:
        hub.speaker.set_volume(100)
        hub.speaker.start_beep(80)
        hub.status_light.on('red')
        hub.light_matrix.write('2')


    if pocitadlo == 2 and hub.right_button.was_pressed():

        hub.speaker.stop()
        hub.light_matrix.off()
        hub.status_light.on("green")

        hub.motion_sensor.reset_yaw_angle()

        vzv.run_for_seconds(0.5, 100)


# LEGO type:standard slot:0 autostart

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
        if pocitadlo >= 5:
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

        #jede televize
        move_gyro(690, 0, 0, "mensi", 2, 0.15, "y", 70)
        wait_for_seconds(0.3)
        mot.move_tank(10, "cm", -40, -40)
        gyro_steer_l(-40, -45, 45)

        #jede vrtule
        wait_for_seconds(0.3)
        move_gyro(1050, 0, 0, "mensi", 2, 0.15, "y", 80)
        gyro_steer_r(80, 0, -70)
        mot.move_tank(10, "cm", 50, 50)
        move_sec(50, 50, 0.6)
        wait_for_seconds(0.3)
        mot.move_tank(5, "cm", -50, -50)
        wait_for_seconds(0.3)
        move_sec(50, 50, 0.5)
        wait_for_seconds(0.3)
        mot.move_tank(5, "cm", -50, -50)
        wait_for_seconds(0.3)
        move_sec(50, 50, 0.5)
        wait_for_seconds(0.3)

        #jede trychtýř
        mot.move_tank(15, "cm", -40, -40)
        rad.run_for_seconds(1.3, -50)
        vzv.run_for_degrees(100, 100)
        gyro_steer_l(-90, -35, 35)
        #jedna z věcí pro úpravu na levo nebo na pravo od trychtýře -, +
        mot.move_tank(5.5, "cm", 40, 40)
        #jedna z věcí pro úpravu na levo nebo na pravo od trychtýře -, +
        gyro_steer_l(-92, -35, 35)
        vzv.run_for_degrees(90, -80)
        mot.move_tank(0.5, "seconds", 40, 40)
        rad.run_for_seconds(0.5, 50)
        wait_for_seconds(0.5)
        rad.run_for_seconds(0.5, -50)

        #jede baze
        mot.move_tank(5, "cm", -50, -50)
        gyro_steer_l(-60, -90, 90, "n")
        move_sec(100, 100, 1.75)
        pocitadlo +=1

    #dvojka
    if pocitadlo == 2:
        hub.speaker.set_volume(100)
        hub.speaker.start_beep(75)
        hub.status_light.on('red')
        hub.light_matrix.write('2')

    if pocitadlo == 2 and hub.right_button.was_pressed():

        hub.speaker.stop()
        hub.light_matrix.off()
        hub.status_light.on("green")

        hub.motion_sensor.reset_yaw_angle()

        #power kytka
        move_gyro(1290, 1.8, 0, "mensi", 2.5, 0.15, "y")
        rad.run_for_degrees(120, 100)
        mot.move_tank(4, "cm", 25, 25)
        jizda_po_care(400, 30, "l", "l", 0.2)

        #jede vodník
        move_gyro(600, 0, 0, "mensi", 2, 0.15, "y", 90)
        hub.motion_sensor.reset_yaw_angle()
        vzv.run_for_degrees(250, 100)
        gyro_steer_r(50, 65, 0)
        move_gyro(150, 0, 0, "mensi", 2, 0.15, "y", 90)
        gyro_steer_r(8, 40, -40, "n")
        wait_for_seconds(0.5)
        gyro_steer_l(-1, -40, 40, "n")
        vzv.run_for_degrees(250, -100)

        #jede do bazu
        gyro_steer_l(-40, -80, 80, "n")
        move_gyro(800, 0, 90, "mensi", 2, 0.15, "n")
        pocitadlo +=1
    
    if pocitadlo == 3:
        hub.speaker.set_volume(100)
        hub.speaker.start_beep(80)
        hub.status_light.on('red')
        hub.light_matrix.write('3')

    #trojka
    if pocitadlo == 3 and hub.right_button.was_pressed():

        hub.speaker.stop()
        hub.light_matrix.off()
        hub.status_light.on("green")

        hub.motion_sensor.reset_yaw_angle()

        #jede_ropa
        mot.move_tank(8, "cm", 50, 50)
        vzv.run_for_degrees(-280, 100)
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
        gyro_steer_l(-40, 0, 50)
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
        gyro_steer_l(-30, -50, 50)
        mot.move_tank(20, "cm", -50, -50)
        rad.run_for_seconds(0.5, 100)
        mot.move_tank(30, "cm", -100, -100)
        pocitadlo += 1

    if pocitadlo == 4:
        hub.speaker.set_volume(100)
        hub.speaker.start_beep(85)
        hub.status_light.on('red')
        hub.light_matrix.write('4')

    #ctverka
    if pocitadlo == 4 and hub.right_button.was_pressed():

        hub.speaker.stop()
        hub.light_matrix.off()
        hub.status_light.on("green")

        hub.motion_sensor.reset_yaw_angle()

        #jede vodníka
        move_gyro(760, 0, 50, "mensi", 2)
        wait_for_seconds(0.3)
        gyro_steer_l(-39, -35, 35, "y")
        wait_for_seconds(0.3)
        move_gyro(555, 0, 50, "mensi", 2)
        vzv.run_for_degrees(200, 30)
        wait_for_seconds(0.5)
        vzv.run_for_seconds(0.4, 100)
        wait_for_seconds(0.3)
        vzv.run_for_seconds(1, -100)

        #jede bílý kontejner
        move_gyro(80, 0, 40)
        gyro_steer_r(10, 50, 0)
        move_gyro(150, 0, 40)
        vzv.run_for_seconds(0.5, 100)
        gyro_steer_l(-20, -40, 40)
        wait_for_seconds(0.1)
        move_gyro(480, 0, 0, "mensi", 2, 0.15, "y", 80)
        mot.start_tank_at_power(-50, 0)
        wait_until(cr.get_reflected_light, less_than, cerna_zarovnani)
        mot.stop()
        jizda_po_care_na_senzor("l", 35, "r", "r", 0.35)
        mot.start_tank_at_power(0, 30)
        wait_until(cr.get_reflected_light, greater_than_or_equal_to, 90)
        mot.stop()
        mot.start_tank_at_power(30, 0)
        wait_until(cl.get_reflected_light, greater_than_or_equal_to, 90)
        mot.stop()
        mot.start_tank_at_power(0, -30)
        wait_until(cr.get_reflected_light, less_than_or_equal_to, 40)
        mot.stop()
        mot.start_tank_at_power(-30, 0)
        wait_until(cl.get_reflected_light, less_than_or_equal_to, 40)
        mot.stop()

        #ruka
        move_gyro(140, 0, 50)
        vzv.run_for_seconds(0.8, -100)
        mot.move_tank(0.4, "seconds", -50, -50)
        wait_for_seconds(0.3)
        vzv.run_for_seconds(0.4, 100)
        mot.move_tank(240, "degrees", -50, -50)
        gyro_steer_r(41, 35, -35)

        #jede zbytek
        vzv.run_for_seconds(0.4, -100)
        move_gyro(480, 0, 0, "mensi", 2, 0.15, "y", 80)
        rad.run_for_seconds(0.5, -50)
        wait_for_seconds(0.5)
        rad.run_for_seconds(0.5, 100)
        rad.start(1)
        move_gyro(90, 0, 60)
        vzv.run_for_seconds(1.5, 100)
        vzv.run_for_seconds(1, -100)
        gyro_steer_l(-145, -80, 0)
        mot.move_tank(30, "cm", -60, -60)
        gyro_steer_l(-120, -80, 0)
        #gyro_steer_r(60, 40, -40)
        #mot.move_tank(15, "cm", 65, 65)
        rad.stop()
        
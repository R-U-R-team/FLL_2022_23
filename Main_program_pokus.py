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


#nadprogram
while True:
    if hub.right_button.was_pressed():
        pocitadlo =+ 1
        if pocitadlo == 5:
            pocitadlo = 1

    #jednicka
    if pocitadlo == 1:
        hub.speaker.set_volume(100)
        hub.speaker.start_beep(70)
        hub.status_light.on('red')
        hub.light_matrix.show_image('CLOCK12')

    if pocitadlo == 1 and hub.left_button.was_pressed():

        hub.speaker.stop()
        hub.light_matrix.off()
        hub.status_light.on("green")

        hub.motion_sensor.reset_yaw_angle()

        #jede televize
        move_gyro(690, 0, 60)
        wait_for_seconds(0.3)
        mot.move_tank(10, "cm", -40, -40)
        gyro_steer_l(-35, -35, 35)

        #jede vrtule
        wait_for_seconds(0.3)
        move_gyro(1050, 0, 60)
        gyro_steer_r(75, 0, -70)
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
        gyro_steer_l(-86, -35, 35)
        vzv.run_for_degrees(90, -80)
        mot.move_tank(0.5, "seconds", 40, 40)
        rad.run_for_seconds(0.5, 50)
        wait_for_seconds(0.5)
        rad.run_for_seconds(0.5, -50)

        #jede baze
        mot.move_tank(5, "cm", -50, -50)
        gyro_steer_l(-60, -90, 90)
        move_sec(100, 100, 1.75)

    #dvojka
    if pocitadlo == 2:
        hub.speaker.set_volume(100)
        hub.speaker.start_beep(70)
        hub.status_light.on('red')
        hub.light_matrix.show_image('CLOCK3')

    if pocitadlo == 2 and hub.left_button.was_pressed():

        hub.speaker.stop()
        hub.light_matrix.off()
        hub.status_light.on("green")

        hub.motion_sensor.reset_yaw_angle()

        #power kytka
        move_gyro(1290, 1.8, 0, "mensi", 2, "y")
        rad.run_for_degrees(120, 100)
        mot.move_tank(4, "cm", 25, 25)
        jizda_po_care(400, 30, "l", "l", 0.2)

        #jede vodník
        move_gyro(600, 0, 80, "mensi", 2)
        hub.motion_sensor.reset_yaw_angle()
        gyro_steer_r(39.5, 65, 0)
        move_gyro(150, 0, 80)
        vzv.run_for_degrees(250, 100)
        gyro_steer_r(6, 40, -40)
        wait_for_seconds(0.5)
        gyro_steer_l(-0.8, -40, 40)
        vzv.run_for_degrees(250, -100)

        #jede do bazu
        gyro_steer_l(-45, -60, 30)
        move_gyro(800, 0, 95)

    if pocitadlo == 3:
        hub.speaker.set_volume(100)
        hub.speaker.start_beep(70)
        hub.status_light.on('red')
        hub.light_matrix.show_image('CLOCK6')

    #trojka
    if pocitadlo == 3 and hub.left_button.was_pressed():

        hub.speaker.stop()
        hub.light_matrix.off()
        hub.status_light.on("green")

        hub.motion_sensor.reset_yaw_angle()

        #jede_ropa
        mot.move_tank(10, "cm", 50, 50)
        jizda_po_care(1150, 50, "l", "l", 0.36)
        wait_for_seconds(0.3)
        mot.move_tank(5, "cm", -30, -30)
        vzv.run_for_degrees(280, 100)
        vzv.run_for_degrees(-270, 100)
        for i in range(2):
            vzv.run_for_degrees(280, 100)
            vzv.run_for_degrees(-280, 100)

        #jede RUR
        mot.move_tank(2.8, "cm", 40, 40)
        vzv.run_for_degrees(300, 100)
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
        #mot.stop()
        mot.move_tank(5, "cm", 50, 50)
        wait_for_seconds(0.1)
        #gyro_steer_l(-20, 0, 50)
        #mot.start_tank_at_power(0, 50)
        #wait_until(cr.get_reflected_light, less_than_or_equal_to, 40)
        gyro_steer_l(-40, 0, 50)
        jizda_po_care(620, 50, "r", "r", 0.40)

        #vrací se se vším
        rad.run_for_seconds(0.4, -100)
        mot.move_tank(21.5, "cm", -40, -40)
        wait_for_seconds(0.1)
        gyro_steer_l(-35, -50, 0)
        wait_for_seconds(0.1)
        mot.move_tank(37, "cm", -50, -50)
        wait_for_seconds(0.1)
        gyro_steer_l(-15, -30, 0)
        mot.move_tank(50, "cm", -100, -100)

    if pocitadlo == 4:
        hub.speaker.set_volume(100)
        hub.speaker.start_beep(70)
        hub.status_light.on('red')
        hub.light_matrix.show_image('CLOCK9')

    #ctverka
    if pocitadlo == 4 and hub.left_button.was_pressed():

        hub.speaker.stop()
        hub.light_matrix.off()
        hub.status_light.on("green")

        hub.motion_sensor.reset_yaw_angle()

        #jede vodníka
        move_gyro(760, 0, 50)
        wait_for_seconds(0.3)
        gyro_steer_l(-38, -35, 35, "n")
        wait_for_seconds(0.3)
        move_gyro(555, 0, 50)
        vzv.run_for_degrees(200, 30)
        wait_for_seconds(0.5)
        vzv.run_for_seconds(0.4, 100)
        vzv.run_for_seconds(1, -100)

        #jede bílý kontejner
        move_gyro(80, 0, 65)
        gyro_steer_r(5, 50, 0)
        move_gyro(150, 0, 50)
        vzv.run_for_seconds(0.5, 100)
        gyro_steer_l(-15, -40, 40)
        wait_for_seconds(0.1)
        move_gyro(460, 0, 65)
        mot.start_tank_at_power(-50, 0)
        wait_until(cr.get_reflected_light, less_than, cerna_zarovnani)
        mot.stop()
        jizda_po_care_na_senzor("l", 35, "r", "r", 0.35)

        #ruka
        move_gyro(150, 0, 50)
        vzv.run_for_seconds(0.8, -100)
        mot.move_tank(0.4, "seconds", -50, -50)
        wait_for_seconds(0.3)
        vzv.run_for_seconds(0.4, 100)
        move_gyro(-240, 0, -50, "vetsi")
        gyro_steer_r(32.5, 30, -30)

        #jede zbytek
        vzv.run_for_seconds(0.4, -100)
        move_gyro(480, 0, 60)
        rad.run_for_seconds(0.5, -50)
        wait_for_seconds(0.5)
        rad.run_for_seconds(0.5, 50)
        move_gyro(95, 0, 60)
        vzv.run_for_seconds(1.5, 100)
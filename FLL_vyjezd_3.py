# LEGO type:standard slot:3 autostart

from spike import PrimeHub, ColorSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from spike.operator import greater_than_or_equal_to, less_than_or_equal_to

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
    timer.reset()
    while hub.motion_sensor.get_yaw_angle()<=pozitivni_zatacka and timer.now()<3:
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

hub.speaker.set_volume(100)
hub.speaker.start_beep(85)
hub.status_light.on('red')
hub.light_matrix.show_image('CLOCK9')
hub.right_button.wait_until_pressed()
hub.speaker.stop()
hub.light_matrix.off()
hub.status_light.on("green")
wait_for_seconds(0.5)

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

raise SystemExit
#koneec
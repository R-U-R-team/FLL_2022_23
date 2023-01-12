class Motor_RUR(Motor):

class MotorPair_RUR(MotorPair):

    def move_sec(rychlostl, rychlostr, sekundy):
        start_tank(rychlostl, rychlostr)
        wait_for_seconds(sekundy)
        stop()
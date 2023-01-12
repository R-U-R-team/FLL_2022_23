class Motor_RUR(Motor):

class MotorPair_RUR(MotorPair):

    def move_sec(self, rychlostl, rychlostr, sekundy):
        self.start_tank(rychlostl, rychlostr)
        wait_for_seconds(sekundy)
        self.stop()
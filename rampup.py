class Motor_RUR(Motor):
    def rampup(self, degrees, rychlost_start = 5, rychlost_konec = 50, krok = 1):
        rychlost = rychlost_start
        while self.get_degrees() < degrees:
            self.start_power(rychlost)
            if rychlost < rychlost_konec:
                rychlost += krok
        self.stop()
            
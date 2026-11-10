from robot import Robot

class BalancedBot(Robot):
    def __init__(self):
        super().__init__(name="BalancedBot", mass=25, motor_power=150, armour=10, battery=100)

    def setup(self):
        """print("BalancedBot online.")
        print(f"mass: {self.mass}") 
        print(f"motor power: {self.motor_power}")
        print(f"armour: {self.armour}")
        print(f"battery: {self.battery}")"""

        super().__init__(name="BalancedBot", mass=25, motor_power=150, armour=10, battery=100)
        
    def decide(self):
        if self.battery < 40:
            self.action = "repair"
        else:
            self.action = "attack"

    def repair(self):
        self.battery += 15
        #print(f"{self.name} repaired itself.")

    def act(self):
        if self.action == "repair":
            self.repair()
        else:
            self.ram_attack()
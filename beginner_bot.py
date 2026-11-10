from robot import Robot

class BeginnerBot(Robot):
    def __init__(self):
        super().__init__(name="BeginnerBot", mass=30, motor_power=120, armour=5, battery=120)

    def setup(self):
        print("BeginnerBot ready.") 
        print(f"mass: {self.mass}") 
        print(f"motor power: {self.motor_power}")
        print(f"armour: {self.armour}")
        print(f"battery: {self.battery}")
        
    def decide(self):
        self.action = "attack"

    def act(self):
        self.ram_attack()
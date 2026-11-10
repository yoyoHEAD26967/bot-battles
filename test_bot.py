from robot import Robot

class TestBot(Robot):
    def __init__(self):
        super().__init__(name="test_bot", mass=25, motor_power=150, armour=10, battery=100)

    def setup(self):
        print("TestBot online.")

    def decide(self):
        self.action = "attack"

    def act(self):
        self.ram_attack()
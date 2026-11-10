from robot import Robot

class SmartHunterBot(Robot):
    def __init__(self):
        super().__init__(name="SmartHunter", mass=20, motor_power=200, armour=8, battery=90)

    # Mandatory Over-Riding
    def setup(self):
        super().__init__(name="SmartHunter", mass=20, motor_power=200, armour=8, battery=90)

        """print("SmartHunter calibrating...")
        print(f"mass: {self.mass}") 
        print(f"motor power: {self.motor_power}")
        print(f"armour: {self.armour}")
        print(f"battery: {self.battery}")"""

    # Mandatory Over-Riding
    def decide(self):
        enemy_damage = (self.enemy.calculate_damage())

        if self.structural_integrity < 25:
            self.action = "repair"

        elif (self.enemy.battery < 30):
            self.action = "finish"

        elif enemy_damage > 15:
            self.action = "shield"

        else:
            self.action = "attack"

    def repair(self):
        self.structural_integrity += 20
        self.battery -= 10
        #print(f"{self.name} performs emergency repairs.")

    def shield(self):
        self.armour += 10
        self.battery -= 10
        #print(f"{self.name} reinforces armour.")

    def finish_move(self):
        damage = (self.calculate_damage() * 2)
        actual_damage = max(1, damage - self.enemy.armour)
        self.enemy.battery -= actual_damage
        #print(f"{self.name} uses FINISHER for {actual_damage}")

    # Mandatory Over-Riding
    def act(self):
        if self.action == "repair":
            self.repair()
        elif self.action == "shield":
            self.shield()
        elif self.action == "finish":
            self.finish_move()
        else:
            self.ram_attack()

from robot import Robot

class YahyaBot(Robot):
    def __init__(self, model = None):
        super().__init__(name="YahyaBot", mass=25, motor_power=150, armour=8, battery=100)
        self.model = model
        self.decision = None
        

    def setup(self):
        """print("Yahya has come to conquer!")

        


        print(f"mass: {self.mass}") 
        print(f"motor power: {self.motor_power}")
        print(f"armour: {self.armour}")
        print(f"battery: {self.battery}")"""
        super().__init__(name="YahyaBot", mass=25, motor_power=150, armour=8, battery=100)

        
    def decide(self):
        if self.enemy == None:
            self.action = "none"
            return

        if self.model == None:
            pass # training controls here

        else:

            self.decision = self.model.get_action(self.enemy, self)

        """
        0: repair
        1: attack
        2: special attack
        """
        
        if self.decision == 0:
            self.action = "repair"
        elif self.decision == 1:
            self.action = "ram attack"
        elif self.decision == 2:
            self.action = "special attack"
        else:
            self.action = "none"

    def repair(self):
        self.structural_integrity += 15
        #print(f"{self.name} repaired itself.")

    def special_attack(self):
        damage = self.calculate_damage() * 3
        actual_damage = int(damage - damage*self.enemy.armour_reduction())
        self.enemy.structural_integrity -= actual_damage
        self.battery = self.battery - self.RAM_BAT

        #print(f"{self.name} hit a special attack on {self.enemy.name} for {actual_damage} damage, (with armour reduction: {round(self.enemy.armour_reduction()*100,1)}%)")

    def act(self):
        if self.action == "repair":
            self.repair()
        elif self.action == "ram attack":
            self.ram_attack()
        elif self.action == "special attack":
            self.special_attack()
        else:
            pass#print(f"{self.name} didn't do anything this turn.")




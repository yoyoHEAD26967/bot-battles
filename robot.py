from abc import ABC, abstractmethod
import math

class Robot(ABC):

    DAMAGE_FACTOR = 0.1 #Constant of proportionality for damage to KE.
    ARMOUR_CONSTANT = 100
    RAM_BAT = 10

    # Robot Attributes
    def __init__(self, name, mass, motor_power, armour, battery):
        self.name = name #Name
        self.mass = mass #Mass (KiloGrams - used to determine other physical properties)
        self.motor_power = motor_power #Motor Power (Watts - used to determine other physical properties )
        self.armour = armour #Armour (Used to reduce incoming physical damage by a percentage)
        self.battery = battery #Batter (Kilo Watt Hours - represents a source of ability usage)
        self.structural_integrity = 100 #Representing robots life/ability to compete
        self.speed = motor_power / mass #Speed (m/s - the speed the robot will move with)
        self.enemy = None #The robots arena battle opponent
        self.action = None #The robots decided choice of action for the upcoming round

    @abstractmethod
    def setup(self):
        pass
    
    def sense(self, enemy):
        self.enemy = enemy
    
    @abstractmethod
    def decide(self):
        pass

    @abstractmethod
    def act(self):
        pass

    def regen(self):
        self.battery += 5

    #All robots will be called to complete this action loop.
    def loop(self, enemy):
        self.sense(enemy)
        self.decide()
        self.act()
        self.regen()

    #All robots physical damage due to a ram_attack is based on Kinetic Energy
    def calculate_damage(self):
        kinetic_energy = (0.5 * self.mass * self.speed ** 2)
        damage = int(self.DAMAGE_FACTOR * kinetic_energy)
        return damage

    def armour_reduction(self):
        AR = self.armour / (self.armour + self.ARMOUR_CONSTANT)
        return AR

    def ram_attack(self):
        damage = self.calculate_damage()
        actual_damage = int(damage - damage*self.enemy.armour_reduction())
        self.enemy.structural_integrity -= actual_damage
        self.battery = self.battery - self.RAM_BAT
        #print(f"{self.name} rammed {self.enemy.name} for {actual_damage} damage, (with armour reduction: {round(self.enemy.armour_reduction()*100,1)}%)")

    def report(self):
        pass#print(f"{self.name:<15} Battery:{self.battery:<5} Structural Integrity:{self.structural_integrity:.1f}")

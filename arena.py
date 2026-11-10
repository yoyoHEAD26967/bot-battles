from abc import abstractmethod

class Arena:
    def __init__(self, robot1, robot2):
        self.robot1 = robot1
        self.robot2 = robot2

        self.roundRunning = False

    def round(self, round_number):
            print()
            print(f"===== ROUND {round_number} =====")
            print("====== FIGHT ! ========")
            

            self.roundRunning = True

            self.robot1.loop(self.robot2)
            self.robot2.report()

            if self.robot2.structural_integrity <= 0:
                self.roundRunning = False
                return True

            self.robot2.loop(self.robot1)
            self.robot1.report()

            if self.robot1.structural_integrity <= 0:
                self.roundRunning = False
                return True

            #print()

    def get_winner(self):
        if self.roundRunning:
            return None

        """
            False means robot 1 won
            True means robot 2 won
        """

        if self.robot1.structural_integrity > 0:
            #print(f"Winner: {self.robot1.name}")
            return False
        else:
            #print(f"Winner: {self.robot2.name}")
            return True

    def setup(self):
        self.robot1.setup()    
        self.robot2.setup()   

    def run(self):
        print()
        print("=== ROBOT ARENA ===")
        print()

        print("Ladies and Gentleman, I present to you our two contestants.")
        self.setup()

        round_number = 1

        self.roundRunning = True

        while (self.robot1.battery > 0 and self.robot2.battery > 0):
        
            round(round_number)

            round_number += 1

            if not self.roundRunning:
                break

        self.get_winner()


        print()
        print("===== GAME OVER =====")

        
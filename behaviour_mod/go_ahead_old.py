from behaviour_mod.behaviour import Behaviour

class GoAhead(Behaviour):
    def __init__(self, robot, supress_list, params):
        super.__init__(robot, supress_list, params)
        self.speed = 20

    def take_control(self):
        if not self.supress:
            return True
        
    def action(self):
        print("----> control: GoAhead")
        self.supress = False
        self.robot.moveTiltTo(90,15)
        self.robot.moveWheels(self.speed, self.speed)
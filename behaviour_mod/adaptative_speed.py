from behaviour_mod.behaviour import Behaviour

class AdaptativeSpeed(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
    
    def take_control(self):
        return False
    def action(self):
        pass
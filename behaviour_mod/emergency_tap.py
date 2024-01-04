
from behaviour_mod.behaviour import Behaviour

class EmergencyTap(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.tap = False
        self.robot.whenATapIsDetected(self.tap_detected)
    
    def tap_detected(self):
        self.tap = True
    
    def take_control(self): 
        if not self.supress:
            return self.tap
        
    def action(self):
        print("----> control: EmergencyTap")
        self.supress = False
        
        for bh in self.supress_list:
            bh.supress = True
            
        self.robot.stopMotors()
        self.set_stop()
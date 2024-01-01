
from behaviour_mod.behaviour import Behaviour

class BusCheck(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.passenger = False
        self.robot.setActiveBlobs(False,False,False,True)
        self.robot.whenANewColorBlobIsDetected(self.blob_detected)
        self.allow_bus_stop = False
        
    def take_control(self):
        if not self.supress:
            return self.passenger and self.allow_bus_stop
    
    def blob_detected(self):
        self.passenger = True
    
    def action(self):
        print("----> control: BusCheck")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True
            
        '''while True:
            if self.passenger:
                self.robot.stopMotors()
                self.passenger = False
                self.robot.wait(1)
            else:
                break'''
                
        self.robot.stopMotors()
        self.robot.wait(5)
            
        self.robot.moveTiltTo(90,15,False)
        self.robot.movePanTo(0,15, True)  
        self.passenger = False
        self.allow_bus_stop = False
              
        for bh in self.supress_list:
            bh.supress = False
     
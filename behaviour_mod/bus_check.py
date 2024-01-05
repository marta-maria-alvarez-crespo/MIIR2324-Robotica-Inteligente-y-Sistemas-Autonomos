
from behaviour_mod.behaviour import Behaviour

class BusCheck(Behaviour):
    def __init__(self, robot, supress_list, params, stop_bus):
        super().__init__(robot, supress_list, params)
        self.passenger = False
        self.robot.setActiveBlobs(False,False,False,True)
        self.robot.whenANewColorBlobIsDetected(self.blob_detected)
        self.stop_bus = stop_bus
        
    def take_control(self): 
        if not self.supress:
            return self.passenger and self.stop_bus.bus_stop
    
    def blob_detected(self):
        self.passenger = True
    
    def action(self):
        print("----> control: BusCheck")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True
        self.stop_bus.finished_stop = False
        self.robot.stopMotors() 
        while True:
            if self.passenger:
                self.passenger = False
                self.robot.wait(1)
            else:
                break   
        self.robot.moveTiltTo(90,15,False)
        self.robot.movePanTo(0,15, True)
        self.stop_bus.finished_stop = True
        self.passenger = False       
        for bh in self.supress_list:
            bh.supress = False
     

from behaviour_mod.behaviour import Behaviour

class StopBus(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.bus_stop = False
        self.min_distance = 10
        self.finished_stop = True
        self.name_qr = 'autobus'
    
    def take_control(self):
        if not self.supress:
            return self.bus_stop
    
    def action(self):
        print("----> control: BusStop")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True
            
        self.robot.moveWheels(5,5)
        self.robot.moveTiltTo(105,100,False)
        self.robot.movePanTo(90,100, True)
        self.robot.wait(15)
        if self.finished_stop:
            self.robot.moveTiltTo(90,100,False)
            self.robot.movePanTo(0,100, True)
        self.bus_stop = False   
           
        for bh in self.supress_list:
            bh.supress = False
     
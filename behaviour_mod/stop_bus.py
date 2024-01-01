
from behaviour_mod.behaviour import Behaviour

class StopBus(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.bus_stop = False
        self.min_distance = 10
        self.name_qr = 'autobus'
        self.robot.whenAQRCodeIsDetected(self.QR_detected)
        
    def QR_detected(self):
        qr_distance = self.robot.readQR().distance
        qr_id = self.robot.readQR().id
        if qr_distance >= self.min_distance and qr_id == self.name_qr and not self.bus_stop:
            self.bus_stop = True
    
    def take_control(self):
        if not self.supress:
            return self.bus_stop
    
    def action(self):
        print("----> control: BusStop")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True
            
        self.robot.moveWheels(5,5)
        self.robot.moveTiltTo(105,15,False)
        self.robot.movePanTo(90,15, True)
        self.robot.wait(15)
        self.robot.moveTiltTo(90,15,False)
        self.robot.movePanTo(0,15, True)
        self.bus_stop = False   
           
        for bh in self.supress_list:
            bh.supress = False
     
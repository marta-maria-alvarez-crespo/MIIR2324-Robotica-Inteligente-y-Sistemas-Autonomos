from behaviour_mod.behaviour import Behaviour

class TurnQR(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.orientation = self.robot.readOrientationSensor().yaw
        self.turn = False
    
    def take_control(self):
        if not self.supress:
            return self.turn
    
    def action(self):
        print("----> control: TurnQR")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True
        if self.read_qr.qr_id == "peligro izquierda":
            self.robot.moveWheelsByTime(10,10,3)
            self.robot.moveWheelsByTime(11, 8, 13)
            self.robot.moveWheelsByTime(10,10,3)
            
        elif self.read_qr.qr_id == "peligro derecha":
            self.robot.moveWheelsByTime(10,10,1) #4
            self.robot.moveWheelsByTime(15, 4, 13)
            self.robot.moveWheelsByTime(10,10,1)
            
        self.turn = False
        for bh in self.supress_list:
            bh.supress = False
            
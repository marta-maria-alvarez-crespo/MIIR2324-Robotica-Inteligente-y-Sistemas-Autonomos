from behaviour_mod.behaviour import Behaviour

class TurnQR(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.orientation = self.robot.readOrientationSensor().yaw
        self.turn = False
        self.name_qr = 'peligro izquierda'
        self.robot.whenAQRCodeIsDetected(self.turn_QR_detected)

    def turn_QR_detected(self):
        qr_distance = self.robot.readQR().distance
        qr_id = self.robot.readQR().id
        if qr_distance >= 15 and qr_id == self.name_qr and not self.turn:
            self.robot.sayText(self.orientation, True)
            self.orientation = self.robot.readOrientationSensor().yaw   
            self.turn = True
    
    def take_control(self):
        if not self.supress:
            return self.turn
    
    def action(self):
        print("----> control: TurnQR")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True
        
        self.robot.moveWheelsByTime(10,10,4) 
        self.robot.moveWheelsByTime(11, 8, 13)
        self.robot.moveWheelsByTime(10,10,4)
        
        self.turn = False
        for bh in self.supress_list:
            bh.supress = False
            
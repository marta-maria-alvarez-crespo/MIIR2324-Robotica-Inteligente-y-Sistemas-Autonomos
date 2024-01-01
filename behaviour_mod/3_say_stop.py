from robobopy.Robobo import Robobo
from robobopy.utils.Orientation import Orientation
from behaviour_mod.behaviour import Behaviour

class SayStop(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.bus_stop = False
        self.min_distance = 20
        self.name_qr = 'autobus'
        self.message = 'para'
        self.robot.startSpeechDetection()
        self.robot.whenAQRCodeIsDetected(self.QR_detected)

    def QR_detected(self):
        qr_distance = self.robot.readQR().distance
        qr_id = self.robot.readQR().id
        if qr_distance >= self.min_distance and qr_id == self.name_qr:
            self.bus_stop = True
    
    def take_control(self):
        if not self.supress:
            return self.robot.readDetectedSpeech().message == self.message
    
    def action(self):
        print("----> control: SayStop")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True

        while not self.bus_stop:
            self.robot.wait(0.01)
        
        #Comportamiento parada


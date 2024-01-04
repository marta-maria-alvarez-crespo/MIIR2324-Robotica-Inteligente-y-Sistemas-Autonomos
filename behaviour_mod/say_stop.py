
from behaviour_mod.behaviour import Behaviour

class SayStop(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.heard_stop = False
        self.required.stop = False
        self.message = 'para'
        self.robot.startSpeechDetection()
        self.hearing()

    def hearing(self):
        while True:
            if self.robot.readDetectedSpeech().message == self.message:
                self.heard_stop = True
                
    def take_control(self):
        if not self.supress:
            return self.required_stop
        
    def action(self):
            print("----> control: BusCheck")
            self.supress = False
            for bh in self.supress_list:
                bh.supress = True
            
            self.robot.moveWheelsByTime(5,5,15)
            self.robot.stopMotors()
            self.robot.wait(5)
            self.heard_stop = False
            self.required_stop = False
            
            for bh in self.supress_list:
                bh.supress = False
            


from behaviour_mod.behaviour import Behaviour

class TurnQR(Behaviour):
    def __init__(self, robot, supress_list, params, update):
        super().__init__(robot, supress_list, params)
        self.orientation = self.robot.readOrientationSensor().yaw
        self.turn = False
        self.orientation = 0
        self.update = update
    
    def take_control(self):
        if not self.supress:
            return self.turn
    
    def action(self):
        for bh in self.supress_list:
            bh.supress = True
        print("----> control: TurnQR")
        self.supress = False
        self.orientation = self.robot.readOrientationSensor().yaw
        self.robot.moveWheelsByTime(8,8,3)
        self.update.SP = self.orientation
        self.robot.moveWheelsByTime(11, 7, 13)
        self.turn = False
        for bh in self.supress_list:
            bh.supress = False
            
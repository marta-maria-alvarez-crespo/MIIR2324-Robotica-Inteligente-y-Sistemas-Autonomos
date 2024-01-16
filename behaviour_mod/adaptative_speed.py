from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class AdaptativeSpeed():
    def __init__(self, robot):     
        self.robot = robot 
        self.rob_detected = False
        self.max_ir_distance = 50
        self.ir_distance_pre = self.robot.readIRSensor(IR.FrontC)
    
    def adapting_speed(self, speed):
        self.robot.wait(0.1)
        ir_distance_cur = self.robot.readIRSensor(IR.FrontC)
        if ir_distance_cur > self.ir_distance_pre + 20:
            speed = speed - 5
        elif ir_distance_cur < self.ir_distance_pre - 20 or (ir_distance_cur <= 15):
            speed = speed + 1
        else:
            pass

        self.ir_distance_pre = ir_distance_cur
        
        if speed >= 0:
            return speed
        else:
            return 0
    
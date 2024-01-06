from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class AdaptativeSpeed():
    def __init__(self, robot):     
        self.robot = robot 
        self.rob_detected = False
        self.max_ir_distance = 100
        self.ir_distance_pre = self.robot.readIRSensor(IR.FrontC)
    
    def adapting_speed(self, speed):
        self.robot.wait(0.2)
        ir_distance_cur = self.robot.readIRSensor(IR.FrontC)
        if ir_distance_cur > self.ir_distance_pre:
            speed = speed - 1
        elif ir_distance_cur <= self.ir_distance_pre:
            speed = speed + 1
        self.ir_distance_pre = ir_distance_cur
        return speed
    
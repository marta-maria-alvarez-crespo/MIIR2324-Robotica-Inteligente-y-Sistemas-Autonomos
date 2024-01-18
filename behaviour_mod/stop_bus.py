
from behaviour_mod.behaviour import Behaviour
from robobopy.utils.Wheels import Wheels
from behaviour_mod.adaptative_speed import AdaptativeSpeed
from behaviour_mod.my_pid import PID

class StopBus(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.bus_stop = False
        self.min_distance = 10
        self.distance_sb = 2*360
        self.max_speed = 5
        self.speed = 5
        self.adaptative_speed = AdaptativeSpeed(robot)
        self.finished_stop = True
        self.searching = False
        self.name_qr = 'autobus'
        self.pid = PID(robot)
    
    def take_control(self):
        if not self.supress:
            return self.bus_stop
    
    def action(self):
        print("----> control: BusStop")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True
        self.robot.moveWheels(self.speed,self.speed)
        self.robot.moveTiltTo(105,15,False)
        self.robot.movePanTo(90,15, True)
        self.orientation = self.robot.readOrientationSensor().yaw
        self.searching = True
        distance = self.robot.readWheelPosition(Wheels.L) + self.distance_sb
        
        while ((self.robot.readWheelPosition(Wheels.L) < distance) and self.finished_stop):
            self.speed = self.adaptative_speed.adapting_speed(self.speed)
            if self.speed > self.max_speed:
                self.speed = self.max_speed
            self.robot.moveWheels(self.pid.PID(self.orientation, self.speed), self.speed)
            self.robot.wait(0.01)
            
        self.finished_stop = True
        self.searching = False
        self.robot.moveTiltTo(90,5,False)
        self.robot.movePanTo(20,5, True)
        
        for bh in self.supress_list:
            bh.supress = False
        self.bus_stop = False
        
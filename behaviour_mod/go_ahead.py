from behaviour_mod.behaviour import Behaviour
from behaviour_mod.my_pid import PID
from behaviour_mod.adaptative_speed import AdaptativeSpeed

class GoAhead(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.adaptative_speed = AdaptativeSpeed(robot)
        self.speed = 20
        self.qr_speed = 20
        self.robot.moveTiltTo(90,15)
        self.__SP = self.robot.readOrientationSensor().yaw
        self.pid = PID(robot)
        
    def take_control(self):
        ''' take control se vuelve true cuando se suprime el comportamiento'''
        if not self.supress:
            return True
        
    def action(self):
        ''' action() se llama desde behaviour a través de run()'''
        print("----> control: GoAhead")
        # print(self.speed)
        self.supress = False
        if not self.supress:
            self.speed = self.adaptative_speed.adapting_speed(self.speed)
            if self.speed >= self.qr_speed:
                self.speed = self.qr_speed
            print("Soy la velocidad que llevo ",self.speed)
            print("Soy la velocidad del qr ", self.qr_speed)
            self.robot.moveWheels(self.speed, int(self.pid.PID(self.__SP, self.speed)))
            self.robot.wait(0.1)
            
    @property # Así me ahorro poner los paréntesis cuando llame a SP
    def SP(self):
        return self.__SP

    @SP.setter # Fuerzo que __SP solo se pueda variar con esta condicion
    def SP(self, state):
        if self.supress:    
            self.__SP = state - 90
            if self.__SP < -180:
                self.__SP = self.__SP + 360
            # print("esto es el __SP actual ",self.__SP)
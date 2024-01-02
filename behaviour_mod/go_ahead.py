from behaviour_mod.behaviour import Behaviour

class GoAhead(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.speed = 20
        self.robot.moveTiltTo(90,15)
        
        self.__SP = self.robot.readOrientationSensor().yaw
        self.K = 0.5
        
        self.Ts = 0.1
        self.Ti = 2
        
        self.C1 = self.Ts / (2 * self.Ti)
        # self.C2 = (2 * self.Td) / (2 * self.Td / (self.N + self.Ts))
        # self.C3 = (2 * self.Td / (self.N - self.Ts)) / (2 * self.Td / (self.N + self.Ts))
        self.C2 = 0
        self.C3 = 0
        
        self.error = [0, 0]
        self.integral = [0, 0]
        self.derivative = [0, 0]
        
        self.CUR = 0
        self.PRE = 1

    def take_control(self):
        ''' take control se vuelve true cuando se suprime el comportamiento'''
        if not self.supress:
            return True
        
    def action(self):
        ''' action() se llama desde behaviour a través de run()'''
        print("----> control: GoAhead")
        print(self.speed)
        self.supress = False
        if not self.supress:
            self.robot.moveWheels(self.speed, int(self.PID()))
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
            print("esto es el __SP actual ",self.__SP)
        
    def PID(self):
        ''' codigo con un pid discretizado. el error se pone en negativo porque se empieza en 20'''
        current_orientation = self.robot.readOrientationSensor().yaw
        
        if current_orientation/self.__SP > 0:
            self.error[self.CUR] = -(self.__SP - self.robot.readOrientationSensor().yaw)
        else:
            self.error[self.CUR] = -(self.__SP + self.robot.readOrientationSensor().yaw)
            
        self.integral[self.CUR] = self.C1 * (self.error[self.CUR] + self.error[self.PRE]) + self.integral[self.PRE]
        self.derivative[self.CUR] = self.C2 * (self.error[self.CUR] - self.error[self.PRE]) + self.C3 * self.derivative[self.PRE]
        print("esto es el error actual ",self.error[self.CUR])
        print("esto es la integral ",self.integral[self.CUR])
        print("esto es la derivada ",self.derivative[self.CUR])
        self.error[self.PRE] = self.error[self.CUR]
        self.integral[self.PRE] = self.integral[self.CUR]
        self.derivative[self.PRE] = self.derivative[self.CUR]
        
        CV = self.speed - self.K * (self.error[self.CUR] + self.integral[self.CUR] + self.derivative[self.CUR])
        
        if CV < 0:
            return 0
        elif CV > self.speed * 2:
            return self.speed * 2
        
        return CV
    
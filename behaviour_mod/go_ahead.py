from behaviour_mod.behaviour import Behaviour

class GoAhead(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.change_speed = False
        self.speed = 20
        self.min_distance = 20
        self.robot.whenANewQRCodeIsDetected(self.QR_detected)
        
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
        self.derivada = [0, 0]
        
        self.ACT = 0
        self.ANT = 1

    def take_control(self):
        if not self.supress:
            return True
    
    def QR_detected(self):
        qr_id = self.robot.readQR().id
        qr_distance = self.robot.readQR().distance

        try:
            speed = int(qr_id)
            if qr_distance >= self.min_distance and (speed >= 0 or speed <=100):
                self.speed = speed
                self.change_speed = True
            else:
                print("Velocidad fuera de rango")
        except:
            print("El QR no indica velocidad")

        
    def action(self):
        print("----> control: GoAhead")
        self.supress = False
        self.robot.moveWheels(self.speed, int(self.PID()))
        self.robot.wait(0.1)
        
    @property
    def SP(self):
        return self.__SP

    @SP.setter
    def SP(self, state):
        if self.supress:    
            self.__SP = state - 90
        
    def PID(self):
        self.error[self.ACT] = -(self.__SP - self.robot.readOrientationSensor().yaw)
        print(self.error[self.ACT])
        self.integral[self.ACT] = self.C1 * (self.error[self.ACT] + self.error[self.ANT]) + self.integral[self.ANT]
        self.derivada[self.ACT] = self.C2 * (self.error[self.ACT] - self.error[self.ANT]) + self.C3 * self.derivada[self.ANT]
                
        self.error[self.ANT] = self.error[self.ACT]
        self.integral[self.ANT] = self.integral[self.ACT]
        self.derivada[self.ANT] = self.derivada[self.ACT]
        
        CV = 20 - self.K * (self.error[self.ACT] + self.integral[self.ACT] + self.derivada[self.ACT])
        if CV < 0:
            return 0
        elif CV > 40:
            return 40
        
        return CV
from behaviour_mod.behaviour import Behaviour

class GoAhead(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.change_speed = False
        self.speed = 20
        self.min_distance = 20
        
        self.robot.moveTiltTo(90,15)
        self.robot.whenANewQRCodeIsDetected(self.new_QR_detected)
        self.robot.whenAQRCodeIsDetected(self.QR_detected)
        
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
        
    def new_QR_detected(self):
        try:
            qr_id = self.robot.readQR().id
            _, _, qr_speed = qr_id.rpartition(' ')
            speed = int(qr_speed)
            self.change_speed = True
        except:
            pass
           
    def QR_detected(self):
        print('caca')
        '''callback del whenAQRCodeIsDetected()'''
        if self.change_speed:
            qr_id = self.robot.readQR().id
            qr_distance = self.robot.readQR().distance
            self.robot.sayText(qr_distance)
            try:
                _, _, qr_speed = qr_id.rpartition(' ')
                speed = int(qr_speed)
                if qr_distance >= self.min_distance and (speed >= 0 or speed <=100):
                    self.speed = speed
                    self.change_speed = False
                else:
                    print("Velocidad fuera de rango")
            except:
                print("El QR no indica velocidad")
        
    def action(self):
        ''' action() se llama desde behaviour a través de run()'''
        print("----> control: GoAhead")
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
        
    def PID(self):
        ''' codigo con un pid discretizado. el error se pone en negativo porque se empieza en 20'''
        self.error[self.CUR] = -(self.__SP - self.robot.readOrientationSensor().yaw)
        # print(self.error[self.CUR])
        self.integral[self.CUR] = self.C1 * (self.error[self.CUR] + self.error[self.PRE]) + self.integral[self.PRE]
        self.derivative[self.CUR] = self.C2 * (self.error[self.CUR] - self.error[self.PRE]) + self.C3 * self.derivative[self.PRE]
                
        self.error[self.PRE] = self.error[self.CUR]
        self.integral[self.PRE] = self.integral[self.CUR]
        self.derivative[self.PRE] = self.derivative[self.CUR]
        
        CV = self.speed - self.K * (self.error[self.CUR] + self.integral[self.CUR] + self.derivative[self.CUR])
        
        if CV < 0:
            return 0
        elif CV > self.speed * 2:
            return self.speed * 2
        
        return CV
    
class PID():
    def __init__(self, robot):
        self.robot = robot
        self.K = 0.63
        
        self.Ts = 0.1
        self.Ti = 30.8
        
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

    def reset_values(self):
        self.error = [0, 0]
        self.integral = [0, 0]
        self.derivative = [0, 0]

    def PID(self, SP, speed):
        current_orientation = self.robot.readOrientationSensor().yaw
        
        if current_orientation/SP > 0:
            self.error[self.CUR] = -(SP - self.robot.readOrientationSensor().yaw)
        else:
            self.error[self.CUR] = -(SP + self.robot.readOrientationSensor().yaw)
            
        self.integral[self.CUR] = self.C1 * (self.error[self.CUR] + self.error[self.PRE]) + self.integral[self.PRE]
        self.derivative[self.CUR] = self.C2 * (self.error[self.CUR] - self.error[self.PRE]) + self.C3 * self.derivative[self.PRE]
        self.error[self.PRE] = self.error[self.CUR]
        self.integral[self.PRE] = self.integral[self.CUR]
        self.derivative[self.PRE] = self.derivative[self.CUR]
        
        CV = speed - self.K * (self.error[self.CUR] + self.integral[self.CUR] + self.derivative[self.CUR])
        
        if CV < 0:
            return 0
        elif CV > speed * 2:
            return speed * 2
        
        return CV
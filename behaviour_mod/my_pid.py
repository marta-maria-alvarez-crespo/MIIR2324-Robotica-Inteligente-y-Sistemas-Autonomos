# Autora: Marta María Álvarez Crespo
# Última modificación: 20/01/2023
# Descripción: PID discretizado y sintonizado para el robot real

class PID():
    def __init__(self, robot):
        """ Inicialización de variables
        """
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
        """ Método que permite el reseteo del error, integral acumulada y derivada
        """
        self.error = [0, 0]
        self.integral = [0, 0]
        self.derivative = [0, 0]

    def PID(self, SP, speed):
        """ Método que, recibiendo la velocidad que lleva el robot y la orientación (consigna) deseada,
        devuelve una señal de control de la velocidad que permite mantener el rumbo
        """
        current_orientation = self.robot.readOrientationSensor().yaw
        # Se compueba el signo de la relación entre la orientación actual y el SP deseado, para calcular
        # el error correctamente (eje pasa de + a -, y viceversa)
        if current_orientation/SP > 0:
            self.error[self.CUR] = -(SP - self.robot.readOrientationSensor().yaw)
        else:
            self.error[self.CUR] = -(SP + self.robot.readOrientationSensor().yaw)
        # Ecuaciones correspondientes a un regulador PID discretizado
        self.integral[self.CUR] = self.C1 * (self.error[self.CUR] + self.error[self.PRE]) + self.integral[self.PRE]
        self.derivative[self.CUR] = self.C2 * (self.error[self.CUR] - self.error[self.PRE]) + self.C3 * self.derivative[self.PRE]
        self.error[self.PRE] = self.error[self.CUR]
        self.integral[self.PRE] = self.integral[self.CUR]
        self.derivative[self.PRE] = self.derivative[self.CUR]
        # Señal de control de velocidad
        CV = speed - self.K * (self.error[self.CUR] + self.integral[self.CUR] + self.derivative[self.CUR])
        # Para evitar que el robot alcance velocidades negativas, se impone la condición de que la velocidad mínima que
        # se devuelva, sea de 0
        if CV < 0:
            return 0
        # Se impide que la velocidad de la rueda alcance valores excesivos, controlando mejor su comportamiento
        elif CV > speed * 2:
            return speed * 2
        return CV
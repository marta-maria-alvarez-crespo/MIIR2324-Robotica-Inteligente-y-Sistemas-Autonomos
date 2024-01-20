# Autora: Marta María Álvarez Crespo
# Última modificación: 20/01/2023
# Descripción: Comportamiento que permite el avance del robot a la velocidad establecida
# en la vía, manteniendo el rumbo

from behaviour_mod.behaviour import Behaviour
from behaviour_mod.my_pid import PID
from behaviour_mod.adaptative_speed import AdaptativeSpeed

class GoAhead(Behaviour):
    def __init__(self, robot, supress_list, params):
        """ Inicialización de variables
        """
        super().__init__(robot, supress_list, params)
        self.adaptative_speed = AdaptativeSpeed(robot)
        self.speed = 20
        self.qr_speed = 20
        # Se hace el atributo SP privado para forzar que únicamente se actualice
        # con las condiciones impuestas en el setter
        self.__SP = self.robot.readOrientationSensor().yaw
        self.pid = PID(robot)
        
    def take_control(self):
        """ Método que define cuándo el comportamiento toma el control
        En este caso, el método devuelve True en todo caso, mientras no esté 
        suprimido, ya que se trata del comportamiento de prioridad más baja
        """
        if not self.supress:
            return True
    
    def action(self):
        """ Método que define las acciones del comportamiento cuando toma el control
        """
        print("----> control: GoAhead")
        self.supress = False
        # Cuando el comportamiento toma el control, el robot avanza manteniendo el
        # rumbo y evitando chocarse con obstáculos adaptando su velocidad
        if not self.supress:
            self.speed = self.adaptative_speed.adapting_speed(self.speed)
            # Si la velocidad del adaptative_speed supera la velocidad leída en el QR, se
            # mantendrá la velocidad máxima del QR, sin superar su valor
            if self.speed >= self.qr_speed:
                self.speed = self.qr_speed
            # El giroscopio en simulador y en la vida real funcionan justo al revés, por lo
            # que se impone la condición de que, dependiendo de la ip, el PID actuará sobre
            # una rueda u otra
            if self.params["ip"] == "localhost":
                self.robot.moveWheels(self.speed,round(self.pid.PID(self.__SP, self.speed)))
            else:
                self.robot.moveWheels(round(self.pid.PID(self.__SP, self.speed)), self.speed)         
            self.robot.wait(0.1)
    # Se permite el acceso al valor del atributo self.__SP desde fuera de la clase
    @property 
    def SP(self):
        return self.__SP
    # Fuerzo que __SP solo se pueda variar con esta condicion
    @SP.setter 
    def SP(self, state):
        if self.supress:
            # Como el giroscopio funciona al revés, se impone la condición de ip
            if self.params["ip"] == "localhost":
                # Actualización del valor de la orientación 90º en función del valor de la
                # última lectura
                self.__SP = state - 90
                if self.__SP < - 180:
                    self.__SP = self.__SP + 360
            else:
                # Actualización del valor de la orientación 90º en función del valor de la
                # última lectura
                self.__SP = state + 90
                if self.__SP > + 180:
                    self.__SP = self.__SP - 360  
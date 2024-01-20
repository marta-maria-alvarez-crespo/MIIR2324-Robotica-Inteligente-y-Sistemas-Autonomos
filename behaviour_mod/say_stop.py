# Autora: Marta María Álvarez Crespo
# Última modificación: 20/01/2023
# Descripción: Comportamiento que detecta la solicitud de parada y permite a los
# pasajeros bajarse del autobús

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.Wheels import Wheels
from behaviour_mod.my_pid import PID
from behaviour_mod.adaptative_speed import AdaptativeSpeed

class SayStop(Behaviour):
    def __init__(self, robot, supress_list, params):
        """ Inicialización de variables
        """
        super().__init__(robot, supress_list, params)
        self.heard_stop = False
        self.required_stop = False
        self.message = 'para'
        self.distance_st = 2*360
        self.robot.startSpeechDetection()
        self.speed = 5
        self.max_speed = 5
        self.adaptative_speed = AdaptativeSpeed(robot)
        self.pid = PID(robot)
                 
    def take_control(self):
        """ Método que define cuándo el comportamiento toma el control
        En este caso, el método devuelve True cuando el mensaje detectado
        coincide con el definido en el __init__ (actualmente "para")
        """
        if not self.supress:
            if self.robot.readDetectedSpeech().message == self.message:
                self.heard_stop = True
            return self.required_stop
        
    def action(self):
        """ Método que define las acciones del comportamiento cuando toma el control
        """
        print("----> control: SayStop")
        self.supress = False
        # Se suprimen los comportamientos de menor prioridad
        for bh in self.supress_list:
            bh.supress = True
        # Se reduce la velocidad del robot a la definida en el __init__
        self.robot.moveWheels(self.speed, self.speed)
        # Se obtiene el yaw del robot actual para el funcionamiento del PID
        # y se resetea el valor de los encoders
        self.orientation = self.robot.readOrientationSensor().yaw        
        # self.robot.resetWheelEncoders() # No funciona en el robot real, pero sí en simulador
        # Se propone almacenar el valor de la posición de una de las ruedas y
        # sumarle la distancia definida en el __init__ (en número de vueltas*vueltas)
        distance = self.robot.readWheelPosition(Wheels.L) + self.distance_st
        # Mientras la distancia recorrida sea menor a la definida en el __init__
        # el robot avanzará, adaptando su velocidad a posibles obstáculos y utilizando
        # el PID para mantener el rumbo
        while ((self.robot.readWheelPosition(Wheels.L) < distance) and not self.supress):
            self.speed = self.adaptative_speed.adapting_speed(self.speed)
            if self.speed > self.max_speed:
                self.speed = self.max_speed
            self.robot.moveWheels(self.pid.PID(self.orientation, self.speed), self.speed)
            self.robot.wait(0.01)
        # Avanzada la distancia, se detiene al robot durante 5 segundos
        self.robot.stopMotors()
        self.robot.wait(5)
        # Se resetea el valor de las variables y se desuprimen los comportamientos de menor
        # prioridad
        self.heard_stop = False
        self.required_stop = False
        for bh in self.supress_list:
            bh.supress = False
            


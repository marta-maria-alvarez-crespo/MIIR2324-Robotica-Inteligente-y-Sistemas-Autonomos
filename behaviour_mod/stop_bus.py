# Autora: Marta María Álvarez Crespo
# Última modificación: 20/01/2023
# Descripción: Comportamiento que permite la comprobación de la existencia o no
# de pasajeros en una parada designada, así como el desbloqueo del comportamiento
# de búsqueda de color

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.Wheels import Wheels
from behaviour_mod.adaptative_speed import AdaptativeSpeed
from behaviour_mod.my_pid import PID

class StopBus(Behaviour):
    def __init__(self, robot, supress_list, params):
        """ Inicialización de variables
        """
        super().__init__(robot, supress_list, params)
        self.bus_stop = False
        self.min_distance = 10
        self.distance_sb = 1*360
        self.max_speed = 5
        self.speed = 5
        self.adaptative_speed = AdaptativeSpeed(robot)
        self.finished_stop = True
        self.searching = False
        self.name_qr = 'autobus'
        self.pid = PID(robot)
    
    def take_control(self):
        """ Método que define cuándo el comportamiento toma el control
        En este caso, el método devuelve True cuando el QR leído coincide
        con el valor impuesto en read_qr (actualmente: rotonda) y no ha leído
        una parada justo antes
        """
        if not self.supress:
            return self.bus_stop
        
    def action(self):
        """ Método que define las acciones del comportamiento cuando toma el control
        """
        print("----> control: BusStop")
        self.supress = False
        # Se suprimen los comportamientos de menor prioridad
        for bh in self.supress_list:
            bh.supress = True
        # Se establece la velocidad del robot a la velocidad definida en el __init__
        # y se coloca el pan y el tilt en posición de búsqueda de pasajeros
        self.robot.moveWheels(self.speed,self.speed)
        self.robot.moveTiltTo(105,15,False)
        self.robot.movePanTo(90,15, True)
        # Una vez colocado, se vuelve a leer la orientación para que el robot no pierda
        # el rumbo al reposicionar el teléfono y se activa la variable searching de
        # lectura de colores
        self.orientation = self.robot.readOrientationSensor().yaw
        self.searching = True
        # self.robot.resetWheelEncoders() # No funciona en el robot real, pero sí en simulador
        # Se propone almacenar el valor de la posición de una de las ruedas y
        # sumarle la distancia definida en el __init__ (en número de vueltas*vueltas)
        distance = self.robot.readWheelPosition(Wheels.L) + self.distance_sb
        # Mientras la distancia recorrida sea menor a la definida en el __init__
        # el robot avanzará, adaptando su velocidad a posibles obstáculos y utilizando
        # el PID para mantener el rumbo
        while (self.robot.readWheelPosition(Wheels.L) < distance) and self.finished_stop  and not self.supress:
            self.speed = self.adaptative_speed.adapting_speed(self.speed)
            if self.speed > self.max_speed:
                self.speed = self.max_speed
            self.robot.moveWheels(self.pid.PID(self.orientation, self.speed), self.speed)
            self.robot.wait(0.01)
        # Avanzada la distancia, se resetean los atributos, se devuelve el pan y el tilt a su posición
        # original y se desuprimen los comportamientos de menor prioridad
        self.finished_stop = True
        self.searching = False
        self.robot.moveTiltTo(90,5,False)
        self.robot.movePanTo(20,5, True)
        for bh in self.supress_list:
            bh.supress = False
        self.bus_stop = False
        
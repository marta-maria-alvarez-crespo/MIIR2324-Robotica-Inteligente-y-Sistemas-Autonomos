# Autora: Marta María Álvarez Crespo
# Última modificación: 20/01/2023
# Descripción: Comportamiento que controla la carga del robot (base y móvil)

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.Wheels import Wheels
from behaviour_mod.my_pid import PID
from behaviour_mod.adaptative_speed import AdaptativeSpeed

class BatteryLow(Behaviour):
    def __init__(self, robot, supress_list, params):
        """
        Inicialización de variables
        """
        super().__init__(robot, supress_list, params)
        self.low_battery = False
        self.min_battery = 23
        self.max_battery = 25
        self.speed = 5
        self.max_speed = 5
        self.distance_bl = 2*360
        self.battery_stop = False
        self.pid = PID(robot)
        self.adaptative_speed = AdaptativeSpeed(robot)
        self.robot.whenATapIsDetected(self.tap_detected)
    
    def tap_detected(self):
        """
        Callback para la detección de Tap en pantalla
        """
        self.tap = True
        
    def take_control(self): 
        """ Método que define cuándo el comportamiento toma el control
        En este caso, el método devuelve True cuando el nivel de la batería
        coincide con el definido en el __init__ (actualmente entre 20 y 80)
        """
        if not self.supress:
            base_battery = self.robot.readBatteryLevel('base')
            phone_battery = self.robot.readBatteryLevel('phone')
            if ((base_battery < self.min_battery or phone_battery < self.min_battery) 
                and (base_battery != 0 and phone_battery != 0)):
                self.low_battery = True
            self.robot.wait(0.01)
            return self.battery_stop
        
    def action(self):
        """ Método que define las acciones del comportamiento
        """
        print("----> control: BatteryLow")
        self.supress = False
        # Se suprimen los comportamientos de menor prioridad
        for bh in self.supress_list:
            bh.supress = True
        # Se obtiene el yaw del robot actual para el funcionamiento del PID
        # y se resetea el valor de los encoders    
        self.orientation = self.robot.readOrientationSensor().yaw
        # self.robot.resetWheelEncoders() # No funciona en el robot real, pero sí en simulador
        # Se propone almacenar el valor de la posición de una de las ruedas y
        # sumarle la distancia definida en el __init__ (en número de vueltas*vueltas)
        distance = self.robot.readWheelPosition(Wheels.L) + self.distance_bl
        # Mientras la distancia recorrida sea menor a la definida en el __init__
        # el robot avanzará, adaptando su velocidad a posibles obstáculos y utilizando
        # el PID para mantener el rumbo
        while ((self.robot.readWheelPosition(Wheels.L) < distance)):
            self.speed = self.adaptative_speed.adapting_speed(self.speed)
            if self.speed > self.max_speed:
                self.speed = self.max_speed
            self.robot.moveWheels(self.pid.PID(self.orientation, self.speed), self.speed)
            self.robot.wait(0.01)
        # Avanzada la distancia, se detiene al robot completamente y se espera a que se cargue
        # Max_speed se cambia a 0 para evitar la influencia del adaptative_speed
        self.robot.stopMotors()
        self.max_speed = 0
        # Se espera a que el robot cargue y se permite la cancelación del while a través de su
        # supresión mediante la actuación de comportamientos superiores (actualmente: emergency_tap)
        while self.low_battery and not self.supress:
            base_battery = self.robot.readBatteryLevel('base')
            phone_battery = self.robot.readBatteryLevel('phone')
            if (base_battery > self.max_battery and phone_battery > self.max_battery):
                self.low_battery = False
            self.robot.wait(0.01)
        # Una vez cargado, se resetea el valor de las variables y se desuprimen los comportamientos 
        # de menor prioridad
        self.battery_stop = False
        for bh in self.supress_list:
            bh.supress = False
            
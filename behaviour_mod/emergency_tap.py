# Autora: Marta María Álvarez Crespo
# Última modificación: 20/01/2023
# Descripción: Comportamiento que permite la detención de la ejecución del programa

from behaviour_mod.behaviour import Behaviour

class EmergencyTap(Behaviour):
    def __init__(self, robot, supress_list, params):
        """ Inicialización de variables
        """
        super().__init__(robot, supress_list, params)
        self.tap = False
        self.robot.whenATapIsDetected(self.tap_detected)
    
    def tap_detected(self):
        """ Callback que se llama cuando se detecta un toque en la pantalla
        """
        self.tap = True
    
    def take_control(self):
        """ Método que define cuándo el comportamiento toma el control
        En este caso, el método devuelve True cuando un tap es detectado
        """
        if not self.supress:
            return self.tap
        
    def action(self):
        print("----> control: EmergencyTap")
        self.supress = False    
        # Se suprimen los comportamientos de menor prioridad
        for bh in self.supress_list:
            bh.supress = True     
        # Se paran los motores y se coloca el pan y el tilt a su posición inicial
        self.robot.stopMotors()
        self.robot.movePanTo(0,15)
        self.robot.moveTiltTo(75,15)
        # Se pone stop a true para salir del bucle del main y desconectar el robot
        self.set_stop()
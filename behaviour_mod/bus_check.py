
from behaviour_mod.behaviour import Behaviour
from robobopy.utils.Wheels import Wheels

class BusCheck(Behaviour):
    def __init__(self, robot, supress_list, params, stop_bus):
        """ Inicialización de variables
        """
        super().__init__(robot, supress_list, params)
        self.passenger = False
        self.robot.setActiveBlobs(False,False,False,True)
        self.robot.whenANewColorBlobIsDetected(self.blob_detected)
        self.stop_bus = stop_bus
        
    def take_control(self): 
        """ Método que define cuándo el comportamiento toma el control
        En este caso, el método devuelve True cuando se está realizando una
        parada, se detecta un pasajero (custom blob) y el robot dejó de girar
        el pan y el tilt (para evitar que vea colores fuera de la zona designada
        como parada)
        """
        if not self.supress:
            return self.passenger and self.stop_bus.bus_stop and self.stop_bus.searching
    
    def blob_detected(self):
        self.passenger = True
    
    def action(self):
        """ Método que define las acciones del comportamiento cuando toma el control
        """
        print("----> control: BusCheck")
        self.supress = False
        # Se suprimen los comportamientos de menor prioridad
        for bh in self.supress_list:
            bh.supress = True
        self.stop_bus.max_speed = 0
        self.robot.stopMotors()
        while True:
            if self.passenger:
                self.passenger = False
                self.robot.wait(1)
            else:
                self.stop_bus.distance = self.robot.readWheelPosition(Wheels.L)
                self.stop_bus.searching = False
                break
        self.robot.moveTiltTo(90,5,False)
        self.robot.movePanTo(20,5, True)
        self.stop_bus.finished_stop = False
        self.passenger = False    
        self.stop_bus.max_speed = 5
        for bh in self.supress_list:
            bh.supress = False
        
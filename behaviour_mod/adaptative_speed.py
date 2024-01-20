# Autora: Marta María Álvarez Crespo
# Última modificación: 20/01/2023
# Descripción: Adaptación de la velocidad del robot ante obstáculos de frente

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class AdaptativeSpeed():
    def __init__(self, robot):
        """ Inicialización de variables
        """
        self.robot = robot 
        self.rob_detected = False
        self.max_ir_distance = 50
        self.ir_distance_pre = self.robot.readIRSensor(IR.FrontC)
    
    def adapting_speed(self, speed):
        """ Método que permite la adaptación de la velocidad del robot
        en función de los valores leídos por el sensor IR frontal
        """
        self.robot.wait(0.1)
        # Se almacena en una variable el valor actual leído por el sensor
        ir_distance_cur = self.robot.readIRSensor(IR.FrontC)
        # Se compara el valor leído con el valor anterior +- 20 unidades:
        # Si el robot está cada vez más lejos del obstáculo, se incrementa una unidad
        # la velocidad, mientras que, si está más lejos, se disminuye en 5 unidades
        if ir_distance_cur > self.ir_distance_pre + 20:
            speed = speed - 5
        elif ir_distance_cur < self.ir_distance_pre - 20 or (ir_distance_cur <= 15):
            speed = speed + 1
        else:
            pass
        # Se actaliza el valor de la distancia anterior con la lectura almacenada en
        # la variable actual
        self.ir_distance_pre = ir_distance_cur
        # Se impide que el valor se vuelva negativo
        if speed >= 0:
            return speed
        else:
            return 0
    
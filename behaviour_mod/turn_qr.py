# Autora: Marta María Álvarez Crespo
# Última modificación: 20/01/2023
# Descripción: Comportamiento que permite realizar los giros y actualizar el
# valor de la consigna de orientación para mantener el rumbo

from behaviour_mod.behaviour import Behaviour

class TurnQR(Behaviour):
    def __init__(self, robot, supress_list, params, update):
        """ Inicialización de variables
        """
        super().__init__(robot, supress_list, params)
        self.turn = False
        self.update = update
    
    def take_control(self):
        """ Método que define cuándo el comportamiento toma el control
        En este caso, el método devuelve True cuando el QR leído coincide
        con el valor impuesto en read_qr (actualmente: peligrosa izquierda)
        """
        if not self.supress:
            return self.turn
    
    def action(self):
        print("----> control: TurnQR")
        self.supress = False
        # Se suprimen los comportamientos de menor prioridad
        for bh in self.supress_list:
            bh.supress = True
        # Se lee el valor del giroscopio al inicio del comportamiento
        self.orientation = self.robot.readOrientationSensor().yaw
        # El robot reduce su velocidad mientras se aproxima a la curva
        self.robot.moveWheelsByTime(8,8,3)
        # Actualiza el valor del SP para el cambio de dirección
        self.update.SP = self.orientation
        # Realiza el giro pre-programado (valores actuales correspondientes a la maqueta real)
        self.robot.moveWheelsByTime(11, 7, 13)
        # Se resetea el valor de las variables y se desuprimen los comportamientos de menor
        # prioridad
        self.turn = False
        for bh in self.supress_list:
            bh.supress = False
            
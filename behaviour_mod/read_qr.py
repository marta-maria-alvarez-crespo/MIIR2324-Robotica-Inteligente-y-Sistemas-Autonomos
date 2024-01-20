# Autora: Marta María Álvarez Crespo
# Última modificación: 20/01/2023
# Descripción: Programa de lectura de QRs y control de entrada de los diferentes comportamientos

class readQR():
    def __init__(self,robot,behaviour):
        """ Inicialización de variables
        """
        self.robot = robot
        self.behaviour = behaviour
        self.bus_stop = False
        self.turn = False
        self.name_turn_qr = 'peligrosa izquierda' # Valor en robot real
        # self.name_turn_qr = 'peligro izquierda' # Valor en Simulador
        self.name_stop_bus_qr = 'rotonda' # Valor en robot real
        # self.name_stop_bus_qr = 'autobus' # Valor en Simulador
        self.new_stop = False
        self.last_qr = ''
        self.id = ''
        self.num = {"go_ahead": 0, "turn_qr": 1, "stop_bus": 2, "check_bus": 3, "say_stop": 4, "battery_low": 5, "emergency_tap": 6}
        self.robot.whenAQRCodeIsDetected(self.qr_detected)
        self.robot.whenANewQRCodeIsDetected(self.new_qr_detected)
        self.robot.whenAQRCodeIsLost(self.qr_lost)
        
    def qr_detected(self):
        """ Método que define el estado natural del robot de lectura de QRs
        En función del tipo de QR y la distancia a la que lo lee, modificará el valor
        de los diferentes atributos que controlan la entrada de los diferentes comportamientos
        """
        # Se almacena la distancia y el id del qr leído en dos variables 
        qr_distance = self.robot.readQR().distance
        qr_id = self.robot.readQR().id
        # Cumpliendo las siguientes condiciones, se permite la activación del comportamiento de giro
        if qr_distance >= 700 and qr_id == self.name_turn_qr and not self.behaviour[self.num["turn_qr"]].turn:   
            self.behaviour[self.num["turn_qr"]].turn = True 
        # Cumpliendo las siguientes condiciones, se permite la activación de los comportamientos asociados
        # a la parada de autobús. Dependiendo de las condiciones y el estado del robot, se activarán unos u 
        # otros comportamientos. Se evita que el robot lea en bucle la parada mientras ajusta el tilt y el 
        # pan, de forma que solo se ejecute el comportamiento una vez
        if qr_distance >= 400 and qr_id == self.name_stop_bus_qr and not self.behaviour[self.num["stop_bus"]].bus_stop and self.new_stop:
            if self.behaviour[self.num["battery_low"]].low_battery:
                self.behaviour[self.num["battery_low"]].battery_stop = True
            elif self.behaviour[self.num["say_stop"]].heard_stop:
                self.behaviour[self.num["say_stop"]].required_stop = True
            else:
              self.behaviour[self.num["stop_bus"]].bus_stop = True
            self.new_stop = False    
        # Se limpia la lectura de las señales de velocidad para almacenar el valor en una variable de tipo
        # integer, para introducirla directamente como nueva consigna de go_ahead / my_pid / adaptative_speed
        try:
            _, _, qr_speed = qr_id.rpartition(' ')
            speed = int(qr_speed)
            if qr_distance >= 500 and (speed >= 0 or speed <=100):
                # Se resetea el error del pid para evitar sobreoscilaciones y lograr un comportamiento más rápido
                self.behaviour[self.num["go_ahead"]].pid.reset_values()
                # Se actualiza el valor de velocidad máxima que deberá llevar el robot en go_ahead
                self.behaviour[self.num["go_ahead"]].qr_speed = speed
            else:
                # Se evita que el robot lea velocidades fuera de su alcance
                print("Velocidad fuera de rango")
        except:
            pass

    def new_qr_detected(self):
        """ Método que evita que se puedan producir dos paradas de autobús simultáneas, evitando lecturas erróneas
        en los diferentes procesos de aproximación
        """
        self.id = self.robot.readQR().id
        if self.id != self.last_qr:
            self.new_stop = True
            
    def qr_lost(self):
        """ Método que actualiza el valor del atributo self.last_qr utilizado por el método new_qr_detected() para
        determinar si se debe realizar o no una parada en función de la lectura recibida
        """
        self.last_qr = self.id
        
class readQR():
    def __init__(self,robot,behaviour):
        self.robot = robot
        self.behaviour = behaviour
        self.bus_stop = False
        self.turn = False
        self.name_turn_qr = 'peligrosa izquierda'
        self.name_turn_qr_r = 'peligro derecha'
        self.name_stop_bus_qr = 'rotonda'
        self.new_stop = False
        self.last_qr = ''
        self.id = ''
        self.num = {"go_ahead": 0, "turn_qr": 1, "stop_bus": 2, "check_bus": 3, "say_stop": 4, "battery_low": 5, "emergency_tap": 6}
        self.robot.whenAQRCodeIsDetected(self.qr_detected)
        self.robot.whenANewQRCodeIsDetected(self.new_qr_detected)
        self.robot.whenAQRCodeIsLost(self.qr_lost)
        
    def qr_detected(self):
        qr_distance = self.robot.readQR().distance
        qr_id = self.robot.readQR().id
        
        # Este permite la activación del giro
        if qr_distance >= 700 and qr_id == self.name_turn_qr and not self.behaviour[self.num["turn_qr"]].turn:   
            self.behaviour[self.num["turn_qr"]].turn = True 
            
        # Este permite la activación de los comportamientos de parada
        if qr_distance >= 400 and qr_id == self.name_stop_bus_qr and not self.behaviour[self.num["stop_bus"]].bus_stop and self.new_stop:
            if self.behaviour[self.num["battery_low"]].low_battery:
                self.behaviour[self.num["battery_low"]].battery_stop = True
            elif self.behaviour[self.num["say_stop"]].heard_stop:
                self.behaviour[self.num["say_stop"]].required_stop = True
            else:
              self.behaviour[self.num["stop_bus"]].bus_stop = True
            
            self.new_stop = False
            
        # Este permite la activación del comportamiento de avance y velocidad
        try:
            _, _, qr_speed = qr_id.rpartition(' ')
            speed = int(qr_speed)
            if qr_distance >= 500 and (speed >= 0 or speed <=100):
                self.behaviour[self.num["go_ahead"]].pid.reset_values()
                self.behaviour[self.num["go_ahead"]].qr_speed = speed
            else:
                print("Velocidad fuera de rango")
        except:
            pass

    def new_qr_detected(self):
        self.id = self.robot.readQR().id
        if self.id != self.last_qr:
            self.new_stop = True
            
    def qr_lost(self):
        self.last_qr = self.id
        
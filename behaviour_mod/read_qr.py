
class readQR():
    def __init__(self,robot,behaviour):
        self.robot = robot
        self.behaviour = behaviour
        self.bus_stop = False
        self.turn = False
        self.name_turn_qr = 'peligro izquierda'
        self.name_stop_bus_qr = 'autobus'
        self.new_stop = False
        self.robot.whenAQRCodeIsDetected(self.qr_detected)
        self.robot.whenANewQRCodeIsDetected(self.new_qr_detected)
        
    def qr_detected(self):
        qr_distance = self.robot.readQR().distance
        qr_id = self.robot.readQR().id
        
        # Este permite la activación del giro
        if qr_distance >= 15 and qr_id == self.name_turn_qr and not self.behaviour[1].turn:
            self.orientation = self.robot.readOrientationSensor().yaw   
            self.behaviour[1].turn = True 
        
        # Este permite la activación de los comportamientos de parada
        if qr_distance >= 10 and qr_id == self.name_stop_bus_qr and not self.behaviour[2].bus_stop and self.new_stop:
            if not self.behaviour[5].low_battery and not self.behaviour[4].heard_stop:
              self.behaviour[2].bus_stop = True
            elif self.behaviour[5].low_battery:
                self.behaviour[5].battery_stop = True
            elif self.behaviour[4].heard_stop:
                self.behaviour[4].required.stop = True
            self.new_stop = False
            
        # Este permite la activación del comportamiento de avance y velocidad
        try:
            _, _, qr_speed = qr_id.rpartition(' ')
            speed = int(qr_speed)
            if qr_distance >= 15 and (speed >= 0 or speed <=100):
                self.behaviour[0].error = [0, 0]
                self.behaviour[0].integral = [0, 0]
                self.behaviour[0].derivative = [0, 0]
                self.behaviour[0].speed = speed
            else:
                print("Velocidad fuera de rango")
        except:
            print("El QR no indica velocidad")

        
    def new_qr_detected(self):
        id = self.robot.readQR().id
        if id == self.name_stop_bus_qr:
            self.new_stop = True
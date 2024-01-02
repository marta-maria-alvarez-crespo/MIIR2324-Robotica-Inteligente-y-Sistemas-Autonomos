
class readQR():
    def __init__(self,robot,behaviour):
        self.robot = robot
        self.behaviour = behaviour
        self.bus_stop = False
        self.turn = False
        self.name_turn_qr = 'peligro izquierda'
        self.name_stop_bus_qr = 'autobus'
        self.robot.whenAQRCodeIsDetected(self.QR_detected)
        
    def QR_detected(self):
        qr_distance = self.robot.readQR().distance
        qr_id = self.robot.readQR().id
        
        # Este permite la activación del giro
        if qr_distance >= 15 and qr_id == self.name_turn_qr and not self.behaviour[1].turn:
            self.orientation = self.robot.readOrientationSensor().yaw   
            self.behaviour[1].turn = True 
        
        # Este permite la activación de los comportamientos de parada
        if qr_distance >= 10 and qr_id == self.name_stop_bus_qr and not self.behaviour[2].bus_stop:
            self.behaviour[2].bus_stop = True
            
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

        
        

class readQR():
    def __init__(self,robot,behaviour):
        self.robot = robot
        self.behaviour = behaviour
        self.bus_stop = False
        self.turn = False
        self.name_turn_qr = 'peligro izquierda'
        self.name_stop_bus_qr = 'autobus'
        self.new_stop = False
        self.last_qr = ''
        self.id = ''
        self.num_go_ahead = 0
        # self.num_ajuste_de_velocidad = 1
        self.num_turn_qr = 2
        self.num_stop_bus = 3
        self.num_check_bus = 4
        self.num_say_stop = 5
        self.num_battery_low = 6
        self.num_emergency_tap = 7
        self.robot.whenAQRCodeIsDetected(self.qr_detected)
        self.robot.whenANewQRCodeIsDetected(self.new_qr_detected)
        self.robot.whenAQRCodeIsLost(self.qr_lost)
        
    def qr_detected(self):
        qr_distance = self.robot.readQR().distance
        qr_id = self.robot.readQR().id

        # Este permite la activación del giro
        if qr_distance >= 15 and qr_id == self.name_turn_qr and not self.behaviour[self.num_turn_qr].turn:
            self.orientation = self.robot.readOrientationSensor().yaw   
            self.behaviour[self.num_turn_qr].turn = True 
        
        # Este permite la activación de los comportamientos de parada
        if qr_distance >= 10 and qr_id == self.name_stop_bus_qr and not self.behaviour[self.num_stop_bus].bus_stop and self.new_stop:
            if not self.behaviour[self.num_battery_low].low_battery and not self.behaviour[self.num_say_stop].heard_stop:
              self.behaviour[self.num_stop_bus].bus_stop = True
            elif self.behaviour[self.num_battery_low].low_battery:
                self.behaviour[self.num_battery_low].battery_stop = True
            elif self.behaviour[self.num_say_stop].heard_stop:
                self.behaviour[self.num_say_stop].required_stop = True
            self.new_stop = False
            
        # Este permite la activación del comportamiento de avance y velocidad
        try:
            _, _, qr_speed = qr_id.rpartition(' ')
            speed = int(qr_speed)
            if qr_distance >= 15 and (speed >= 0 or speed <=100):
                self.behaviour[self.num_go_ahead].error = [0, 0]
                self.behaviour[self.num_go_ahead].integral = [0, 0]
                self.behaviour[self.num_go_ahead].derivative = [0, 0]
                self.behaviour[self.num_go_ahead].speed = speed
            else:
                print("Velocidad fuera de rango")
        except:
            print("El QR no indica velocidad")

    def new_qr_detected(self):
        self.id = self.robot.readQR().id
        if self.id != self.last_qr:
            self.new_stop = True
            
    def qr_lost(self):
        self.last_qr = self.id
        print(self.last_qr)
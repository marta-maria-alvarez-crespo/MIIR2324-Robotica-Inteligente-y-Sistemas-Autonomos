
from behaviour_mod.behaviour import Behaviour
from robobopy.utils.Wheels import Wheels

class BatteryLow(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.low_battery = False
        self.min_battery = 20
        self.max_battery = 89
        self.speed = 5
        self.max_speed = 5
        self.distance = 4*360
        self.battery_stop = False
        
    def take_control(self): 
        if not self.supress:
            base_battery = self.robot.readBatteryLevel('base')
            phone_battery = self.robot.readBatteryLevel('phone')
            if ((base_battery < self.min_battery or phone_battery < self.min_battery) 
                and (base_battery != 0 and phone_battery != 0)):
                self.low_battery = True
            self.robot.wait(0.01)
            return self.battery_stop
        
    def action(self):
            print("----> control: BatteryLow")
            self.supress = False
            for bh in self.supress_list:
                bh.supress = True
                
            self.robot.resetWheelEncoders()
            while (self.robot.readWheelPosition(Wheels.L) < self.distance):
                self.speed = self.adaptative_speed.adapting_speed(self.speed)
                if self.speed > self.max_speed:
                    self.speed = self.max_speed
                self.robot.moveWheels(self.speed, self.speed)
            # No se si es necesario:
            self.stop_bus.max_speed = 0 
            self.robot.stopMotors()
            
            while self.low_battery:
                base_battery = self.robot.readBatteryLevel('base')
                phone_battery = self.robot.readBatteryLevel('phone')
                if (base_battery > self.max_battery and phone_battery > self.max_battery):
                    self.low_battery = False
                self.robot.wait(0.01)
            self.battery_stop = False
            for bh in self.supress_list:
                bh.supress = False
            
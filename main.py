from robobopy.Robobo import Robobo
from behaviour_mod.go_ahead import GoAhead
from behaviour_mod.turn_qr import TurnQR
from behaviour_mod.stop_bus import StopBus
from behaviour_mod.bus_check import BusCheck
from behaviour_mod.read_qr import readQR
from behaviour_mod.emergency_tap import EmergencyTap
from behaviour_mod.battery_low import BatteryLow
from behaviour_mod.say_stop import SayStop
from behaviour_mod.adaptative_speed import AdaptativeSpeed
import time

robobo = Robobo("192.168.1.113")
robobo.connect()
#robobo.moveWheelsByTime(-50,-50,2)

# Diccionario que se pasará a los comportamientos
# para que lo activen cuando se finalice la misión
params = {"stop": False}

go_ahead = GoAhead(robobo, [], params)  #0
adaptative_speed = None # 1
turn_qr = TurnQR(robobo, [go_ahead, adaptative_speed], params) #2
stop_bus = StopBus(robobo, [go_ahead, turn_qr], params) #3
check_bus = BusCheck(robobo, [go_ahead, turn_qr, stop_bus], params, stop_bus) # 4
say_stop = SayStop(robobo, [go_ahead, turn_qr, stop_bus, check_bus], params) # 5
battery_low = BatteryLow(robobo, [go_ahead, turn_qr, stop_bus, check_bus, say_stop], params) # 6
emergency_tap = EmergencyTap(robobo, [go_ahead, turn_qr, stop_bus, check_bus, say_stop, battery_low], params) # 7

# Se crea una Lista con los comportamientos (2 en este ejemplo)
threads = [go_ahead, adaptative_speed, turn_qr, stop_bus, check_bus, say_stop, battery_low, emergency_tap]
read_qr = readQR(robobo,threads)

# Se inician todos los comportamientos

go_ahead.start()
turn_qr.start()
stop_bus.start()
check_bus.start()
say_stop.start()
battery_low.start()
emergency_tap.start()

# Se mantiene el hilo principal en espera
# hasta que algún comportamiento marca
# el objetivo como terminado

while not params["stop"]:
    if turn_qr.turn:
        go_ahead.SP = read_qr.orientation
    time.sleep(0.1)

# Espera a que terminen todos los hilos
for thread in threads:
    thread.join()

robobo.stopMotors()
robobo.disconnect()

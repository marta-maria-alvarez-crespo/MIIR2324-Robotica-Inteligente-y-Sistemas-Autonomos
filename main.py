from robobopy.Robobo import Robobo
from behaviour_mod.go_ahead import GoAhead
from behaviour_mod.turn_qr import TurnQR
from behaviour_mod.stop_bus import StopBus
from behaviour_mod.bus_check import BusCheck
from behaviour_mod.read_qr import readQR
import time

robobo = Robobo("localhost")
robobo.connect()

# robobo.moveWheelsByTime(-20,-20,7)

# Diccionario que se pasará a los comportamientos
# para que lo activen cuando se finalice la misión
params = {"stop": False}

go_ahead = GoAhead(robobo, [], params)
turn_qr = TurnQR(robobo, [go_ahead], params)
stop_bus = StopBus(robobo, [go_ahead, turn_qr], params)
check_bus = BusCheck(robobo, [go_ahead, turn_qr, stop_bus], params)

# Se crea una Lista con los comportamientos (2 en este ejemplo)
threads = [go_ahead, turn_qr, stop_bus, check_bus]
read_qr = readQR(robobo,threads)

# Se inician todos los comportamientos
go_ahead.start()
turn_qr.start()
stop_bus.start()
check_bus.start()

# Se mantiene el hilo principal en espera
# hasta que algún comportamiento marca
# el objetivo como terminado
while not params["stop"]:
    check_bus.allow_bus_stop = stop_bus.bus_stop
    if turn_qr.turn:
        go_ahead.SP = read_qr.orientation
    time.sleep(0.1)

# Espera a que terminen todos los hilos
for thread in threads:
    thread.join()

robobo.disconnect()

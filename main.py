from robobopy.Robobo import Robobo
from behaviour_mod.go_ahead import GoAhead
from behaviour_mod.turn_qr import TurnQR

import time

robobo = Robobo("localhost")
robobo.connect()

# Diccionario que se pasará a los comportamientos
# para que lo activen cuando se finalice la misión
params = {"stop": False}

go_ahead = GoAhead(robobo, [], params)
turn_qr = TurnQR(robobo, [go_ahead], params)

# Se crea una Lista con los comportamientos (2 en este ejemplo)
threads = [go_ahead, turn_qr]

# Se inician todos los comportamientos
go_ahead.start()
turn_qr.start()

# Se mantiene el hilo principal en espera
# hasta que algún comportamiento marca
# el objetivo co terminado
while not params["stop"]:
    go_ahead.SP = turn_qr.decirOrientacion()
    time.sleep(0.1)

# Espera a que terminen todos los hilos
for thread in threads:
    thread.join()

robobo.disconnect()
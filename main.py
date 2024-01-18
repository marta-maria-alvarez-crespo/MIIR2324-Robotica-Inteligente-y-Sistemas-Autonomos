# Autora: Marta María Álvarez Crespo
# Última modificación: 18/01/2023
# Descripción: Creación de los hilos para la ejecución de los diferentes comportamientos

from robobopy.Robobo import Robobo

from behaviour_mod.go_ahead import GoAhead
from behaviour_mod.turn_qr import TurnQR
from behaviour_mod.stop_bus import StopBus
from behaviour_mod.bus_check import BusCheck
from behaviour_mod.read_qr import readQR
from behaviour_mod.emergency_tap import EmergencyTap
from behaviour_mod.battery_low import BatteryLow
from behaviour_mod.say_stop import SayStop

import time

def main():
    """ 
    Definición de la ip, generación de los diferentes hilos a ejecutar con cada comportamiento
    y comportamientos a suprimir por cada uno en orden ascendente en la arquitectura
    """
    ip = "10.113.36.129"
    robobo = Robobo(ip)
    robobo.connect()
    # Colocación del robot en la posición óptima de lectura
    robobo.moveTiltTo(90,15)
    robobo.movePanTo(20,15)
    # Se detiene la ejecución para garantizar que se lee un valor correcto del giroscopio
    time.sleep(1)
    # Diccionario que se pasará a los comportamientos para que lo activen cuando se finalice la misión
    params = {"stop": False, "ip": ip}
    # Instancias de cada comportamiento generado, por orden de prioridad (ascendente)
    go_ahead = GoAhead(robobo, [], params)  #0
    turn_qr = TurnQR(robobo, [go_ahead], params, go_ahead) #2
    stop_bus = StopBus(robobo, [go_ahead, turn_qr], params) #3
    check_bus = BusCheck(robobo, [go_ahead, turn_qr, stop_bus], params, stop_bus) # 4
    say_stop = SayStop(robobo, [go_ahead, turn_qr, stop_bus, check_bus], params) # 5
    battery_low = BatteryLow(robobo, [go_ahead, turn_qr, stop_bus, check_bus, say_stop], params) # 6
    emergency_tap = EmergencyTap(robobo, [go_ahead, turn_qr, stop_bus, check_bus, say_stop, battery_low], params) # 7
    # Se crea una Lista con los comportamientos y se inicia la lectura natural de QRs
    threads = [go_ahead, turn_qr, stop_bus, check_bus, say_stop, battery_low, emergency_tap]
    read_qr = readQR(robobo,threads)
    # Se inician todos los comportamientos
    go_ahead.start()
    turn_qr.start()
    stop_bus.start()
    check_bus.start()
    say_stop.start()
    battery_low.start()
    emergency_tap.start()
    # Se mantiene el hilo principal en espera hasta que algún comportamiento marca el objetivo como terminado
    # Se actualiza el valor del SP con la última lectura leída por el sensor de orientación para el PID
    while not params["stop"]:
        time.sleep(0.1)
    # Espera a que terminen todos los hilos
    for thread in threads:
        thread.join()
    # Con estas sentencias se asegura que adaptative_speed no interfiere en el proceso de parada de emergencia
    go_ahead.qr_speed = 0
    stop_bus.max_speed = 0
    battery_low.max_speed = 0
    say_stop.max_speed = 0
    # Se paran los motores y se desconecta el robot
    robobo.stopMotors()
    robobo.disconnect()

if __name__ == "__main__":
    main()
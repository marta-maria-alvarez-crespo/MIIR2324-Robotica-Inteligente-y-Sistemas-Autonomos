from robobopy.Robobo import Robobo
from robobopy.utils.IR import IR
rob = Robobo('localhost')
rob.connect()

while True:
    base = rob.readBatteryLevel('base')
    print(base)
    rob.readIRSensor(IR.FrontC)
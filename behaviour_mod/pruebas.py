from robobopy.Robobo import Robobo

rob = Robobo('localhost')
rob.connect()

while True:
    base = rob.readBatteryLevel('base')
    print(base)
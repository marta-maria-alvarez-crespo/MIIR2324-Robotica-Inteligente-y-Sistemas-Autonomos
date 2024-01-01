from robobopy.Robobo import Robobo

rob = Robobo('localhost')
rob.connect()

rob.moveWheelsByTime(-20,-20,7)
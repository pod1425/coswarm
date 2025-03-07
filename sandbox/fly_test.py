from codrone_edu.drone import *

drone1 = Drone()
drone2 = Drone()
drone1.pair()
#drone2.pair(portname='COM3')

drone1.takeoff()
#drone2.takeoff()
drone1.hover(3)
#drone2.hover(3)
drone1.land()
#drone2.land()

drone1.close()
#drone2.close()
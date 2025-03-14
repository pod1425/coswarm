from codrone_edu.drone import *

drone = Drone()
drone.pair()

drone.takeoff()
drone.move_forward(20)
drone.set_throttle(80)
drone.move(1)

drone.set_throttle(-40)
drone.move(1)
sleep(2)
drone.land()



drone.close()
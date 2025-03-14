from time import sleep
from xmlrpc.client import boolean

from codrone_edu.drone import Drone

def approx_equals(ideal: float, actual: float, error: float):
    return ideal - error < actual < ideal + error


drone = Drone()
drone.pair()
drone.takeoff()
height = 1.3
speed = 50
tolerance = 0.1

drone_height = drone.get_height('m')
while not approx_equals(height, drone_height, tolerance):
    drone_height = drone.get_height('m')
    if drone_height >= 9.98:
        continue
    print(drone_height)
    if drone_height > height:
        drone.set_throttle(-speed)
        drone.move(0.2)
    elif drone_height < height:
        drone.set_throttle(speed)
        drone.move(0.2)

    sleep(0.1)
print('reached target height!')
drone.hover(1)
drone.land()
drone.close()
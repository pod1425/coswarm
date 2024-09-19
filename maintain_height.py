from xmlrpc.client import boolean

from codrone_edu.drone import Drone

def approx_equals(ideal: float, actual: float, error: float):
    return ideal - error < actual < ideal + error


drone = Drone()
drone.pair()
drone.takeoff()
height = 1.3

drone_height = drone.get_height('m')
while not approx_equals(height, drone_height, 0.04):
    drone_height = drone.get_height('m')
    if drone_height >= 9.98:
        continue
    print(drone_height)
    if drone_height > height:
        drone.set_throttle(-20)
        drone.move(0.2)
        print('going down...')
    elif drone_height < height:
        drone.set_throttle(20)
        drone.move(0.2)
        print('going up...')

    drone.hover(0.1)
print('reached target height!')
drone.hover(1)
drone.land()
drone.close()
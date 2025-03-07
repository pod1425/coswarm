import time

#Python code
from codrone_edu.drone import *

drone = Drone()
drone.pair()


drone.takeoff()
drone.hover(3)
distance = 1
prev_distance = 1
while distance > 0.1:
  prev_distance = distance
  distance = drone.get_bottom_range()

  if distance <= 15:
    drone.emergency_stop()
  if prev_distance != distance:
    print(distance)

  drone.hover(0.5)


drone.land()


drone.close()
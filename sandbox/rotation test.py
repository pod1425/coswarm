from codrone_edu.drone import Drone

drone = Drone()
drone.pair()

drone.takeoff()

for i in range(4):
    drone.turn_left(90)
    drone.hover()

drone.land()

drone.close()
from codrone_edu.drone import Drone

drone = Drone()
drone.pair()

drone.takeoff()
drone.hover(1)
dist = drone.get_front_range()
print(dist)
while dist >= 999:
    drone.set_pitch(30)
    drone.move(0.1)
    drone.hover(0.5)
    dist = drone.get_front_range()
    print(dist)


drone.land()

drone.close()
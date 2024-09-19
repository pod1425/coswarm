from codrone_edu.drone import *

drone = Drone()
drone.pair()


drone.takeoff()
drone.hover(1)
for i in range(4):
    angle = 90 * (i + 1)
    drone.set_pitch(50)
    drone.move(0.5)
    drone.reset_move()
    drone.turn_degree(angle)

    print("turning " + str(angle) + " degree")
drone.land()
drone.close()

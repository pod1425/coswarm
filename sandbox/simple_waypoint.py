from codrone_edu.drone import Drone

drone = Drone()
drone.pair()
drone.takeoff()
drone.hover(1)
drone.goto_waypoint([1, 1, 1], 0.5)

drone.hover(2)
print(drone.get_position_data())
drone.land()


drone.close()
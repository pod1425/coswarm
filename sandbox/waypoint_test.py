import time

from codrone_edu.drone import Drone

drone = Drone()
drone.pair()
drone.takeoff()
drone.hover(1)
drone.set_waypoint()
drone.set_pitch(40)
drone.move(1)
drone.hover(1)
drone.set_waypoint()
waypoints = drone.waypoint_data
print(waypoints)
drone.land()

time.sleep(1)

drone.takeoff()
print(drone.get_position_data())
drone.goto_waypoint(waypoints[0], 0.5)
print('after first waypoint', drone.get_position_data())
new_waypoint = waypoints[0]
#[0] + forward, - backward
#[1] + to left, - to right
#[2]
new_waypoint[2] -= 0.4
print('new', new_waypoint)

drone.hover(1)
drone.goto_waypoint(new_waypoint, 0.5)
print('after second waypoint', drone.get_position_data())
drone.hover(2)
drone.land()

drone.close()
from time import sleep

from swarm import drone_control_2d
from swarm.drone_control_2d import DroneControl

swarm = DroneControl()

if swarm.auto_connect() != 0:
    print("Exiting...")
    exit(0)

swarm.all_takeoff()
swarm.await_standby()
swarm.all_move_left(30)
swarm.await_standby()
sleep(0.5)

swarm.all_move_right(30)
sleep(0.5)
swarm.await_standby()

swarm.all_change_throttle(60, 1)
swarm.await_standby()
sleep(1)
swarm.all_change_throttle(-60, 1.5, drones=["1", "3", "5"])
swarm.all_change_throttle(60, 1.5, drones=["2", "4"])
swarm.await_standby()
sleep(0.5)
swarm.all_change_throttle(60, 1.5, drones=["1", "3", "5"])
swarm.all_change_throttle(-60, 1.5, drones=["2", "4"])
swarm.await_standby()
sleep(1)
swarm.all_change_throttle(-60, 1)
#swarm.all_goto_height(0.9, 50)
swarm.await_standby()

swarm.all_move_forward(100, drones=["3"])
swarm.all_move_forward(50, drones=["2", "4"])
swarm.await_standby()

sleep(1)
swarm.all_move_forward(150)
swarm.all_hover(3)
sleep(1)
swarm.all_land()
swarm.await_standby()
swarm.close_all()
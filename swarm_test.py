from time import sleep

from swarm import drone_control_2d
from swarm.drone_control_2d import DroneControl

control = DroneControl()

if control.auto_connect() != 0:
    print("Exiting...")
    exit(0)

control.all_takeoff()
control.all_hover(2, ["1", "3"])
control.all_land(["2"])
sleep(1.0)
control.all_land()
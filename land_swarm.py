from time import sleep

from swarm import drone_control_2d
from swarm.drone_control_2d import DroneControl

control = DroneControl()

if control.auto_connect() != 0:
    print("Exiting...")
    exit(0)

control.all_land()
control.close_all()
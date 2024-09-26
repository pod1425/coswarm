import keyboard
from codrone_edu.drone import Drone


def manual_fly(drone: Drone):
    power = 30
    duration = 0.1



    if keyboard.is_pressed('w'):
        drone.set_pitch(power)
        drone.move(duration)
    if keyboard.is_pressed('s'):
        drone.set_pitch(-power)
        drone.move(duration)
    if keyboard.is_pressed('a'):
        drone.set_roll(-power)
        drone.move(duration)
    if keyboard.is_pressed('d'):
        drone.set_roll(power)
        drone.move(duration)
    if keyboard.is_pressed('e'):
        drone.set_yaw(-power)
        drone.move(duration)
    if keyboard.is_pressed('q'):
        drone.set_yaw(power)
        drone.move(duration)
    if keyboard.is_pressed('f'):
        drone.set_throttle(-power)
        drone.move(duration)
    if keyboard.is_pressed('r'):
        drone.set_throttle(power)
        drone.move(duration)
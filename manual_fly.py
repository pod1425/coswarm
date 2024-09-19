from codrone_edu.drone import *
import keyboard
import time

#TODO: usage of sendControl() to send controls to drone
#TODO: on release key stopping
def main():

    print("Hello, World!")
    drone = Drone()
    drone.pair()
    drone.takeoff()


    power = 40
    duration = 0.1
    curr_time = int(time.time())
    last_time = curr_time
    while not keyboard.is_pressed('esc'):
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

        curr_time = int(time.time())
        if curr_time != last_time:
            data = drone.get_position_data()
            print(data)
            last_time = curr_time
        drone.hover(0)

    print("Loop stopped because a key was pressed.")

    drone.land()
    drone.close()


if __name__ == "__main__":
    main()
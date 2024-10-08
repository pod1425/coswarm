import queue

import keyboard
from serial.tools import list_ports
from codrone_edu.drone import *
from time import sleep


class DroneControl:

    def __init__(self):
        self.drones = []
        self.num_drones = 0

    def worker(self, drone: Drone, task_queue: Queue):
        while True:
            func, args = task_queue.get()  # Get a function from the queue
            if func is None:  # Stop if None is received
                break
            func(*args)  # Execute the function
            task_queue.task_done()

    def auto_connect(self):
        drone_objects = []
        x = list(list_ports.comports(include_links=True))
        portnames = []

        # Append all of the correct drone portnames in the portnames list
        for element in x:
            if element.vid == 1155:
                portname = element.device
                print("Detected: ", portname)
                portnames.append(str(portname))
        print("")

        self.num_drones = len(portnames)

        for i in range(self.num_drones):
            drone_objects.append(Drone())

        for i in range(self.num_drones):
            drone_objects[i].pair(portnames[i])
            print("Paired drone at port ", portnames[i])
            print("")

        for drone in drone_objects:
            drone_queue = Queue()  # Task queue specific to this drone
            drone_thread = threading.Thread(target=self.worker, args=(drone, drone_queue))
            drone_thread.daemon = True  # Make the thread a daemon so it exits with the program

            self.drones.append((drone, drone_thread, drone_queue))

        for _, thread, _ in self.drones:
            thread.start()



    def close_all(self):
        for drone, _, drone_queue in self.drones:
            drone_queue.put(None)
        for drone, _, _ in self.drones:
            drone.close()


    def all_takeoff(self):
        for drone, _, q in self.drones:
            q.put(drone.takeoff, ())
        sleep(4)


    def all_land(self):
        for drone, _, q in self.drones:
            q.put(drone.land, ())
        sleep(4)


    def all_move(self, r, p, y, t, seconds):

        timeout = seconds
        init_time = time.time()

        while time.time() - init_time < timeout:
            for drone, _, q in self.drones:
                q.put(drone.sendControl, (r, p, y, t))
                sleep(0.05)


    def all_hover(self, seconds):

        timeout = seconds
        init_time = time.time()

        while time.time() - init_time < timeout:
            for drone, _, q in self.drones:
                q.put(drone.sendControl, (0, 0, 0, 0))
                sleep(0.05)


    def all_turn_degree(self, degree):
        for drone, _, q in self.drones:
            if degree > 0:
                q.put(drone.turn_right, (degree))
            elif degree < 0:
                q.put(drone.turn_left, (degree))


    def manual_fly(self, drone: Drone):
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
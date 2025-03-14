import queue
import string
from operator import itemgetter

import keyboard
from serial.tools import list_ports
from codrone_edu.drone import *
from time import sleep

from swarm.graphing import get_graph_points, approx_equals


class DroneControl:

    def __init__(self):
        self.drones = []
        self.num_drones = 0
        self.global_height = 1

    def worker(self, drone: Drone, task_queue: Queue):
        while True:
            task = task_queue.get()  # Get a function from the queue
            if task is None:
                break
            func, args = task
            func(*args)  # Execute the function
            task_queue.task_done()

    def auto_connect(self):
        drone_objects = []
        x = list(list_ports.comports(include_links=True))
        portnames = []

        # Append all of the correct drone portnames in the portnames list
        for element in x:
            print("scanning port " + element.name)
            if element.vid == 1155:
                portname = element.device
                print("Detected: ", portname)
                portnames.append(str(portname))
        print("")
        if (len(portnames) == 0):
            print("No drones found!")
            return -1
        self.num_drones = len(portnames)

        for i in range(self.num_drones):
            drone_objects.append(Drone())

        for i in range(self.num_drones):
            drone_objects[i].pair(portnames[i])
            drone_queue = Queue()  # Task queue specific to this drone
            drone_thread = threading.Thread(target=self.worker, args=(drone_objects[i], drone_queue))
            drone_thread.daemon = True  # Make the thread a daemon so it exits with the program

            self.drones.append((drone_objects[i], drone_thread, drone_queue, portnames[i]))
            print("Paired drone at port ", portnames[i])
            print("")

        self.drones = sorted(self.drones, key=itemgetter(3))
        i = 1
        for index, (drone, thread, q, portname) in enumerate(self.drones):
            thread.start()
            # Create a new tuple with the modified portname
            self.drones[index] = (drone, thread, q, str(i))
            i += 1
        return 0

    def get_drones(self, drones: list[string]=None) -> list[Drone]:
        affected_drones = self._getAffectedDrones(drones)
        drone_array = []
        for drone, _, _, num in affected_drones:
            drone_array.append(drone)
            print("adding drone num " + num)
        return drone_array

    def _getAffectedDrones(self, drones: list[string]=None) -> list[(Drone, Thread, Queue, string)]:
        if drones is None:
            return self.drones
        affected = []
        for t in self.drones:
            if t[3] in drones:
                affected.append(t)
        return affected

    def close_all(self):
        for drone, _, drone_queue, _ in self.drones:
            drone_queue.put(None)
        for drone, thread, _, _ in self.drones:
            drone.close()
            thread.join()


    def all_takeoff(self, drones: list[string]=None):
        affected_drones = self._getAffectedDrones(drones)
        for drone, _, q, _ in affected_drones:
            q.put((drone.takeoff, ()))
        sleep(4)


    def all_land(self, drones: list[string]=None):
        affected_drones = self._getAffectedDrones(drones)
        for drone, _, q, _ in affected_drones:
            q.put((drone.land, ()))
        sleep(4)


    def all_move(self, roll, pitch, yaw, throttle, seconds, drones: list[string]=None):
        '''

        :param roll:  left/right
        :param pitch: forward/backward
        :param yaw: rotation
        :param throttle: up/down
        :param seconds: time
        :param drones: affected drones
        :return:
        '''

        affected_drones = self._getAffectedDrones(drones)
        timeout = seconds
        init_time = time.time()

        while time.time() - init_time < timeout:
            for drone, _, q, _ in affected_drones:
                q.put((drone.sendControl, (roll, pitch, yaw, throttle)))
                sleep(0.05)


    def all_hover(self, seconds, drones: list[string]=None):
        affected_drones = self._getAffectedDrones(drones)
        timeout = seconds
        init_time = time.time()

        while time.time() - init_time < timeout:
            for drone, _, q, _ in affected_drones:
                q.put((drone.sendControl, (0, 0, 0, 0)))
                sleep(0.05)


    def all_turn_degree(self, degree, drones: list[string]=None):
        affected_drones = self._getAffectedDrones(drones)
        for drone, _, q, _ in affected_drones:
            if degree > 0:
                q.put((drone.turn_right, (degree)))
            elif degree < 0:
                q.put((drone.turn_left, (degree)))

    def all_move_forward(self, distance, units="cm", speed=0.5, drones: list[string]=None):
        affected_drones = self._getAffectedDrones(drones)
        for drone, _, q, _ in affected_drones:
            q.put((drone.move_forward, (distance, units, speed)))

    def all_move_backward(self, distance, units="cm", speed=0.5, drones: list[str] = None):
        affected_drones = self._getAffectedDrones(drones)
        for drone, _, q, _ in affected_drones:
            q.put((drone.move_backward, (distance, units, speed)))

    def all_move_left(self, distance, units="cm", speed=0.5, drones: list[str] = None):
        affected_drones = self._getAffectedDrones(drones)
        for drone, _, q, _ in affected_drones:
            q.put((drone.move_left, (distance, units, speed)))

    def all_move_right(self, distance, units="cm", speed=0.5, drones: list[str] = None):
        affected_drones = self._getAffectedDrones(drones)
        for drone, _, q, _ in affected_drones:
            q.put((drone.move_right, (distance, units, speed)))

    def all_change_throttle(self, power, time, drones: list[str] = None):
        affected_drones = self._getAffectedDrones(drones)
        for drone, _, q, _ in affected_drones:
            q.put((drone.set_throttle, (power,)))
            q.put((drone.move, (time,)))
            q.put((drone.reset_move_values, (3,)))


    def all_turn_left(self, degrees, speed=0.5, drones: list[str] = None):
        affected_drones = self._getAffectedDrones(drones)
        for drone, _, q, _ in affected_drones:
            q.put((drone.turn_left, (degrees, speed)))

    def all_turn_right(self, degrees, speed=0.5, drones: list[str] = None):
        affected_drones = self._getAffectedDrones(drones)
        for drone, _, q, _ in affected_drones:
            q.put((drone.turn_right, (degrees, speed)))

    def form_shape(self, fx, max_distance, velocity, drones: list[string]=None):
        affected_drones = self._getAffectedDrones(drones)
        coords = get_graph_points(fx, -max_distance / 2, max_distance /2, affected_drones.count())

        for i in range(len(affected_drones)):
            drone = affected_drones[i].drone
            affected_drones[i].drone_queue.put((drone.goto_waypoint, [coords[0], self.global_height, coords[1]]))

    def all_goto_height(self, height, speed: int=30, drones: list[string]=None):
        affected_drones = self._getAffectedDrones(drones)

        for drone, _, q, _ in affected_drones:
            q.put((_maintain_height, (drone, height, speed)))



    def await_standby(self, drones: list[string]=None):
        affected_drones = self._getAffectedDrones(drones)

        for _, _, q, _ in affected_drones:
            q.join()



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


def _maintain_height(drone: Drone, height: float, speed: int):
    drone_height = drone.get_height('m')
    while not approx_equals(height, drone_height, height * 0.1 if height > 1 else 0.1):
        drone_height = drone.get_height('m')
        if drone_height >= 9.98:
            continue
        if drone_height > height:
            drone.set_throttle(-speed)
            drone.move(0.2)
        elif drone_height < height:
            drone.set_throttle(speed)
            drone.move(0.2)

        drone.hover(0.1)
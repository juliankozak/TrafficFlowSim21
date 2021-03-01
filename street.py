import queue


class Street:

    L = 0
    street_name = None
    cars_queue = None # structure: [{car:"car", remained_time:3}, {car:"car", remained_time:3}]
    next_intersection = None
    simulation_manager = None
    debug_messages = False

    def __init__(self, street_name, L, next_intersection, simulation_manager, debug_messages=False):
        self.street_name = street_name
        self.L = L
        self.cars_queue = queue.Queue()
        self.next_intersection = next_intersection
        self.simulation_manager = simulation_manager
        self.debug_messages=debug_messages

    def queue_new_car(self, car):
        self.cars_queue.put(
            {'car': car,
             'remained_time': self.L
             })

    def run_simulation_step(self):
        # take all cars out of the queue one by one, update them and put them back into the queue if they need more time
        # in this street

        if self.debug_messages:
            print("--Street " + self.street_name)

        for i in range(self.cars_queue.qsize()):
            driving_car = self.cars_queue.get()

            if self.debug_messages:
                print("----Car: " + driving_car['car'].route[0] + "...")

            driving_car['remained_time'] -= 1   # decrease the remained time on the street by -1

            if self.debug_messages:
                print("----remaining waiting time: " + str(driving_car['remained_time']))

            if driving_car['remained_time'] == 0:
                if driving_car['car'].check_if_last_street() == False:
                    # move the car to the next intersection
                    self.next_intersection.add_arriving_car(driving_car['car'], self.street_name)

                    if self.debug_messages:
                        print("----moved car to intersection: " + str(self.next_intersection.intersection_id))
                else:
                    # remove the car from the simulation by not putting it onto any other intersection and calculate points
                    driving_car['car'].calculate_points(self.simulation_manager.D, self.simulation_manager.F, self.simulation_manager.current_time+1)
                    if self.debug_messages:
                        print("----car arrived, calculating points: " + str(driving_car['car'].points))
            else:
                # add the car back to the queue (keeping the order of the cars in the queue since all element are taken out)
                self.cars_queue.put(driving_car)



import queue


class Intersection:
    intersection_id = None
    queues = []     # structure: [{name:"street_name", q:Queue_of_cars} , {name:"street_name", q:Queue_of_cars} ,  ...]
    incoming_streets = []
    schedule = []   # [{street_name:"name1", Ti=duration}, {street_name:"name1", Ti=duration}, ... ]
    schedule_duration = 0
    simulation_time = 0    # simulation starts at t=0
    simulation_manager = None
    debug_messages = False

    def __init__(self, intersection_id, simulation_manager, incoming_streets=[], debug_messages=False, schedule=None, optimizer=None):
        """
        Constructor of class Intersection:
        :param intersection_id: ID of the intersection (integer)
        :param incoming_streets: list of names of incoming streets. Can be added later (easier to parse the input file)
        :param schedule: [{street_name:"name1", Ti=duration}, {street_name:"name1", Ti=duration}, ... ] (optional, can be added later manually)
        """

        self.intersection_id = intersection_id
        self.incoming_streets = incoming_streets
        self.simulation_manager = simulation_manager
        self.queues = []
        self.optimizer = optimizer

        if len(incoming_streets) > 0:
            for street in incoming_streets:
                q = {'street_name': street,
                     'q': queue.Queue()}
                self.queues.append(q)

        if schedule:
            self.verify_and_add_schedule(schedule)

        self.debug_messages = debug_messages

    def verify_and_add_schedule(self, schedule):
        # Verify schedule and store it:
        incoming_streets_schedule = []
        total_time_schedule = 0
        for s in schedule:
            if s['street_name'] not in self.incoming_streets:
                raise ValueError(
                    "Intersection {id}: Schedule contains streets that are not listed as incoming street ({e})".format(
                        id=self.intersection_id, e=s['street_name']))
            if s['Ti'] <= 0:
                raise ValueError(
                    "Intersection {id}: The schedule contains invalid duration ({e})".format(id=self.intersection_id, e=s['Ti']))
            incoming_streets_schedule.append(s['street_name'])
            total_time_schedule += s['Ti']

        if len(set(incoming_streets_schedule)) < len(incoming_streets_schedule):
            raise ValueError("Intersection {}: The schedule should contain each street at most once".format(self.intersection_id))
        self.schedule = schedule
        self.schedule_duration = total_time_schedule


    def add_incoming_street_to_intersection(self, street_name):
        """
        add an incoming street. makes parsing of input file easier, if intersection can be created without knowing all incoming streets yet
        :param street_name: name of the incoming street
        """

        # check if street already listed as incoming street
        if street_name not in self.incoming_streets:
            self.incoming_streets.append(street_name)

           # add new incoming queue instance
            q = {'street_name': street_name, 'q': queue.Queue()}
            self.queues.append(q)

    def add_arriving_car(self, car, street):
        """
        Add a car to the queue of an incoming street of an intersection
        :param car: the car object that is arriving
        :param street: name of the incoming street
        """
        for q in self.queues:
            if q['street_name'] == street:
                q['q'].put(car)

    def run_simulation_step(self, initial_step=False):
        """
        Update the state of the simulation (T = T + 1)
        """
        if self.debug_messages:
            print("--Intersection " + str(self.intersection_id))

        if len(self.schedule) > 0:  # otherwise the traffic lights are always red for this intersection.

            # Find which incoming street has green traffic light
            t_in_cycle = self.simulation_time % self.schedule_duration
            moving_street = None
            t_accumulated = 0
            for s in self.schedule: # example: t_in_cycle=3, T_0=2, T_1=2 -> moving street should be the second street in the schedule
                t_accumulated += s['Ti']
                if t_in_cycle < t_accumulated:
                    moving_street = s['street_name']
                    break

            if self.debug_messages:
                print("----Moving street: " + moving_street)

            # Move one car over the intersection into the next street on their route
            car = None
            for q in self.queues:
                if q['street_name'] == moving_street:
                    current_queue = q['q']
                    if current_queue.qsize() > 0:   # check if a car is in the queue (!)
                        car = q['q'].get()
                    break

            if car:
                next_street = car.get_next_street()

                if self.debug_messages:
                    print("----Car should be moved to " + next_street )

                # put this car onto the next street
                for street in self.simulation_manager.list_of_streets:
                    if street.street_name == next_street:
                        street.queue_new_car(car)
                        if self.debug_messages:
                            print("----Car moved to street " + next_street)
                        break

        # store queue lengths to optimizer
        if self.optimizer:
            q_lengths = []
            for q in self.queues:
                q_lengths.append(q['q'].qsize())
            self.optimizer.store_values_in_optimizer(self.intersection_id, q_lengths, self.simulation_time)

        self.simulation_time += 1


    def reset_intersection_state(self):
        # reset simulation time:
        self.simulation_time = 0
        # empty all queues:
        for q in self.queues:
            while not q['q'].empty():
                q['q'].get()








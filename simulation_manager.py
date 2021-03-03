import intersection
import car
import street


class Simulation_manager:

    D = 0   # duration of the simulation
    I = 0   # number of intersections
    S = 0   # number of streets
    V = 0   # number of cars
    F = 0   # bonus points

    list_of_cars = []
    list_of_streets = []
    list_of_intersections = []
    current_time = 0
    optimizer = None

    debug_messages = False

    def __init__(self, filename, optimizer=None, debug_messages=False):
        self.debug_messages = debug_messages
        self.optimizer = optimizer
        self.read_input_file_and_create_object_instances(filename)
        if self.optimizer:
            self.optimizer.initialize_optimizer(self.list_of_intersections, self.D)


    def run_simulation_step(self, print_frequency=100):

        if self.current_time % print_frequency == 0:
            print("running simulation {} / {}".format(self.current_time, self.D))

        #update all streets
        for s in self.list_of_streets:
            s.run_simulation_step()
        #update all intersections
        for i in self.list_of_intersections:
            i.run_simulation_step()

        self.current_time += 1

    def read_input_file_and_create_object_instances(self, filename):
        with open(filename) as f:
            self.parse_first_line(f.readline())
            for i in range(self.S):
                self.parse_street(f.readline())
            for v in range(self.V):
                self.parse_cars(f.readline())

    def parse_first_line(self, first_line):
        vals = first_line.split(" ")
        self.D = int(vals[0])
        self.I = int(vals[1])
        self.S = int(vals[2])
        self.V = int(vals[3])
        self.F = int(vals[4])

    def parse_street(self, line):
        vals = line.split(" ")
        B = int(vals[0])     # intersection beginning of the street
        E = int(vals[1])     # intersection end of the street
        name = vals[2]  # street name
        L = int(vals [3])    # length of the street

        # check if E intersection already exists
        next_intersection = None
        for current_intersection in self.list_of_intersections:
            if current_intersection.intersection_id == E:
                next_intersection = current_intersection
                next_intersection.add_incoming_street_to_intersection(name)
                break
        if not next_intersection:
            # create intersection
            next_intersection = intersection.Intersection(E, self, incoming_streets=[name],
                                                          debug_messages=self.debug_messages, optimizer=self.optimizer)
            self.list_of_intersections.append(next_intersection)

        # create the street instance
        s = street.Street(name, L, next_intersection, self,debug_messages=self.debug_messages)
        self.list_of_streets.append(s)
        print(" Street {} created".format(name))

    def parse_cars(self, line):
        vals = line.split("\n")[0].split(" ")
        route = []
        for i in range(int(vals[0])):
            route.append(vals[i+1])

        new_car = car.Car(route)
        self.list_of_cars.append(new_car)
        print(" Created car {}, {}, ...".format(route[0], route[1]))

    def initialize_all_schedules_uniform(self, value):
        """
        Initialize schedule of all intersections with 'value' seconds for each incoming street
        """

        print("Initializing all intersection schedules uniformly with Ti = {}s ".format(value))

        for i in self.list_of_intersections:
            incoming_streets = i.incoming_streets
            new_schedule = []
            for s in incoming_streets:
                new_dict = {'street_name': s,
                            'Ti': value}
                new_schedule.append(new_dict)
            i.verify_and_add_schedule(new_schedule)

        print("Initializing finished.")

    def write_schedule_to_file(self, filename):
        """
        assuming, we have a schedule for every intersection
        """
        with open(filename, 'w') as f:
            f.write("{} \n".format(str(len(self.list_of_intersections)))) # number of intersections with traffic light schedules

            for current_intersection in self.list_of_intersections:
                f.write("{} \n".format(str(current_intersection.intersection_id)))   # id
                f.write("{} \n".format((str(len(current_intersection.schedule)))))  # number of incoming streets with schedule
                for entry in current_intersection.schedule:
                    f.write("{} {} \n".format(entry['street_name'], entry['Ti']))      # streetname Ti

    def calculate_points(self):
        total = 0
        for c in self.list_of_cars:
            total += c.points

        return total

    def get_cars_ready(self):
        """
        put all cars into the queue of the intersection at the end of the first street of their schedule
        """
        print("Start getting cars ready...")

        for c in self.list_of_cars:
            starting_street = c.get_next_street()
            for s in self.list_of_streets:
                if s.street_name == starting_street:
                    first_intersection = s.next_intersection
                    first_intersection.add_arriving_car(c, starting_street)
                    break


        for i in self.list_of_intersections:
            # if the intersection is free to move (green), move the car over the intersection to the beginning of the
            # next street before starting the simulation. Otherwise one second is lost because the streets are updated
            # before the intersections
            i.run_simulation_step(initial_step=True)

        print("All cars ready to go!")

    def run_simulation(self, print_frequency):
        self.current_time = 0   # reset time to zero

        # reset intersection states
        for i in self.list_of_intersections:
            i.reset_intersection_state()

        # reset street states
        for s in self.list_of_streets:
            s.reset_street_state()

        # reset car states
        for c in self.list_of_cars:
            c.reset_car_state()

        self.get_cars_ready()

        print("Start simulation")
        for i in range(self.D):
            self.run_simulation_step(print_frequency)
        print("Simulation finished")



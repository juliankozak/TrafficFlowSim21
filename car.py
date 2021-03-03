
class Car:

    route = []
    num_streets = 0
    current_index_in_route = 0
    points = 0

    def __init__(self, route):
        """
        Constructor of class Car
        :param route: list of street names
        """
        self.route = route
        self.num_streets = len(self.route)

    def get_next_street(self):
        """
        get the name of the next street, the car has to enter
        :return next_street: name of next street the car has to enter
        """

        if self.current_index_in_route > self.num_streets-1:
            raise ValueError("Error: The car already reached the end of the route. No further streets available")

        # street[0] taken for initialization, then current_index = 1 and car is waiting at first intersection.
        next_street = self.route[self.current_index_in_route]
        self.current_index_in_route += 1

        return next_street

    def check_if_last_street(self):
        """
        If last street was queried with get_next_street(), the car should be removed from the simulation
        (there are no more intersections to travel through)
        :return is_last_street: always False except if there are no more streets on the route (the car is removed
        from the simulation at the end of the street)
        """
        is_last_street = False if (self.current_index_in_route < len(self.route)) else True
        #print("#### check_if_last_street: " + "current index in route " + str(self.current_index_in_route) + " len route: " + str(len(self.route)) )
        return is_last_street

    def calculate_points(self, D, F, T):
        """
        calculate number of points received for completing the drive through the city.
        :param D: duration of the simulation
        :param F: number of extra points
        :param T: time of arrival
        :return: number of points = F + (D - T)
        """
        if self.current_index_in_route != self.num_streets:
            raise ValueError("Error: The car must reach the end of his route before calculating the points.")

        if T <= D:
            points = F + (D-T)
        else:
            points = 0

        self.points = points
        return self.points

    def reset_car_state(self):
        self.current_index_in_route = 0
        self.points = 0
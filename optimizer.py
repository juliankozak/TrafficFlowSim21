import numpy as np

"""
Task: Derive a class from Optimizer and implement optimizer_step()

- queue_lengths at all times of all intersections are available in Optimizer (3-dim array)
- derive new schedule in the given format and return it. 
  Only intersections with an new schedule will be update. All other intersections keep their old schedule.
   return:
    [
          {'intersection_id': 1,
               'new_schedule': [ {street_name:"name1", Ti=duration}, {street_name:"name1", Ti=duration}}]
          },
          { 'intersection_id': 2,
                'new_schedule': [...] 
          }
     ]
"""


class Optimizer:

    q_lengths = None    # store queue length of each incoming street of each intersection at each time
                            # number of rows = number of intersections
                            # number of columns = number of intersections (largest value possible) - if an intersection has less incoming streets, fill with nans
                            # third dimension = time duration of simulation
                            # example: [[ [2, 3, 0, nan, nan],
                            #            [1, 1, 1,   0,   0],
                            #            [0, 0, 0, nan, nan] ]]
                            # dtype: np array

    mapping = []            # for each intersection, map name of incoming street to index in list
                            # [ {id: 0, incoming_streets: [street-a, street-b, ...]},
                            #   {id: 1, incoming_streets: [...], ...   ]

    simulation_manager = None

    def __init__(self, simulation_manager=None):
        self.simulation_manager = simulation_manager

    def initialize_optimizer(self, list_of_intersections, duration_of_simulation):
        self.initialize_mapping(list_of_intersections)

        num_intersections = len(list_of_intersections)
        max_num_incoming_streets = 0
        for intersection in list_of_intersections:
            # find the intersection with the most incoming streets
            if len(intersection.incoming_streets) > max_num_incoming_streets:
                max_num_incoming_streets = len(intersection.incoming_streets)

        self.q_lengths = np.zeros((duration_of_simulation+1, num_intersections, max_num_incoming_streets, ))

        # fill unused part of array with nan (for all simulation times)
        for intersection in list_of_intersections:
            self.q_lengths[:, intersection.intersection_id, len(intersection.incoming_streets):] = np.nan;
        print("Optimizer initialized.")

    def initialize_mapping(self, list_of_intersections):
        for intersection in list_of_intersections:
            self.mapping.append( [] )

        for intersection in list_of_intersections:
            self.mapping[intersection.intersection_id] = {
                    'id': intersection.intersection_id,
                    'incoming_streets': intersection.incoming_streets   # keeping the same order as list of incoming streets in intersection
                }

    def get_index_of_incoming_street(self, intersection_id, street_name):
        index = None
        for m in self.mapping:
            if m['id'] == intersection_id:
                m_list = m['incoming_streets']
                for index, s in enumerate(m_list):
                    if s == street_name:
                        return index
                    #index = m_list.index(street_name)  # very slow
        return index

    def store_values_in_optimizer(self, intersection_id, q_lengths, current_time):
        """
        store the current queue lengths of an intersection
        :param intersection_id
        :param q_lengths: list of queue lengths, keeping the same order as saved in the intersection
        :param current_time
        :return:
        """
        #for i in range(len(q_lengths)):
            #print("current time: {} , id: {} , q_lengths {}".format(current_time, intersection_id, q_lengths[i]))
        self.q_lengths[current_time, intersection_id, :len(q_lengths)] = np.array(q_lengths)

    def optimizer_step(self):
        """
        optimizer_step should be implemented for a custom optimizer
        :return: the schedule, that needs to be updated. Can also return the entire schedule for all traffic lights.
          expected structure of return value:
                 [
                  {'intersection_id': 1,
                   'new_schedule': [ {street_name:"name1", Ti=duration}, {street_name:"name1", Ti=duration}}]
                  },
                  { 'intersection_id': 2,
                    'new_schedule': [...] }
                 ]
        """
        print("INFO: method 'optimizer_step' should be overwritten in order to update traffic light schedule")
        pass

    def optimizer_step_and_load(self):
        schedule_modifications = self.optimizer_step()
        self.load_modified_schedule_into_intersections(schedule_modifications)

    def load_modified_schedule_into_intersections(self, modifications):
        print("Loading schedule modifications into intersections ...")
        for intersection_mod in modifications:
            id = intersection_mod['intersection_id']

            for intersection in self.simulation_manager.list_of_intersections:
                if intersection.intersection_id == id:
                    #verify and update schedule in corresponding intersection object
                    intersection.verify_and_add_schedule(intersection_mod['new_schedule'])
        print("Finished loading.")

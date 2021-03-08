from optimizer import Optimizer
import numpy as np
import pickle
import datetime

"""
    removed unused incoming streets from schedule
    hoping to increase the number of arriving cars for dataset "d"  
"""

class OptimizerRemoveUselessIncomingStreets(Optimizer):

    def optimizer_step(self):
        """
        Adapt schedule such that Ti matches average queue length of each incoming street of an intersection
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

        schedule_update = []
        text_file_lines = []
        # Intersection by intersection
        for current_intersection in self.simulation_manager.list_of_intersections:

            schedule_update_int = []
            for incoming_street in current_intersection.incoming_streets:

                current_schedule = None
                if current_intersection.traffic_stats[current_intersection.mapping[incoming_street]] > 0:
                    # keep this incoming street in schedule
                    current_schedule = [sch for sch in current_intersection.schedule if sch['street_name'] == incoming_street][0]
                else:
                    print(" -- Intersection {} remove incoming street from schedule: {} (index = {})".format(current_intersection.intersection_id, incoming_street,current_intersection.mapping[incoming_street] ))

                if current_schedule is not None:
                    schedule_update_int.append(current_schedule)

            if len(schedule_update_int) > 0:
                schedule_update.append(
                    {
                        'intersection_id': int(current_intersection.intersection_id),
                        'new_schedule': schedule_update_int
                    }
                )

            outline = "intersection {}".format(current_intersection.intersection_id)
            for i in range(len(current_intersection.traffic_stats)):
                outline += " ; {}".format(current_intersection.traffic_stats[i])
            outline += "\n"
            text_file_lines.append(outline)

        filename = "debug_data/d_traffic_stats_{}.csv".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        with open(filename, "w") as f:
            for line in text_file_lines:
                f.write(line)

        return schedule_update

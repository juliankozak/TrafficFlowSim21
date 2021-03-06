from optimizer import Optimizer
import numpy as np
import pickle
import datetime

class OptimizerMatchAvgQueueLength(Optimizer):

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

        # take mean queue length over entire simulation time
        q_avg = np.nanmean(self.q_lengths, 0)    # ignore nan

        # save q_avg for visualization / better understanding
        filename = "debug_data/q_avg_{}.pck".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        pickle.dump(q_avg, open(filename, "wb"))

        # create the output data -> list of dictionaries with new schedules
        schedule_update = []
        for i in range(q_avg.shape[0]): # intersection by intersection

            # load the existing schedule to update it later
            current_intersection = [inter for inter in self.simulation_manager.list_of_intersections if inter.intersection_id == i][0]
            incoming_streets_new_schedule = current_intersection.schedule

            # update the existing schedule
            N_intersection = np.count_nonzero(~np.isnan(q_avg[i, :]))

            for s in range(N_intersection):
                val = int(np.ceil(q_avg[i, s]))     # CEIL average value
                if val > 0:
                    # resolve s to street_name via mapping
                    current_street_name = [n for n in self.mapping if n['id'] == i][0]['incoming_streets'][s]

                    # add extra time to existing schedule
                    for index, schedule in enumerate(incoming_streets_new_schedule):
                        if schedule['street_name'] == current_street_name:
                            incoming_streets_new_schedule[index] = {
                                'street_name': current_street_name,
                                'Ti': schedule['Ti'] + val
                            }

            if len(incoming_streets_new_schedule) > 0:
                schedule_update.append(
                    {
                        'intersection_id': int(i),
                        'new_schedule': incoming_streets_new_schedule
                    }
                )

        return schedule_update

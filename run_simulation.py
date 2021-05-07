import simulation_manager
import strategy_remove_unused_incoming_streets_d
import argparse
import datetime

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='Run hashcode simulation from commandline')
    my_parser.add_argument("--experiment", type=str)
    my_parser.add_argument("--init", type=int)
    args = my_parser.parse_args()

    experiment = args.experiment
    init_schedule_val = args.init
    print_frequency = 500
    show_debug_messages = False     # write

    filename = "input_data/" + experiment + ".txt"
    out_file_suffix = "_Optimizer_remove_incoming_streets"

    # Number of iterations
    N_epoch = 2

    sim_manager = simulation_manager.Simulation_manager(filename, optimizer=None, debug_messages=show_debug_messages)

    opt = strategy_remove_unused_incoming_streets_d.OptimizerRemoveUselessIncomingStreets(simulation_manager=sim_manager) #this optimizer should not be passed to simulation manager - todo, quick and dirty

    # INITIALIZE TRAFFIC LIGHT SCHEDULE
    sim_manager.initialize_all_schedules_uniform(init_schedule_val) # initialize with 1 for dataset d - otherwise 0 points

    # RUN SIMULATION
    for i in range(N_epoch):
        print("** EPOCH {}: **".format(i))

        filename = "schedule_{}_{}_epoch_{}.txt".format(experiment, out_file_suffix, i)
        schedule_filename = "output_schedules/" + experiment + out_file_suffix + "_epoch_" + str(i) + "_init_" + str(init_schedule_val) + \
            "_schedule_{}.txt".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        sim_manager.write_schedule_to_file(schedule_filename)

        sim_manager.run_simulation(print_frequency)

        total_points = sim_manager.calculate_points()
        print("Total points: {}".format(total_points))

        # write points to a file with same name as schedule.
        filename_points = "output_schedules/" + experiment + out_file_suffix + "_epoch_" + str(i) + \
                  "_points_{}.txt".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        with open(filename_points, "w") as f:
            f.write("Total points: {} \n".format(total_points))
            f.write("Init uniformly with {} \n".format(init_schedule_val))
            f.write("Schedule: {} \n".format(schedule_filename) )

        print("optimizing schedule...")
        opt.optimizer_step_and_load()
        print("finished optimizing schedule")

        for cu in sim_manager.list_of_intersections:
            cu.initialize_traffic_stats()

    print("--- simulation finished.")





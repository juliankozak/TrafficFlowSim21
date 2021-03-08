import simulation_manager
import optimizer
import strategy_average_queue_length
import strategy_remove_unused_incoming_streets_d


experiment = "d"
print_frequency = 500
show_debug_messages = False     # write

filename = "input_data/" + experiment + ".txt"
out_file_suffix = "_Optimizer_remove_incoming_streets"

# Number of iterations
N_epoch = 2

sim_manager = simulation_manager.Simulation_manager(filename, optimizer=None, debug_messages=show_debug_messages)

opt = strategy_remove_unused_incoming_streets_d.OptimizerRemoveUselessIncomingStreets(simulation_manager=sim_manager) #this optimizer should not be passed to simulation manager - todo, quick and dirty

# INITIALIZE TRAFFIC LIGHT SCHEDULE
sim_manager.initialize_all_schedules_uniform(1) # initialize with 1 for dataset d - otherwise 0 points

# RUN SIMULATION
for i in range(N_epoch):
    print("** EPOCH {}: **".format(i))

    filename = "schedule_{}_{}_epoch_{}.txt".format(experiment, out_file_suffix, i)
    sim_manager.write_schedule_to_file(
        "output_schedules/" + experiment + out_file_suffix + "_epoch_" + str(i) + "_schedule.txt")

    sim_manager.run_simulation(print_frequency)

    total_points = sim_manager.calculate_points()
    print("Total points: {}".format(total_points))

    print("optimizing schedule...")
    #opt.optimizer_step()
    opt.optimizer_step_and_load()
    print("finished optimizing schedule")

    for cu in sim_manager.list_of_intersections:
        cu.initialize_traffic_stats()

print("--- simulation finished.")
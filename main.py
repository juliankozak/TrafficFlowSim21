import simulation_manager
import optimizer
import strategy_average_queue_length
import cProfile

experiment = "c"
print_frequency = 200
show_debug_messages = False     # write

filename = "input_data/" + experiment + ".txt"
out_file_suffix = "OptimizerMatchAvgQueueLength"

N_epoch = 2

#opt = optimizer.Optimizer()
opt = strategy_average_queue_length.OptimizerMatchAvgQueueLength()

sim_manager = simulation_manager.Simulation_manager(filename, optimizer=opt, debug_messages=show_debug_messages)
opt.simulation_manager = sim_manager

# INITIALIZE TRAFFIC LIGHT SCHEDULE
sim_manager.initialize_all_schedules_uniform(2)

# RUN SIMULATION
for i in range(N_epoch):
    print("** EPOCH {}: **".format(i))
    sim_manager.run_simulation(print_frequency)
    #cProfile.run('sim_manager.run_simulation(print_frequency)')
    total_points = sim_manager.calculate_points()
    print("Total points: {}".format(total_points))

    opt.optimizer_step_and_load()

    filename = "schedule_{}_{}_epoch_{}_points_{}.txt".format(experiment, out_file_suffix, i, total_points)
    sim_manager.write_schedule_to_file("output_schedules/" + experiment + out_file_suffix + "_epoch_" + str(i) + "_schedule.txt")

print("--- simulation finished.")
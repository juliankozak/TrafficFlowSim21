import simulation_manager
import optimizer

experiment = "a"
print_frequency = 1
show_debug_messages = False     # write

filename = "input_data/" + experiment + ".txt"

opt = optimizer.Optimizer()
sim_manager = simulation_manager.Simulation_manager(filename, optimizer=opt, debug_messages=show_debug_messages)
opt.simulation_manager = sim_manager

# INITIALIZE TRAFFIC LIGHT SCHEDULE
sim_manager.initialize_all_schedules_uniform(2)

# RUN SIMULATION
sim_manager.run_simulation(print_frequency)
print("Total points: {}".format(sim_manager.calculate_points()))

opt.optimizer_step()

sim_manager.run_simulation(print_frequency)
print("Total points: {}".format(sim_manager.calculate_points()))

sim_manager.write_schedule_to_file("output_schedules/" + experiment + "_schedule.txt")

print("--- simulation finished.")
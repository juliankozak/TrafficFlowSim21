import simulation_manager

experiment = "c"
print_frequency = 100
show_debug_messages = False

filename = "input_data/" + experiment + ".txt"

sim_manager = simulation_manager.Simulation_manager(filename, debug_messages=show_debug_messages)
sim_manager.initialize_all_schedules_uniform(2)
sim_manager.get_cars_ready()

sim_manager.run_simulation(print_frequency)

print("Total points: {}".format(sim_manager.calculate_points()))

sim_manager.write_schedule_to_file("output_schedules/" + experiment + "_schedule.txt")

print("--- simulation finished.")
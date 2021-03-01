from car import Car
from intersection import Intersection
from street import Street
from simulation_manager import Simulation_manager

sim_manager = Simulation_manager(10);
sim_manager.F = 1000


# CAR
print("--- create CAR")
car = Car(["street-1", "street-2"])
sim_manager.list_of_cars.append(car)

# INTERSECTION
print("--- create INTERSECTIONS")
intersection1 = Intersection(1, sim_manager, ["street-1"], schedule=[{"street_name": "street-1", "Ti": 2}])
intersection2 = Intersection(2, sim_manager, ["street-2"], schedule=[{"street_name": "street-2", "Ti": 2}])

sim_manager.list_of_intersections.append(intersection1)
sim_manager.list_of_intersections.append(intersection2)

# STREET
print("--- create STREETS")
street1 = Street("street-1", 3, intersection1, sim_manager)
street2 = Street("street-2", 1, intersection2, sim_manager)
sim_manager.list_of_streets.append(street1)
sim_manager.list_of_streets.append(street2)

# SIMULATION
print("--- test SIMULATION")
print("initialize")
intersection1.add_arriving_car(car, "street-1")

print("round 1")
street1.run_simulation_step()
street2.run_simulation_step()
intersection1.run_simulation_step()
intersection2.run_simulation_step()
print(" Points:", car.points)

print("round 2")
street1.run_simulation_step()
street2.run_simulation_step()
intersection1.run_simulation_step()
intersection2.run_simulation_step()
print(" Points:", car.points)

print("round 3")
street1.run_simulation_step()
street2.run_simulation_step()
intersection1.run_simulation_step()
intersection2.run_simulation_step()
print(" Points:", car.points)

print("round 4")
street1.run_simulation_step()
street2.run_simulation_step()
intersection1.run_simulation_step()
intersection2.run_simulation_step()
print(" Points:", car.points)

print("round 5")
street1.run_simulation_step()
street2.run_simulation_step()
intersection1.run_simulation_step()
intersection2.run_simulation_step()
print(" Points:", car.points)

print("--- ok")



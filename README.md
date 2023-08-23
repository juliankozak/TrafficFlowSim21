## Google Hashcode 2021, Traffic Signalling

Problem Statement: [Problem_statement.pdf](https://github.com/juliankozak/hashcode_2021_traffic_lights/blob/7f341982f9dc46a46dca29817969627795db6ab0/_Problem_statement.pdf)

### Brief description:
A city is described as a list of streets with intersections and connecting streets. Each intersection has a traffic light at every incoming street. For a given set of cars that have fixed routes through the streets of the city, the goal is to optimize the traffic light schedule in a way that as many cars as possible arrive at their destination as quickly as possible. The topology of the city and the number and routes of the car vary from dataset to dataset.

**Output**: Schedule for each traffic light, optimized in a way that as many cars as possible arrive at their destination
before the simulation ends. 


The initial idea was, having access to the queues at the incoming streets of each intersection, it should be possible to
find an optimization based on the average queue length. 

The simulation was rewritten in order to have access to the queue lengths. The simulation was then used to find an optimization based on the average queue length. The city is modeled in an object oriented way, with object classes car, intersection, street. The simulation is managed by the simulation_manager. The simulation_manager has access to the queue lengths at the incoming streets of each intersection. The simulation_manager is used by the optimizer to find an optimization based on the average queue length.

**Source code files:**  
run_batch.sh   
run_simulation.py   
simulation_manager.py   
intersection.py   
car.py  
street.py  
optimizer.py  

It turned out that the success of the optimization strongly depends on the input dataset = the city shape (b,c,d,e or f).
Some scenarios are very uniformly distributed, some other have a star shape with some crucial intersections that act as a bottleneck. 


Then it became clear that a better insight into the data is needed:
The following auxiliary jupyter notebooks were used to get a better understanding of the data:

**analysis_independent_paths.ipynb:** find intersections, where cars are only coming from a single incoming street.  
**analysis_common_streets.ipynb:** try to find streets that were used by many cars (common streets).  
**analyse_path_lengths.ipynb:** look at the path lengths of the cars compared to the number of streets available  
**optimization_common_paths(_v2).ipynb:** The idea was to find the N streets that have the highest traffic and to try to connect them to form "common paths", that are worth optimizing.
Starting from the longest common path, we started optimizing the traffic light schedule in a way, that the time to drive along the path is minimum.
To do so, only incoming streets with traffic were considered. The order of the green light sequence was permutated in a way to try to minimize the waiting time at the traffic light. If no permutation was possible, an extra delay was accepted. 
 The duration of the green phase was fixed to 1s. The duration of the schedule of each traffic light was therefore fixed and only permutations were used to minimize the waiting times.    
 
 Unfortunately it turned out that connecting frequently used streets to form common paths do not truly represent the paths driven by the cars. The connection to the paths of the cars is lost since in many scenarios, just a few cars pass each street during the simulation. Therefore there are many streets with a very close number of usages. Connecting theses streets might randomly match the paths of some cars but not match the paths of a significant amount of cars.   

After the extended round of the google hashcode challenge, the same problem was released on Kaggle with a new dataset. All cars have routes of length = 120 and the traffic seems to be very uniformly distributed over the map. 

### Conclusion
It is a tough topic and I would like to know the best solution one day, but for now I just publish my code in case somebody is interested in it and wants to use the queue length for the optimization. Have fun with it!



  

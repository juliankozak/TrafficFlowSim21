# Google Hashcode 2021 - Traffic signalling

Input: List of streets and intersections and how they are connected. List of cars and the route they are driving

Output: Schedule for each traffic light, optimized in a way that as many cars as possible arrive at their destination
before the simulation ends. 

problem statement: _hashcode_2021_online_qualifications.pdf

### First round: 4 hours competition in the evening
Understanding the problem statement, analyzing input and output file format.

Submitted solution: simple schedule, where each incoming street of an intersection gets green for a duration of 1 second, 
no matter if any car is arriving through the intersection or not.

### Second round (extended round) 
Approach: 
Programming the entire simulation with streets and cars that move along streets. The points calculated by the simulation
equal the points displayed in Hashcode Dashboard when uploading the respective schedule.

The initial idea was, having access to the queues at the incoming streets of each intersection, it should be possible to
find an optimization based on the average queue length. 

It turned out that the success of the optimization strongly depends on the input dataset (b,c,d,e or f).
Some scenarios are very uniformly distributed, some other have a star shape with some crucial intersections. 


run_batch.sh
run_simulation.py
simulation_manager.py
intersection.py
car.py
street.py
optimizer.py


Then it became clear that a better insight into the data is needed:

analysis_independent_paths.ipynb: find intersections, where cars are only coming from a single incoming street. 

analysis_common_streets.ipynb: try to find streets that were used by many cars (common streets). 

analyse_path_lengths.ipynb: look at the path lengths of the cars compared to the number of streets available, the 
simulation time.

optimization_common_paths(_v2).ipynb: The idea was to find the N streets that have the highest traffic and to try to connect them to form "common paths", that are worth optimizing.
Starting from the longest common path, we started optimizing the traffic light schedule in a way, that the time to drive along the path is minimum.
To do so, only incoming streets with traffic were considered. The order of the green light sequence was permutated in a way to try to minimize the waiting time at the traffic light. If no permutation was possible, an extra delay was accepted. 
 The duration of the green phase was fixed to 1s. The duration of the schedule of each traffic light was therefore fixed and only permutations were used to minimize the waiting times. 
 
 Unfortunately it turned out that connecting frequently used streets to form common paths do not truly represent the paths driven by the cars. The connection to the paths of the cars is lost since in many scenarios, just a few cars pass each street during the simulation. Therefore there are many streets with a very close number of usages. Connecting theses streets might randomly match the paths of some cars but the real connection is lost.    


### Problemset available in Kaggle
The same challenge was released on Kaggle with a new dataset. All cars have routes of length = 120 and the traffic seems to be very uniformly distributed over the map. 
The easiest approach would be to submit a schedule with uniformly 1 for each incoming street of an intersection, where there is traffic. 


### Lessons learned
Understand the data before starting any big programming story.

Rewriting the entire simulation turned out to be useless, even though the calculated points matched the points displayed in the dashboard. This was a very nice feeling, once the simulation was correct. The idea was to have access to the queue lengths in order to perform some optimization. It could have been estimated beforehand, that the queue lengths might be very short in most cases since only very few cars pass each single intersection during the simulation



  

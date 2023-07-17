# Vehicle Routing Problem

Your homework will be to solve the Vehicle Routing Problem using the ant colony optimization. The VRP is just a generalized travelling salesman problem – the goal is to optimize the delivery of parcels for a delivery company. We have depots, each with its own vehicles with a given capacity and a set of shipments that need to be delivered to their owners. The goal is to find a set of delivery routes in such a way that all shipments are delivered to the owners and that the total cost is minimized. More specifically, that the least number of vehicles is used and that the routes are as short as possible.

For the homework, we will use a simplified version of this problem with a single depot that has an unlimited number of vehicles of one type. The input data can be found in the attached zip file. It contains three different inputs in the XML format - 2 small ones and a larger one. Each file contains:

    A list of nodes with x and y coordinates, where the node with type 0 is a depot, and the others with type 1 are customer locations.
    A list of vehicles, in this case we have one type of vehicle that must start and end at the depot and has a maximum capacity of items it can carry.
    A list of requirements, i.e. to which node what needs to be delivered.



## My solution

In my solution, I have implemented classes for City, Requests, Cars, and Fleet. I have also added the Fleet class to handle multiple cars, although some modifications may be required to make it work for different types of cars. The Map class combines all of these classes and creates the necessary components for the algorithm to function.

The Aco file consists of the Colony and Ant classes. The key part of the algorithm lies within the Colony class, where for each ant, we construct a path that represents a plausible solution. The construction of the path ensures that the car is not overloaded. We select cities to visit by creating a list of unvisited cities and making decisions based on the distance matrix and pheromone matrix. Factors such as alpha, beta, evaporation rate, probability of selecting the city with the highest probability, and initial pheromone strength were chosen based on an experimentation, which can be found in files parameters_experiment.txt. In file output can be seen more information about a result of a simulation.
In folder out plot of convergens of each file can be viewed.

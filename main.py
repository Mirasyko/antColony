from map_init import initilize_map
from aco import Colony
import time

def main():
    total_start_time = time.time()
    print("Starting at: ", time.strftime("%H:%M:%S", time.gmtime(total_start_time + 2 * 3600)), end='\n')
    
    # data_32 = (1, 2.5, 0.8, 0.8, 0.15)
    data_72 = (1, 3, 0.7, 0.8, 0.3)
    # data_422 = (0.5, 3, 0.7, 0.9, 0.2)

    number_of_ants = 30
    number_of_iterations = 30
    filenames = [
                # 'data/data_422.xml',
                'data/data_72.xml', 
                # 'data/data_32.xml'
                ]

    for filename, params in zip(filenames, [data_72]): # [data_422, data_72, data_32]
        
        # Unpack params
        alpha = params[0]
        beta = params[1]
        evaporation_rate =  params[2]
        init_pheromone = params[3]
        probability_to_pick_the_best =  params[4]

        print('#' * 50)
        print("File: ", filename)
        print('#' * 50)
 
        solution_time = time.time()  

        map, _ = initilize_map(filename, evaporation_rate, init_pheromone)
        colony = Colony(map, number_of_iterations, number_of_ants, beta, alpha, probability_to_pick_the_best)
        colony = colony.construct_path()
        
        end_loop_time = round(time.time() - solution_time, 4)

        # Plotting results
        n_cars = map.best_path.count(map.depot) - 1
        map.plot_convergence()

        print("Number of iterations: ", number_of_iterations)
        print("Number of ants: ", number_of_ants)
        print("Alpha: ", alpha)
        print("Beta: ", beta)
        print("Evaporation rate: ", evaporation_rate)
        print("Init pheromone: ", init_pheromone)
        print("Probability to pick the best: ", probability_to_pick_the_best)
        print('-' * 50)
        print("Result of Simulation")
        print('-' * 50)
        print("Number of cars: ", n_cars)
        print("Distance ", map.best_path_distance)
        print("Solution found in  %s seconds" % (end_loop_time))
        print('-' * 50, end='\n\n')
        del map, colony

    total_end_time = round(time.time() - total_start_time, 4)
    print("Total time: %s seconds" % (total_end_time))


if __name__ == "__main__":
    main()
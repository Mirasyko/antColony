import numpy as np
from map_init import Map, City
import numpy as np

class Colony:
    def __init__(self, globe: Map, n_iter: int, n_ants: int, beta: float, alpha:float, q0: float) -> None:
        self.globe = globe
        self.alpha = alpha
        self.beta = beta
        self.n_iter = n_iter
        self.n_ants = n_ants
        self.q0 = q0
        self.best_path = None
        self.best_path_length = np.inf
        self.convergence = []
        self.ants = []
    
    def construct_path(self):
        for _ in range(self.n_iter):

            ants = list(Ant(self.globe, self.alpha, self.beta, [self.globe.depot]) for _ in range(self.n_ants))
            for k in range(self.n_ants):
            
                while not ants[k].visited_all():
                    next_city = self.select_next_index(ants[k])
                    if not ants[k].condition(next_city):
                        next_city = self.select_next_index(ants[k])
                        if not ants[k].condition(next_city):
                            next_city = self.globe.depot
                    ants[k].move_to_city(next_city)

                    self.globe.update_pheromones_local(ants[k].current_city, next_city)

                ants[k].move_to_city(self.globe.depot)
                self.globe.update_pheromones_local(ants[k].current_city, self.globe.depot)

            ants_completed_path = list(ant for ant in ants if ant.path_length > 0)
            paths_distance = np.array([ant.path_length for ant in ants_completed_path])

            best_index = np.argmin(paths_distance)
            if (self.best_path is None or (paths_distance[best_index] < self.best_path_lenght
                                           and paths_distance[best_index] > 0 
                                           and ants[int(best_index)].get_active_cars_num() <= self.globe.car_num)
                ):

                self.best_path = ants[int(best_index)].path
                self.best_path_lenght = paths_distance[best_index]
                self.convergence.append(self.best_path_lenght)
                self.best_vehicle_num = self.best_path.count(0) - 1
                self.globe.best_route_car_num = ants[int(best_index)].get_active_cars_num()
            
            elif self.best_path_lenght > 0:
                self.convergence.append(self.best_path_lenght)

            self.globe.update_phermones_global(self.best_path, self.best_path_lenght)

        self.globe.update_best_path(self.best_path, self.convergence)
        self.best_path = self.globe.best_path
        self.best_path_lenght = self.globe.best_path_distance
        
        return self
    
  
    def select_next_index(self, ant):
        current_city = ant.current_city
        indecies_to_visit = [city.index for city in ant.unvisited]

        transition_prob = np.power(self.globe.pheromone_matrix[current_city.index][indecies_to_visit], self.alpha) * \
            np.power(self.globe.inverse_distance[current_city.index][indecies_to_visit], self.beta)
        
        transition_prob = transition_prob / np.sum(transition_prob)

        if np.random.rand() < self.q0:
            max_prob_index = np.argmax(transition_prob)
            next_index = indecies_to_visit[max_prob_index]
        else:
            sum_tran_prob = np.sum(transition_prob)
            norm_transition_prob = transition_prob/sum_tran_prob
            next_index = np.random.choice(indecies_to_visit, 1, p=norm_transition_prob)[0]
            
            while next_index == self.globe.depot.index and len(indecies_to_visit) > 1:
                next_index = np.random.choice(indecies_to_visit, 1)[0]
                return self.globe.cities[next_index]
            
            if len(indecies_to_visit) == 1:
                next_index = indecies_to_visit[0]
                return self.globe.cities[next_index]

        return self.globe.cities[next_index]

class Ant:
    def __init__(self, globe: Map, alpha: float, beta: float, visited):
        self.globe: Map = globe
        self.visited: list = visited
        self.current_city: City = globe.cities[0]
        self.beta: float = beta
        self.alpha: float = alpha
        self.path: list = []
        self.path_length: int = 0
        self.load: float|int = 0
        self.unvisited: list = globe.cities[:]


    def init_ant(self):
        self.path = []
        self.path_length = 0

    def move_to_city(self, city: City):
        self.path.append(city)
        self.path_length += self.globe.distance_matrix[self.current_city.index, city.index]
        if city.index == 0:
            self.load = 0
        
        else:
            self.load += city.request.quantity
            self.visited.append(city)
            self.unvisited.remove(city)

        self.current_city = city
    
    def visited_all(self):
        return len(self.visited) == len(self.globe.cities) - 1 # because of depot

    def get_active_cars_num(self):
        return self.path.count(self.globe.depot) - 1
    
    def condition(self, next_city: City):
        if next_city.type == "0":
            return False
        
        if next_city in self.visited:
            return False
        
        if next_city.request.quantity < 0:
            return False
        
        if self.load + next_city.request.quantity > self.globe.car.capacity:
            return False
        
        return True
        

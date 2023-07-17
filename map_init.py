from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import numpy as np


class Map:
    def __init__(self, Q: float, car, initial_pheromones: float, header: str, car_num: int = None):
        self.Q = Q
        self.car: Vehicle = car
        self.initial_pheromones = initial_pheromones
        self.depot: City = None
        self.header = header
        self.cities = []
        self.requests = []
        self.pheromone_matrix: np.array = None
        self.distance_matrix: np.array = None
        self.inverse_distance: np.array = None
        self.best_path: list = None
        self.best_path_distance: float = None
        self.car_num = car_num
        self.best_route_car_num: int|float = None
        self.convergence = []
        
    def construct_distance_matrix(self):
        matrix = []
        inverse_matrix = []
        for city_1 in self.cities:
            row = []
            inverse_row = []
            for city_2 in self.cities:
                dist = city_1.distance(city_2)
                if dist == 0:
                    inverse_row.append(0)
                else:       
                    inverse_row.append(1 / dist)
                
                row.append(city_1.distance(city_2))
            inverse_matrix.append(inverse_row)
            matrix.append(row)

        self.distance_matrix = np.array(matrix)
        self.inverse_distance = np.array(inverse_matrix)
    
        return self

    def construct_pheromone_matrix(self):
        matrix = np.ones((len(self.cities), len(self.cities))) * self.initial_pheromones
        self.pheromone_matrix = matrix
        return self
    
    def update_pheromones_local(self, city_start, city_end):
        self.pheromone_matrix[city_start.index][city_end.index] = (1-self.Q) * self.pheromone_matrix[city_start.index][city_end.index] + \
                                                  self.Q * self.initial_pheromones

    def update_phermones_global(self, best_path, best_path_distance):

        self.pheromone_matrix = (1-self.Q) * self.pheromone_matrix

        current_city = best_path[0]
        for next_city in best_path[1:]:
            self.pheromone_matrix[current_city.index][next_city.index] += self.Q/best_path_distance
            current_city = next_city

    def update_best_path(self, path, convergence: list):
        self.best_path = path
        self.best_path_distance = round(self.calculate_path_distance(path), 2)
        self.convergence = convergence

    def insert(self, smt):
        if type(smt) == City:
            self.cities.append(smt)
        
        elif type(smt) == Request:
            self.requests.append(smt)
        
        else:
            raise TypeError

    def getting_cities(self, cities):
        for town, index in zip(cities, range(len(cities))):
            x = float(town.cx.contents[0])
            y = float(town.cy.contents[0])
            city = City(x, y, int(town.get('id')), town.get("type"), index)
            self.insert(city)

        try:    
            self.depot = self.cities[0]
        except IndexError:
            print("[getting_cities]: IndexError -> No cities given")

    def getting_requests(self, requests: list):
        for request, index in zip(requests, range(len(requests))):
            id = int(request.get('id'))
            node =  int(request.get('node'))
            quantity = float(request.quantity.contents[0])
            req = Request(id, node, quantity, index=index)
            self.insert(req)

    def match_cities_requests(self):
        for city in self.cities:
            for request in self.requests:
                if city.id == request.node:
                    city.request = request
                    break
            if city.request is None:
                city.request = Request(-1, -1, -1, index=-1)
        
        if self.car_num is None:
            self.car_num = len(self.cities)
    
    def calculate_path_distance(self, path: list) -> float:
        distance = 0
        for i in range(len(path)-1):
            distance += path[i].distance(path[i+1])
        
        return distance

    def show(self):
        sep = "----------------------------------------"
        print("Cities")
        print(sep)

        for city in self.cities:
            print(city)

        print(sep, end="\n")
        print("Requests")
        print(sep)

        for request in self.requests:
            print(request)
        
        print(sep)

    def plot_map(self):
        """ Add requests to the plot """
        fig = plt.figure()
        linspace_x = [city.position[0] for city in self.cities]
        linspace_y = [city.position[1] for city in self.cities]
        plt.scatter(linspace_x, linspace_y, marker="o")
        plt.title("Map of cities \n distance: {0:.2f}".format(self.best_path_distance))

        for city in self.cities:
            plt.annotate(city.id, 
                        city.position,
                        textcoords="offset points",
                        xytext=(0,6),
                        ha='center')
        if self.best_path:
            for i in range(len(self.best_path)-1):
                plt.plot([self.best_path[i].position[0], self.best_path[i+1].position[0]],
                         [self.best_path[i].position[1], self.best_path[i+1].position[1]],
                          color='r', linestyle='-', linewidth=2)
        fig.savefig(f"out/{self.header}.png")
    
    def plot_convergence(self):
        fig = plt.figure()
        plt.plot(self.convergence)
        plt.title(f"Convergence \n Best distance: {self.best_path_distance}")
        plt.xlabel("Iteration")
        plt.ylabel("Distance")
        fig.savefig(f"out/{self.header}_convergence.png")

class City:
    def __init__(self, x: float, y: float, id: int, depot: str, index: int):
        self.position = (x, y)  
        self.id = id  # what is a difference between this and id?
        self.type = depot
        self.index = index
        self.request: Request = None
        self.visited = False
    

    def __repr__(self) -> str:
        if self.type == '0':
            typ = "Depot"
        else:
            typ = "Customer"

        return f"""ID: {self.id}, X: {self.position[0]}, Y: {self.position[1]}, Type: {typ} """
    
    def distance(self, other) -> float:
        return np.sqrt((self.position[0]- other.position[0])**2 + (self.position[1]-other.position[1])**2)
    
    def change_visit(self):
        if self.visited:
            self.visited = False
        else:
            self.visited = True
    

class Request:
    def __init__(self, id: int, node, quantity: float, index) -> None:
        self.id = id
        self.node = node
        self.index = index
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"Id: {self.id}, City: {self.node}, Quantity: {self.quantity}"
    
    
class Fleet:
    def __init__(self):
        self.cars = []
    
    def insert_car(self, car):
        self.cars.append(car)

    def getting_cars(self, records):
        for record in  records:
            capacity = float(record.capacity.contents[0])
            arr = record.arrival_node.contents[0]
            dep = record.departure_node.contents[0]
            car = Vehicle(capacity, record.get('type'), arr, dep)
            
            self.insert_car(car)
    
    def show(self):
        print("Cars:")
        print("----------------------------------------")
        for car in self.cars:
            print(car)



class Vehicle:
    def __init__(self, capacity, typ, arrival_node, departure_node) -> None:
        self.capacity = capacity
        self.type = typ
        self.arrival_node = arrival_node
        self.departure_node = departure_node
    
    def __repr__(self) -> str:
        return f"Type: {self.type}, Departure: {self.departure_node}, Arrival: {self.arrival_node}, Capacity: {self.capacity}"
        


def initilize_map(filename: str, Q: float, initial_pheromones: float) -> tuple[Map, Fleet]:
    with open(filename, 'r') as f:
        data = f.read()

    Bs_data = bs(data, "xml")
    nodes = Bs_data.find_all('node')
    cars = Bs_data.find_all('vehicle_profile')
    requests = Bs_data.find_all('request')

    header = filename.split("/")[1].split(".")[0]

    init_fleet = Fleet()
    init_fleet.getting_cars(cars)
    init_map = Map(Q, init_fleet.cars[0], initial_pheromones, header)  # Need only one car, becuase I dont have more, should be adjusted...
    init_map.getting_cities(nodes)
    init_map.getting_requests(requests)
    init_map.match_cities_requests()
    init_map = init_map.construct_distance_matrix()
    init_map = init_map.construct_pheromone_matrix()

    return init_map, init_fleet


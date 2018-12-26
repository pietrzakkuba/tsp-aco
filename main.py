from math import sqrt
from random import randint
from numpy.random import choice
from plot import plot
from time import process_time


class Graph:
    def __init__(self, cost_matrix: list, vertices: int):
        self.matrix = cost_matrix
        self.vertices = vertices
        self.pheromone = [[1 / vertices ** 2 for _ in range(vertices)] for _ in range(vertices)]


class AntColony:
    def __init__(self, ant_number: int, iterations: int, alpha: float, beta: float, rho: float, q: float):
        self.ant_number = ant_number
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q

    def pheromone_evaporation_and_update(self, graph: Graph, ants: list):
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= 1 - self.rho
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_change[i][j]

    def run(self, graph: Graph):
        shortest_length = float("inf")
        shortest_path = []
        for iteration in range(self.iterations):
            ants = [Ant(self, graph) for _ in range(self.ant_number)]
            for ant in ants:
                for i in range(1, graph.vertices):
                    ant.next_city()
                ant.route += graph.matrix[ant.ant_was_there[-1]][ant.ant_was_there[0]]
                if ant.route < shortest_length:
                    shortest_path = ant.ant_was_there
                    shortest_length = ant.route
                ant.local_pheromone_change()
            self.pheromone_evaporation_and_update(graph, ants)
        return shortest_length, shortest_path


class Ant:
    def __init__(self, aco: AntColony, graph: Graph):
        self.aco = aco
        self.graph = graph
        self.route = 0.0
        self.pheromone_change = []
        self.ant_was_not_there = [i for i in range(graph.vertices)]
        self.attractiveness = [[0 if i == j else 1 / graph.matrix[i][j] for j in range(graph.vertices)] for i in range(graph.vertices)]
        self.first_city = randint(0, graph.vertices - 1)
        self.ant_was_there = [self.first_city]
        self.current = self.first_city
        self.ant_was_not_there.remove(self.first_city)

    def next_city(self):
        denominator = 0
        for i in self.ant_was_not_there:
            denominator += self.graph.pheromone[self.current][i] ** self.aco.alpha * self.attractiveness[self.current][i] ** self.aco.beta

        chances = [0 for _ in range(self.graph.vertices)]
        for i in range(self.graph.vertices):
            if i in self.ant_was_not_there:
                chances[i] = self.graph.pheromone[self.current][i] ** self.aco.alpha * self.attractiveness[self.current][i] ** self.aco.beta / denominator

        where_to_go = choice(self.graph.vertices, p=chances)
        self.ant_was_not_there.remove(where_to_go)
        self.ant_was_there.append(where_to_go)
        self.route += self.graph.matrix[self.current][where_to_go]
        self.current = where_to_go

    def local_pheromone_change(self):
        self.pheromone_change = [[0.0 for _ in range(self.graph.vertices)] for _ in range(self.graph.vertices)]
        for x in range(1, len(self.ant_was_there)):
            i = self.ant_was_there[x - 1]
            j = self.ant_was_there[x]
            self.pheromone_change[i][j] = self.pheromone_change[j][i] = self.aco.q / self.route


class City:
    def __init__(self, order_number: int, x: float, y: float):
        self.order_number = order_number
        self.x = x
        self.y = y

    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def main():
    cities = []
    points = []
    source = "att48.txt"
    with open(source, "r") as my_file:
        quantity = int(my_file.readline())
        for line in my_file:
            n = line.split(' ')
            cities.append(City(int(n[0]), float(n[1]), float(n[2])))
            points.append((float(n[1]), float(n[2])))
    paths_matrix = []

    for i in range(quantity):
        row = []
        for j in range(quantity):
            row.append(cities[i].dist(cities[j]))
        paths_matrix.append(row)
    ant_quantity = 100
    generations = 10
    alpha = 1
    beta = 5
    rho = 0.5
    q = 1
    colony = AntColony(ant_quantity, generations, alpha, beta, rho, q)
    my_map = Graph(paths_matrix, quantity)
    time_ = process_time()
    length, path = AntColony.run(colony, my_map)
    time_ = process_time() - time_
    print("Time:", time_)
    path.append(path[0])
    for i in range(len(path)):
        path[i] += 1
    print("Length:", length, "\nPath:", path)
    title = "Name: " + source[:-4] + "\nLength: " + str(length) + "\nants: " + str(ant_quantity) + " | gens: " + str(generations) + " | alpha: " + str(alpha) + " | beta: " + str(beta) + " | rho: " + str(rho) + " | q: " + str(q)
    plot(points, path, title)


if __name__ == '__main__':
    main()

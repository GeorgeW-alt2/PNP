import itertools
import multiprocessing
import random

# Function to generate a symmetric distance matrix for TSP
def generate_symmetric_distance_matrix(size):
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(0)  # Distance to self is 0
            elif i < j:
                dist = random.randint(1, 100)  # Random distance between 1 and 100
                row.append(dist)
            else:
                row.append(matrix[j][i])  # Ensure symmetry
        matrix.append(row)
    return matrix

# Generate a 20x20 symmetric distance matrix
distance_matrix = generate_symmetric_distance_matrix(20)

# City identifiers for 20 cities
cities = list(range(10))

def calculate_route_distance(route):
    """Calculate the total distance of the given route."""
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    total_distance += distance_matrix[route[-1]][route[0]]  # Return to the start
    return total_distance

def tsp_solver_worker(permutations_chunk):
    """Worker function to solve a part of the TSP problem."""
    best_distance = float('inf')
    best_route = None
    for route in permutations_chunk:
        current_distance = calculate_route_distance(route)
        if current_distance < best_distance:
            best_distance = current_distance
            best_route = route
    return best_distance, best_route

def divide_workload(data, num_chunks):
    """Divide data into chunks for multiprocessing."""
    chunk_size = len(data) // num_chunks
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

if __name__ == '__main__':
    num_agents = multiprocessing.cpu_count()  # Number of available agents
    all_permutations = list(itertools.permutations(cities))  # All possible routes

    # Divide the work among the available agents
    chunks = divide_workload(all_permutations, num_agents)

    with multiprocessing.Pool(num_agents) as pool:
        results = pool.map(tsp_solver_worker, chunks)

    # Find the overall best result from all workers
    best_distance = float('inf')
    best_route = None
    for distance, route in results:
        if distance < best_distance:
            best_distance = distance
            best_route = route

    print(f"Best route: {best_route}, Distance: {best_distance}")
    input()
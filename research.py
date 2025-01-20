import time
import tracemalloc
import matplotlib.pyplot as plt
from simulated_annealing import simulated_annealing
from tabu_search import TabuSearch
from two_opt import two_opt
from utils import generate_tour, tour_length, connect_beginning_to_end

def benchmark_algorithm(algorithm, *args, **kwargs):
    """
    Benchmarks the given algorithm in terms of execution time and memory usage.

    :param algorithm: The algorithm function to benchmark
    :param args: Positional arguments to pass to the algorithm
    :param kwargs: Keyword arguments to pass to the algorithm
    :return: Execution time and peak memory usage
    """
    start_time = time.time()
    tracemalloc.start()

    result = algorithm(*args, **kwargs)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    execution_time = time.time() - start_time

    return execution_time, peak / 1024, result  # Return time (s) and memory (KB)

def compare_algorithms(problem_sizes, iterations=5):
    """
    Compares the performance of simulated annealing, tabu search, and 2-opt on TSP instances of varying sizes.

    :param problem_sizes: List of problem sizes (number of cities)
    :param iterations: Number of iterations for repeatability
    """
    execution_times = {"Simulated Annealing": [], "Tabu Search": [], "2-Opt": []}
    memory_usages = {"Simulated Annealing": [], "Tabu Search": [], "2-Opt": []}
    tour_lengths = {"Simulated Annealing": [], "Tabu Search": [], "2-Opt": []}
    time_vs_length = {"Simulated Annealing": [], "Tabu Search": [], "2-Opt": []}
    memory_vs_length = {"Simulated Annealing": [], "Tabu Search": [], "2-Opt": []}

    for size in problem_sizes:
        avg_execution_times = {"Simulated Annealing": 0, "Tabu Search": 0, "2-Opt": 0}
        avg_memory_usages = {"Simulated Annealing": 0, "Tabu Search": 0, "2-Opt": 0}
        avg_tour_lengths = {"Simulated Annealing": 0, "Tabu Search": 0, "2-Opt": 0}

        for _ in range(iterations):
            tsp_problem = generate_tour(size, (0, 100), (0, 100))

            # Simulated Annealing
            sa_time, sa_memory, sa_result = benchmark_algorithm(simulated_annealing, tsp_problem, a=1.05)
            avg_execution_times["Simulated Annealing"] += sa_time
            avg_memory_usages["Simulated Annealing"] += sa_memory
            tour_len = tour_length(sa_result)
            avg_tour_lengths["Simulated Annealing"] += tour_len
            time_vs_length["Simulated Annealing"].append((tour_len, sa_time))
            memory_vs_length["Simulated Annealing"].append((tour_len, sa_memory))

            # Tabu Search
            tabu_search = TabuSearch(problem=tsp_problem)
            ts_time, ts_memory, ts_result = benchmark_algorithm(
                tabu_search.run, tabu_size=5, search_space_percent=20, aspiration_criteria=10, max_stuck_iterations=100, iterations=100
            )
            avg_execution_times["Tabu Search"] += ts_time
            avg_memory_usages["Tabu Search"] += ts_memory
            tour_len = tour_length(ts_result)
            avg_tour_lengths["Tabu Search"] += tour_len
            time_vs_length["Tabu Search"].append((tour_len, ts_time))
            memory_vs_length["Tabu Search"].append((tour_len, ts_memory))

            # 2-Opt
            opt_time, opt_memory, opt_result = benchmark_algorithm(two_opt, tsp_problem)
            avg_execution_times["2-Opt"] += opt_time
            avg_memory_usages["2-Opt"] += opt_memory
            tour_len = tour_length(opt_result)
            avg_tour_lengths["2-Opt"] += tour_len
            time_vs_length["2-Opt"].append((tour_len, opt_time))
            memory_vs_length["2-Opt"].append((tour_len, opt_memory))

        # Calculate averages
        for algorithm in avg_execution_times.keys():
            execution_times[algorithm].append(avg_execution_times[algorithm] / iterations)
            memory_usages[algorithm].append(avg_memory_usages[algorithm] / iterations)
            tour_lengths[algorithm].append(avg_tour_lengths[algorithm] / iterations)

    # Plot results
    plot_results(problem_sizes, execution_times, memory_usages, tour_lengths, time_vs_length, memory_vs_length)

def plot_results(problem_sizes, execution_times, memory_usages, tour_lengths, time_vs_length, memory_vs_length):
    """
    Plots the comparison of execution times, memory usage, and tour lengths for varying problem sizes.

    :param problem_sizes: List of problem sizes (number of cities)
    :param execution_times: Dictionary of execution times for each algorithm
    :param memory_usages: Dictionary of memory usages for each algorithm
    :param tour_lengths: Dictionary of tour lengths for each algorithm
    :param time_vs_length: Dictionary of time vs tour length for each algorithm
    :param memory_vs_length: Dictionary of memory vs tour length for each algorithm
    """
    # Execution Times
    plt.figure()
    for algorithm, times in execution_times.items():
        plt.plot(problem_sizes, times, marker='o', label=algorithm)
    plt.title("Execution Time Comparison")
    plt.xlabel("Problem Size (Number of Cities)")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.grid()
    plt.show()

    # Memory Usage
    plt.figure()
    for algorithm, memory in memory_usages.items():
        plt.plot(problem_sizes, memory, marker='o', label=algorithm)
    plt.title("Memory Usage Comparison")
    plt.xlabel("Problem Size (Number of Cities)")
    plt.ylabel("Memory (KB)")
    plt.legend()
    plt.grid()
    plt.show()

    # Tour Lengths
    plt.figure()
    for algorithm, lengths in tour_lengths.items():
        plt.plot(problem_sizes, lengths, marker='o', label=algorithm)
    plt.title("Tour Length Comparison")
    plt.xlabel("Problem Size (Number of Cities)")
    plt.ylabel("Tour Length")
    plt.legend()
    plt.grid()
    plt.show()

    # Time vs Tour Length
    plt.figure()
    for algorithm, data in time_vs_length.items():
        lengths, times = zip(*data)
        plt.scatter(lengths, times, label=algorithm)
    plt.title("Tour Length vs Execution Time")
    plt.xlabel("Tour Length")
    plt.ylabel("Execution Time (s)")
    plt.legend()
    plt.grid()
    plt.show()

    # Memory vs Tour Length
    plt.figure()
    for algorithm, data in memory_vs_length.items():
        lengths, memories = zip(*data)
        plt.scatter(lengths, memories, label=algorithm)
    plt.title("Tour Length vs Memory Usage")
    plt.xlabel("Tour Length")
    plt.ylabel("Memory Usage (KB)")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    problem_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    compare_algorithms(problem_sizes)

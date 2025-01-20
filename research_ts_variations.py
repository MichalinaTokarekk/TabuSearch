import matplotlib.pyplot as plt
from utils import generate_tour, tour_length
from tabu_search import TabuSearch

def compare_tabu_search_versions(problem_sizes, iterations=5):
    """
    Compares multiple configurations (versions) of Tabu Search on tour length.

    :param problem_sizes: List of problem sizes (number of cities)
    :param iterations: Number of iterations for repeatability
    """
    versions = {
        "Version 1": {"tabu_size": 5, "search_space_percent": 20, "aspiration_criteria": 10},
        "Version 2": {"tabu_size": 10, "search_space_percent": 15, "aspiration_criteria": 5},
        "Version 3": {"tabu_size": 15, "search_space_percent": 25, "aspiration_criteria": 15},
        "Version 4": {"tabu_size": 20, "search_space_percent": 30, "aspiration_criteria": 20},
    }

    results = {version: [] for version in versions.keys()}

    for size in problem_sizes:
        for version, params in versions.items():
            avg_tour_length = 0
            for _ in range(iterations):
                tsp_problem = generate_tour(size, (0, 100), (0, 100))
                tabu_search = TabuSearch(problem=tsp_problem)
                ts_result = tabu_search.run(
                    tabu_size=params["tabu_size"],
                    search_space_percent=params["search_space_percent"],
                    aspiration_criteria=params["aspiration_criteria"],
                    max_stuck_iterations=100,
                    iterations=100,
                )
                avg_tour_length += tour_length(ts_result)
            avg_tour_length /= iterations
            results[version].append(avg_tour_length)

    # Plot the results
    plot_tabu_search_versions(problem_sizes, results)

def plot_tabu_search_versions(problem_sizes, results):
    """
    Plots the comparison of multiple Tabu Search configurations (versions).

    :param problem_sizes: List of problem sizes (number of cities)
    :param results: Dictionary of results for each version with average tour lengths
    """
    plt.figure()
    for version, lengths in results.items():
        plt.plot(problem_sizes, lengths, marker='o', label=version)
    plt.title("Comparison of Tabu Search Versions on Tour Length")
    plt.xlabel("Problem Size (Number of Cities)")
    plt.ylabel("Average Tour Length")
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    problem_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    compare_tabu_search_versions(problem_sizes)

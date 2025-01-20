from tabu_search import TabuSearch
from utils import generate_tour


tour = generate_tour(50, x_range=(0,100), y_range=(0,100))

ts = TabuSearch(problem=tour)

result = ts.run(
    tabu_size=20,
    search_space_percent=30,
    aspiration_criteria=0.1,
    max_stuck_iterations=10,
    max_seconds=20,
)

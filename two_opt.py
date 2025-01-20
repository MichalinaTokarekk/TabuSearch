from utils import tour_length, connect_beginning_to_end


def two_opt(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    def swap(tour, i, k):
        new_tour = tour[:i] + tour[i : k + 1][::-1] + tour[k + 1 :]
        return new_tour

    current_tour = points
    improvement = True
    iteration = 0

    while improvement:
        improvement = False
        best_distance = tour_length(connect_beginning_to_end(current_tour))

        for i in range(1, len(points) - 1):
            for k in range(i + 1, len(points)):
                new_tour = swap(current_tour, i, k)
                new_distance = tour_length(connect_beginning_to_end(new_tour))

                if new_distance < best_distance:
                    current_tour = new_tour
                    best_distance = new_distance
                    improvement = True
        iteration += 1

    return connect_beginning_to_end(current_tour)

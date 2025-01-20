from random import randint, shuffle
import time

from utils import tour_length, connect_beginning_to_end


class TabuSearch:
    def __init__(self, *, problem: list[tuple[int, int]]) -> None:
        self.initial_solution = problem
        shuffle(self.initial_solution)

    def _tour_cost(self, solution: list[tuple[int, int]]) -> float:
        return tour_length(connect_beginning_to_end(solution))

    @staticmethod
    def _get_tour_options(
        tour: list[tuple[int, int]], search_space_percent: int, randomize: bool
    ) -> list[tuple[int, int]]:
        tour_options = []
        options_size = int((search_space_percent / 100) * len(tour))
        for _ in range(options_size):
            vertex_idx_1 = 0
            vertex_idx_2 = 0

            while vertex_idx_1 == vertex_idx_2:
                vertex_idx_1 = randint(1, len(tour) - 1)
                vertex_idx_2 = randint(1, len(tour) - 1)

            if vertex_idx_1 > vertex_idx_2:
                swap = vertex_idx_1
                vertex_idx_1 = vertex_idx_2
                vertex_idx_2 = swap

            neighborhood_tour = tour[vertex_idx_1:vertex_idx_2]
            new_neighborhood_tour = neighborhood_tour[::-1]

            if randomize:
                shuffle(new_neighborhood_tour)

            tour_option = (
                tour[:vertex_idx_1] + new_neighborhood_tour + tour[vertex_idx_2:]
            )
            tour_options.append(tour_option)

        return tour_options

    def run(
        self,
        *,
        tabu_size: int,
        search_space_percent: int,
        aspiration_criteria: float,
        max_stuck_iterations: int,
        iterations: int | None = None,
        max_seconds: int | None = None,
    ) -> list[int]:
        """
        Tabu size
            how bug the tabu list will be. If the size is exceeded
            the last item will be removed.

        Search space percent
            defines how many tour options will be checked during
            one iteration. If problem has size 100 and percent
            will be set to 20 the function will generate 20 new
            solutions.

        Aspiration criteria
            defines how much better a solution must be to escape
            tabu list. If best solution has cost of 120 and new
            solution has 100 their diferrence will be 20.
            Aspiration criteria defined as 0.1 will allow this
            new solution. 20 >= 0.1 * 120. Higher aspiration
            critieria will let lesser solutions out of tabu list.

        Max stuck iterations
            the program will randomize the tour option if there
            was no improvment after the number of max stuck iterations.
            This helps escaping local minimum.

        Iterations and max seconds
            Defines when program will stop. Only one condition
            can be set. Either the program can run for only 50 seconds
            or it can only run for 50 iterations. In either case
            the orher parameter must be set to None.

        """
        assert not (iterations and max_seconds)

        best_solution = self.initial_solution
        best_candidate = self.initial_solution
        tabu_list = [self.initial_solution]

        stuck_iterations = 0
        iteration = 0

        total_seconds = 0

        while self._is_condition_met(iterations, max_seconds, iteration, total_seconds):
            iteration += 1
            start = time.time()
            exceeded_stuck_limit = stuck_iterations >= max_stuck_iterations

            tour_options = self._get_tour_options(
                best_candidate,
                search_space_percent,
                exceeded_stuck_limit,
            )
            best_candidate = tour_options[0]

            for candidate in tour_options:
                candidate_tour_cost = self._tour_cost(candidate)
                best_candidate_tour_cost = self._tour_cost(best_candidate)

                is_candidate_better = candidate_tour_cost < best_candidate_tour_cost
                is_candidate_tabu = candidate in tabu_list

                difference = best_candidate_tour_cost - candidate_tour_cost

                does_tabu_candidate_meet_aspiration = (
                    difference >= (aspiration_criteria * best_candidate_tour_cost) / 100
                )
                can_tabu_candidate_aspire = (
                    does_tabu_candidate_meet_aspiration if is_candidate_tabu else False
                )

                if can_tabu_candidate_aspire or (
                    is_candidate_better and not is_candidate_tabu
                ):
                    best_candidate = candidate

                if can_tabu_candidate_aspire:
                    tabu_list.remove(best_candidate)

            best_candidate_tour_cost = self._tour_cost(best_candidate)
            best_solution_tour_cost = self._tour_cost(best_solution)

            is_best_candidate_better = (
                best_candidate_tour_cost < best_solution_tour_cost
            )

            if is_best_candidate_better:
                best_solution = best_candidate
                stuck_iterations = 0
            else:
                stuck_iterations += 1

            tabu_list.append(best_candidate)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            end = time.time()
            total_seconds += end - start

        return best_solution

    def _is_condition_met(
        self, max_iterations: int, max_seconds: int, iteration: int, total_seconds: int
    ):
        if max_iterations:
            return max_iterations >= iteration

        return max_seconds >= total_seconds

import time

import pandas as pd

from src.puzzle import Puzzle
from src.LDFS_search import limited_depth_first_search
from src.RBFS_search import recursive_best_first_search


ALGOS_LIST = ["RBFS", "LDFS"]
NUM_EXPERIMENTS = 10 # the number of experiments we take for each algorithm
NUM_RANDOM_MOVES = 10 # the number of random moves we will make to create initial_state
LDFS_LIMIT_DEPTH = 2 # the limit of depth for this algorithm

EXPER_EXECUT_LIMIT_TIME = 10 # minutes
EXPER_EXECUT_LIMIT_MEMORY = 512 # MB


results_df = pd.DataFrame(
    columns=[
        "exp_ii", "algorithm", "start_state",
        "end_state", "goal_state", "time",
        "generated_states", "max_states_in_memory"
    ]
)
results_df = results_df.set_index(["exp_ii", "algorithm"])


def repr_start_end_puzzle_states(start_state: list[int], end_state: list[int]):
    return str(start_state[0:3]) + '\t  \t' + str(end_state[0:3]) +\
        '\n'+str(start_state[3:6]) + '\t->\t' + str(end_state[3:6]) +\
        '\n'+str(start_state[6:9]) + '\t  \t' + str(end_state[6:9])


def main(exp_ii: int, initial_state: list[int]):
    for ALGO in ALGOS_LIST:

        Puzzle.num_of_instances = 0
        Puzzle.max_states_in_memory = 0
        t0 = time.time()
        print(f"exp № {exp_ii}")

        if ALGO == "RBFS":
            END_STATE = recursive_best_first_search(initial_state=initial_state)
        elif ALGO == "LDFS":
            END_STATE = limited_depth_first_search(initial_state=initial_state, limit=LDFS_LIMIT_DEPTH)

        t1 = round(time.time() - t0, 5)

        # region data append
        if END_STATE is None:
            results_df.loc[(exp_ii, ALGO), :] = [
                ''.join(map(str, initial_state)), None,
                ''.join(map(str, Puzzle.goal_state)), t1, Puzzle.num_of_instances,
                Puzzle.max_states_in_memory
            ]
        else:
            results_df.loc[(exp_ii, ALGO), :] = [
                ''.join(map(str, initial_state)), ''.join(map(str, END_STATE.state)),
                ''.join(map(str, Puzzle.goal_state)), t1, Puzzle.num_of_instances,
                Puzzle.max_states_in_memory
            ]
        # endregion
        
        # region print
        if END_STATE is None:
            print("due to the depth limit, the solution wasn't found")
        else:
            print(f"initial_state\t->\tend_state\n{repr_start_end_puzzle_states(initial_state, END_STATE.state)}")
            print(f"{ALGO}: {END_STATE.find_solution()}")
        print(f"amount of total generated instances: {Puzzle.num_of_instances}")
        print(f"amount of max states in memory: {Puzzle.max_states_in_memory}")
        print(f"spent time: {t1:2f}")
        print()

        print('------------------------------------------')

        # endregion


if __name__ == "__main__":
    for exp_ii in range(NUM_EXPERIMENTS):
        initial_state: list[int] = Puzzle.create_initial_state(num_random_moves=NUM_RANDOM_MOVES)
        main(exp_ii=exp_ii, initial_state=initial_state)
    
    print(results_df, "\n")

    avg_time = results_df.groupby(level='algorithm')['time'].mean()
    avg_generated_states = results_df.groupby(level='algorithm')['generated_states'].mean()
    avg_max_states_in_memory = results_df.groupby(level='algorithm')['max_states_in_memory'].mean()

    print(f"avg_time:\n{avg_time}\n")
    print(f"avg_generated_states:\n{avg_generated_states}\n")
    print(f"avg_max_states_in_memory:\n{avg_max_states_in_memory}\n")


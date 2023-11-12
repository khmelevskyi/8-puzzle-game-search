import time
from sys import maxsize

import psutil

from src.puzzle import Puzzle


def memory_limit_exceeded(memory_limit_mb):
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    return memory_usage > memory_limit_mb


def recursive_best_first_search(initial_state: list[int], time_limit: int = 10, memory_limit_mb: int = 512) -> Puzzle:
    start_time = time.time()

    def RBFS_search(node: Puzzle, f_limit: int) -> 'tuple[Puzzle|None, int|None]':
        successors: list = []

        if time.time() - start_time > time_limit or memory_limit_exceeded(memory_limit_mb):
            return None, maxsize

        if node.goal_test():
            return node, None
        children: list[Puzzle] = node.generate_child()
        if not len(children):
            return None, maxsize
        count = -1
        for child in children:
            count += 1
            successors.append((child.evaluation_function, count, child))
        while len(successors):
            successors.sort()
            best_node: Puzzle = successors[0][2]
            
            if best_node.evaluation_function > f_limit:
                return None, best_node.evaluation_function
            alternative: int = successors[1][0]
            result, best_node.evaluation_function = RBFS_search( best_node, min(f_limit, alternative) )
            successors[0]=(best_node.evaluation_function,successors[0][1],best_node)
            if result != None:
                break
        return result, None


    node, f_limit = RBFS_search(Puzzle(initial_state=initial_state, parent=None, action=None, path_cost=0, needs_hueristic=True), f_limit=maxsize)
    return node


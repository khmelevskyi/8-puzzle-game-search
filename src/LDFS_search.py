import time

import psutil

from src.puzzle import Puzzle


def memory_limit_exceeded(memory_limit_mb):
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    return memory_usage > memory_limit_mb

def limited_depth_first_search(initial_state: list, depth_limit: int, time_limit: int = 10, memory_limit_mb: int = 512) -> Puzzle:
    start_time = time.time()
    
    def LDFS_search(node: Puzzle, depth_limit: int) -> 'Puzzle|None':

        if time.time() - start_time > time_limit or memory_limit_exceeded(memory_limit_mb):
            return None
        
        if node.goal_test():
            return node
        elif depth_limit == 0:
            return None
        else:
            children = node.generate_child() # or successors
            for child in children:
                result = LDFS_search(child, depth_limit - 1)
                if result is not None:
                    return result
            return None

    node = LDFS_search(Puzzle(initial_state, parent=None, action=None, path_cost=0, needs_hueristic=True), depth_limit)
    return node




import psutil

from puzzle import Puzzle


def memory_limit_exceeded(memory_limit_mb):
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    return memory_usage > memory_limit_mb

def limited_depth_first_search(initial_state: list, limit: int) -> Puzzle:
    
    def LDFS_search(node: Puzzle, limit: int) -> 'Puzzle|None':
        if node.goal_test():
            return node
        elif limit == 0:
            return None
        else:
            children = node.generate_child() # or successors
            for child in children:
                result = LDFS_search(child, limit - 1)
                if result is not None:
                    return result
            return None

    node = LDFS_search(Puzzle(initial_state, parent=None, action=None, path_cost=0, needs_hueristic=True), limit)
    return node




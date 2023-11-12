import random


class Puzzle:
    goal_state: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    heuristic: int = None
    evaluation_function: int = None
    needs_hueristic: bool = False
    num_of_instances: int = 0
    max_states_in_memory: int = 0

    def __init__(self, initial_state: list[int], parent: 'Puzzle|None', action: str, path_cost: int, needs_hueristic: bool = False):
        self.parent: 'Puzzle|None' = parent
        self.state: list[int] = initial_state
        self.action: str=action
        if parent:
            self.path_cost: int = parent.path_cost + path_cost
        else:
            self.path_cost: int = path_cost
        if needs_hueristic:
            self.needs_hueristic: bool = True
            self.generate_heuristic()
            self.evaluation_function=self.heuristic+self.path_cost
        Puzzle.num_of_instances+=1

    def __str__(self):
        return str(self.state[0:3])+'\n'+str(self.state[3:6])+'\n'+str(self.state[6:9])

    def generate_heuristic(self) -> None:
        # region heuristic function with distance
        # self.heuristic=0
        # for num in range(1,9):
        #     distance=abs(self.state.index(num) - self.goal_state.index(num))
        #     i=int(distance/3)
        #     j=int(distance%3)
        #     self.heuristic=self.heuristic+i+j
        # endregion

        self.heuristic = 0
        for i in range(9):
            if self.state[i] != self.goal_state[i]:
                self.heuristic += 1

    def goal_test(self) -> bool:
        if self.state == self.goal_state:
            return True
        return False

    @staticmethod
    def find_legal_actions(i, j) -> list[str]:
        """
        This function finds possible moves for blank space
        """
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0:  # up is disable
            legal_action.remove('U')
        elif i == 2:  # down is disable
            legal_action.remove('D')
        if j == 0:
            legal_action.remove('L')
        elif j == 2:
            legal_action.remove('R')
        return legal_action

    def generate_child(self) -> list:
        """
        This function generates children (successors) possible states of the current state
        """
        children=[]
        x = self.state.index(0)
        i = int(x / 3) # find index by row
        j = int(x % 3) # find index by column
        legal_actions=self.find_legal_actions(i, j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action == 'U':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action == 'D':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action == 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action == 'R':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(initial_state=new_state, parent=self, action=action, path_cost=1, needs_hueristic=self.needs_hueristic))

            # print(children)
            Puzzle.max_states_in_memory = max(len(children), Puzzle.max_states_in_memory)

        return children

    @staticmethod
    def create_initial_state(num_random_moves: int) -> list[int]:
        """
        This function creates an initial state by moving the blank space
        in randomised order for specific amount of moves
        """
        initial_state = Puzzle.goal_state.copy()
        x = initial_state.index(0)
        i, j = int(x / 3), x % 3

        for _ in range(num_random_moves):
            legal_actions = Puzzle.find_legal_actions(i, j)
            action = random.choice(legal_actions)

            if action == 'U':
                initial_state[x], initial_state[x - 3] = initial_state[x - 3], initial_state[x]
                i -= 1
            elif action == 'D':
                initial_state[x], initial_state[x + 3] = initial_state[x + 3], initial_state[x]
                i += 1
            elif action == 'L':
                initial_state[x], initial_state[x - 1] = initial_state[x - 1], initial_state[x]
                j -= 1
            elif action == 'R':
                initial_state[x], initial_state[x + 1] = initial_state[x + 1], initial_state[x]
                j += 1

            x = i * 3 + j

        return initial_state

    def find_solution(self) -> list[str]:
        """
        This function finds solution for 8-puzzle by going through parent nodes
        and appending the actions. Then reverse the order of actions
        """
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution

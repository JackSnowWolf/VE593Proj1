import random
import math


def BFS(Graph, initialState):
    """
     Breadth-First Search
    :param Graph: simple graph for the problem to be solved
    :param initialState: initial state of condition
    :return: a tuple of list of path and corresponding cost
    """
    queue = [initialState]
    # queue_t = {}
    # queue_t[initialState] = 0
    # queue_t is a dict for convenience to check the status.
    # please ensure the memory is enough
    marked_state = {}
    parents = {}
    while len(queue) != 0:
        # tmp_queue = list(queue.items())
        # tmp_queue.sort(key=_take_cost)
        # curr_state, _ = tmp_queue[0]
        # queue.pop(curr_state)
        curr_state = queue[0]
        # queue_t.pop(curr_state)
        del queue[0]
        if Graph.isGoal(curr_state):
            path = path_helper(parents, initialState, curr_state)
            return (path, len(path) - 1)
        marked_state[curr_state] = 1
        for next_state in Graph.successors(curr_state):
            if next_state not in marked_state and next_state not in parents:
                queue.append(next_state)
                # queue_t[next_state] = 1
                # i = i + 1
                parents[next_state] = curr_state


def path_helper(parents, initialState, finalState):
    """
    :param parents: a dict for storing parent-child relationship. key is child and parents is value
    :param initialState: initial state
    :param finalState: final state
    :return: the path from inital state to the final state based on parents
    """
    path = [finalState]
    curr_state = finalState
    while curr_state != initialState:
        curr_state = parents[curr_state]
        path.append(curr_state)
    path.reverse()
    return path


def _take_length(state):
    """
    helper function for sorting
    """
    return state[0]


def _take_cost(state):
    """
    helper function for sorting
    """
    return state[1]


def UCS(ValuedGraph, initialState):
    """
    Uniform-Cost Search
    :param ValuedGraph: valued graph for problem to be solved
    :param initialState: initial state
    :return: a tuple of list of path and corresponding cost
    """
    queue = {}
    queue[initialState] = 0
    marked_state = {}
    parents = {}
    while len(queue) != 0:
        tmp_queue = list(queue.items())
        tmp_queue.sort(key=_take_cost)
        prev_state, prev_cost = tmp_queue[0]
        queue.pop(prev_state)
        if ValuedGraph.isGoal(prev_state):
            path = path_helper(parents, initialState, prev_state)
            return (path, prev_cost)
        marked_state[prev_state] = 1
        for cost, next_state in ValuedGraph.successors(prev_state):
            if next_state not in marked_state and next_state not in queue:
                queue[next_state] = cost + prev_cost
                parents[next_state] = prev_state


def DFS(Graph, initialState):
    """
    Depth-First Search
    Notice that I use a trick here. I use the popitem function to get the last item of dict,
    which is much faster than other data structure
    :param Graph: simple graph for problem to be solved
    :param initialState: initial state
    :return: a tuple of list of path and corresponding cost
    """
    queue = {}
    queue[initialState] = 1
    # i = 1
    marked_state = {}
    parents = {}
    while len(queue) != 0:
        # tmp_queue = list(queue.items())
        # tmp_queue.sort(key=_take_cost)
        # curr_state, _ = tmp_queue[-1]
        # queue.pop(curr_state)
        curr_state, _ = queue.popitem()
        # use this function may let the function run faster, but not guarantee the correctness of DFS
        if Graph.isGoal(curr_state):
            path = path_helper(parents, initialState, curr_state)
            return (path, len(path) - 1)
        marked_state[curr_state] = 1
        for next_state in Graph.successors(curr_state):
            if next_state not in marked_state and next_state not in queue:
                queue[next_state] = 1
                # i = i + 1
                parents[next_state] = curr_state


def DLS(Graph, initialState, depthLimit):
    """
    Depth-Limited Search
    :param Graph: simple graph for problem to be solved
    :param initialState: initial state
    :param depthLimit: the depth limit of the search
    :return: if cutoff, return "cutoff";else if failure, return "failure";
             else return a tuple of list of path and corresponding cost
    """
    marked_state = {}
    marked_state[initialState] = 1
    result = DLS_helper(Graph, initialState, depthLimit, marked_state)
    if result == "cutoff":
        return "cutoff"
    elif result == "failure":
        return "failure"
    else:
        result.reverse()
        return (result, len(result) - 1)


def DLS_helper(Graph, State, depthLimit, marked_states):
    """
    Depth-Limited Search helper function for recursive
    :param Graph: simple graph for problem to be solved
    :param State: current state
    :param depthLimit: current depth limit
    :param marked_states: a dict of visited states
    :return: if cutoff, return "cutoff";else if failure, return "failure";
             else return a tuple of list of path and corresponding cost
    """
    cutoff_occured = False
    if Graph.isGoal(State):
        return [State]
    elif 0 == depthLimit:
        return "cutoff"
    else:
        for node in Graph.successors(State):
            if node in marked_states:
                continue
            marked_states[node] = 1
            result = DLS_helper(Graph, node, depthLimit - 1, marked_states)
            if result == "cutoff":
                cutoff_occured = True
            elif result != "failure":
                result.append(State)

                return result
    if cutoff_occured == True:
        return "cutoff"
    else:
        return "failure"


def IDS(Graph, initialState):
    """
    Iterative Deepening Search
    :param Graph: simple graph for problem to be solved
    :param initialState: initial state
    :return: a tuple of list of path and corresponding cost
    """
    i = 0
    while 1:
        result = DLS(Graph, initialState, i)
        if result == "cutoff":
            i = i + 1
            if i > 10000:
                return "failure"
            continue
        elif result == "failure":
            return "failure"
        else:
            return result


def Astar(ValuedGraph, initialState, heuristic):
    """
    A* Search Search
    :param ValuedGraph: valued graph for problem to be solved
    :param initialState: initial state
    :param heuristic: heuristic function, which could get a cost if pass a state into it
    :return: a tuple of list of path and corresponding cost
    """
    queue = [(0, initialState)]
    marked_state = {}
    parents = {}
    while len(queue) != 0:
        curr_state = queue[0]
        del queue[0]
        # tmp_queue = list(queue.items())
        # tmp_queue.sort(key=_take_cost)
        # curr_state, _ = tmp_queue[-1]
        # queue.pop(curr_state)
        if ValuedGraph.isGoal(curr_state[1]):
            path = path_helper(parents, initialState, curr_state[1])
            return (path, curr_state[0])
        marked_state[curr_state[1]] = 1
        for _, next_state in ValuedGraph.successors(curr_state[1]):
            if next_state not in marked_state and next_state not in parents:
                queue.append((curr_state[0] + heuristic(next_state), next_state))
                parents[next_state] = curr_state[1]
        queue.sort(key=_take_length)


beta = 1.5


def MCTS(ValuedGraph, state, budget):
    """
    Monte Carlo Tree Search method
    :param ValuedGraph: valued graph for problem to be solved
    :param initialState: initial state
    :param budget: the times of loops, which should be large enough to solve the problem,
                   otherwise, it will assert a error
    :return: a tuple of list of path and corresponding cost
    """
    queue = {}
    queue[state] = (0, 0)
    pre_state = state
    adj_state = []
    for (_, j) in ValuedGraph.successors(state):
        adj_state.append(j)
    marked_state = [state]
    parents = []
    num = 0
    continue_flag = 0
    while num <= budget:
        # TreePolicy
        while 1:
            if len(adj_state) != 0:
                curr_state = adj_state[0]
                queue[curr_state] = (0, 0)
                parents.append((pre_state, curr_state))
                marked_state.append(curr_state)
                del adj_state[0]
                break
            else:
                pre_state = state
                while len(adj_state) == 0:
                    list_tmp = []
                    log_pre_value_n = math.log(queue[pre_state][0])
                    for state_t in MCTS_findchild(pre_state, parents):
                        state_value = queue[state_t]
                        assert state_value[0] != 0
                        state_pair = (
                            state_value[1] / state_value[0] + beta * math.sqrt(2 * log_pre_value_n / state_value[0]),
                            state_t)
                        list_tmp.append(state_pair)
                    if len(list_tmp) == 0:
                        num += 1
                        continue_flag = 1
                        break
                    list_tmp.sort(key=_take_length)
                    pre_state = list_tmp[-1][1]
                    adj_state = []
                    for i in ValuedGraph.successors(pre_state):
                        if i[1] not in marked_state:
                            adj_state.append(i[1])
                    if ValuedGraph.isGoal(pre_state):
                        num += 1
                        del list_tmp[:]
                        continue_flag = 1
                        break

                    del list_tmp[:]
                if continue_flag == 1:
                    break
        if continue_flag == 1:
            continue_flag = 0
            continue
        # roll out
        cost = MCTS_rollout(ValuedGraph, curr_state)

        # back up
        (n, Q) = queue[curr_state]
        queue[curr_state] = (n + 1, Q + cost)
        parent = MCTS_findparent(curr_state, parents)
        while parent != state:
            (n, Q) = queue[parent]
            queue[parent] = (n + 1, Q + cost)
            parent = MCTS_findparent(parent, parents)
        (n, Q) = queue[state]
        queue[state] = (n + 1, Q + cost)

        num += 1

    sort_child = []
    for (i, j) in ValuedGraph.successors(state):
        assert queue[j][1] != None
        sort_child.append((queue[j][1], j, i))
    sort_child.sort(reverse=True)
    return (sort_child[0][2], sort_child[0][1])


def MCTS_findchild(pre_state, parents):
    result = []
    for (i, j) in parents:
        if pre_state == i:
            result.append(j)
    return result


def MCTS_findparent(curr_state, parents):
    for (i, j) in parents:
        if curr_state == j:
            return i


def MCTS_rollout(ValuedGraph, initialState):
    prev_state = (0, initialState)
    # queue = [prev_state]
    while 1:
        if ValuedGraph.isGoal(prev_state[1]):
            return prev_state[0]
        next_list = ValuedGraph.successors(prev_state[1])
        next_state = next_list[random.randint(0, len(next_list)) - 1]
        prev_state = (next_state[0] + prev_state[0], next_state[1])

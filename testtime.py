from testgraphs import *
from search import *
from optparse import OptionParser
import time

parser = OptionParser()
parser.add_option("-n", "--nPuzzleGraph_Length", action="store",
                  dest="nPuzzleGraph_Length",
                  default=3,
                  help="set nPuzzle Graph length")
parser.add_option("--BFS", action="store_true",
                  dest="BFS",
                  default=False,
                  help="choose Breadth-First Search method")
parser.add_option("--UCS", action="store_true",
                  dest="UCS",
                  default=False,
                  help="choose Uniform-Cost Search method")
parser.add_option("--DFS", action="store_true",
                  dest="DFS",
                  default=False,
                  help="choose Depth-First Search method")
parser.add_option("--DLS", action="store_true",
                  dest="DLS",
                  default=False,
                  help="choose Depth-Limited Search method")
parser.add_option("--IDS", action="store_true",
                  dest="IDS",
                  default=False,
                  help="choose Iterative Deepening Search method")
parser.add_option("--Astar", action="store_true",
                  dest="Astar",
                  default=True,
                  help="choose A* Search Search method")
parser.add_option("--MCTS", action="store_true",
                  dest="MCTS",
                  default=False,
                  help="choose Monte Carlo Tree Search method")

options, _ = parser.parse_args()

nPuzzleGraph_Length = int(options.nPuzzleGraph_Length)
goal_state = list(range(1, nPuzzleGraph_Length ** 2)) + [0]

# options analysis
search_method = []
if options.BFS:
    search_method.append(("Breadth-First Search", BFS))
if options.UCS:
    search_method.append(("Uniform-Cost Search", UCS))
if options.DFS:
    search_method.append(("Depth-First Search", DFS))
if options.DLS:
    search_method.append(("Depth-Limited Search", DLS))
if options.IDS:
    search_method.append(("Iterative Deepening Search", IDS))
if options.Astar:
    search_method.append(("A* Search", Astar))
if options.MCTS:
    search_method.append(("Monte Carlo Tree Search", MCTS))


def nPuzzleGraph_heurisitc(state):
    cost = 0
    for i in range(nPuzzleGraph_Length ** 2):
        final_state_index = (i + nPuzzleGraph_Length ** 2 - 1)\
                            % (nPuzzleGraph_Length ** 2)
        index_x = final_state_index \
                  % nPuzzleGraph_Length
        index_y = int(final_state_index / nPuzzleGraph_Length)
        x = state.value.index(i) % nPuzzleGraph_Length
        y = int(state.value.index(i) / nPuzzleGraph_Length)
        cost = cost + (index_x - x) ** 2 + (index_y - y) ** 2
    return cost


# my nPuzzle graph for different length n
class my_nPuzzleGraph(nPuzzleGraph):
    def isGoal(self, state):
        return state.value == goal_state


# my nPuzzle valued graph for different length n
class nPuzzleValuedGraph(my_nPuzzleGraph):
    def successors(self, state):
        succs = []
        if (state.blankPosition % self.n != 0):
            succs.append((nPuzzleGraph_heurisitc(state), self.succ(state, Action.LEFT)))
        if (state.blankPosition >= self.n):
            succs.append((nPuzzleGraph_heurisitc(state), self.succ(state, Action.UP)))
        if (state.blankPosition % self.n != self.n - 1):
            succs.append((nPuzzleGraph_heurisitc(state), self.succ(state, Action.RIGHT)))
        if (state.blankPosition < self.n * (self.n - 1)):
            succs.append((nPuzzleGraph_heurisitc(state), self.succ(state, Action.DOWN)))
        return succs


# check the inversions in the generated list
def check_inversions(ls):
    count = 0
    length = len(ls)
    for i in range(0, len(ls) - 1):
        if ls[i] == 0:
            continue
        for j in range(i + 1, length):
            if ls[j] == 0:
                continue
            if ls[i] > ls[j]:
                count = count + 1
    return count


# return a solvable nPuzzle graph
def generate_nPuzzle():
    assert nPuzzleGraph_Length % 2 == 1
    ls = list(range(nPuzzleGraph_Length ** 2))
    random.shuffle(ls)
    while check_inversions(ls) % 2 == 1:
        random.shuffle(ls)
    return State(ls)


# main function
if __name__ == "__main__":

    total_time = [float(0) for _ in range(len(search_method))]

    for i in range(5):
        nPuzzle_init = generate_nPuzzle()
        print("testcase %d:" % (i + 1), flush=True)
        print(nPuzzle_init.value, flush=True)
        my_simple_nPuzzle = my_nPuzzleGraph(nPuzzleGraph_Length)
        my_valued_nPuzzle = nPuzzleValuedGraph(nPuzzleGraph_Length)
        for j in range(len(search_method)):
            name = search_method[j][0]
            start_time = time.time()
            if name == "Breadth-First Search":
                BFS(my_simple_nPuzzle, nPuzzle_init)
            elif name == "Uniform-Cost Search":
                UCS(my_valued_nPuzzle, nPuzzle_init)
            elif name == "Depth-First Search":
                DFS(my_simple_nPuzzle, nPuzzle_init)
            elif name == "Depth-Limited Search":
                # result = DLS(my_simple_nPuzzle, nPuzzle_init, 100)
                continue
            elif name == "Iterative Deepening Search":
                IDS(my_simple_nPuzzle, nPuzzle_init)
            elif name == "A* Search":
                Astar(my_valued_nPuzzle, nPuzzle_init, nPuzzleGraph_heurisitc)
            elif name == "Monte Carlo Tree Search":
                # MCTS(my_valued_nPuzzle,nPuzzle_init, 100)
                continue
            running_time = time.time() - start_time
            print("%s times %d" % (search_method[j][0], i + 1), flush=True)
            print("running time: %.2f seconds\n" % running_time, flush=True)
            total_time[j] = total_time[j] + running_time

    average_time = [t / 5 for t in total_time]
    for j in range(len(search_method)):
        if average_time[j] == 0:
            continue
        print("%s: " % search_method[j][0])
        print("average cost time: %.2f seconds\n " % average_time[j])

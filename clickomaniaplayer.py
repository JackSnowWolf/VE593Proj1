import random
from search import *
from clickomania import *
from optparse import OptionParser


def my_parser():
    """
    analysis arguments
    :return: N, M, K, budget
    """
    parser = OptionParser()
    parser.add_option("-n", "-N", action="store",
                      dest="N",
                      default=6,
                      help="set height of clickomania")
    parser.add_option("-m", "-M", action="store",
                      dest="M",
                      default=9,
                      help="set weight of clickomania")
    parser.add_option("-k", "-K", action="store",
                      dest="K",
                      default=4,
                      help="set types of cell in clckomania")
    parser.add_option("-b", "--budget", action="store",
                      dest="budget",
                      default=1000,
                      help="set budget of MCTS")
    options, _ = parser.parse_args()
    return int(options.N), int(options.M), int(options.K), int(options.budget)


def generate_clickomania_initalstate(N, M, K):
    """
    generate clickomania inital state
    :param N: height
    :param M: width
    :param K: types
    :return: a clickomania type inital state
    """
    graph = []
    for i in range(N * M):
        graph.append(random.randint(1, K))
    return cState(graph)


def clickomania_print(state, score, N, M, step):
    """
    print clickomania for output
    :param state: current state
    :param score: the score for this step
    :param N: height
    :param M: width
    :param step: step number
    :return: None
    """
    print("step %d" % step)
    print("step score: %d\nstate:" % score)
    for i in range(N):
        print(state.value[i * M:(i + 1) * M])
    print("\n")


def test():
    N, M, K, budget = my_parser()

    next_state = generate_clickomania_initalstate(N, M, K)
    # next_state = cState([5, 3, 5, 6, 6, 2, 2, 2, 6, 3, 3, 4, 2, 5, 2, 6, 2, 5, 1, 1, 3, 4, 2, 2, 6, 2, 1, 2, 3, 2, 5, 5, 4, 4, 1, 1, 3, 4, 1, 6, 2, 5, 2, 3, 6, 1, 2, 6, 6, 4, 1, 1, 4, 4, 6, 3, 3, 3, 3, 3, 6, 6, 1])

    clickomania_print(next_state, 0, N, M, 0)
    myclickonmania = Clickomania(N, M, K)
    total_score = 0
    # the budget should be increased if the size become larger
    # if budget is too small to solve the problem, it will throw a error
    step = 1
    while 1:
        score, next_state = MCTS(myclickonmania, next_state, budget)
        # next_state = MCTS(myclickonmania, cState([2, 1, 2, 3, 1, 1, 3, 1, 3, 2, 3, 3]), 10)
        # next_state = MCTS(myclickonmania, cState([2,1,2,1,3,3,2,3,3]), 10)
        clickomania_print(next_state, score, N, M, step)
        step = step + 1
        total_score = score + total_score
        if myclickonmania.isGoal(next_state):
            print("final score: %d" % total_score)
            break
    return


if __name__ == "__main__":
    test()

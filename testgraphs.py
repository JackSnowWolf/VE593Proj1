#!/bin/python


class SimpleGraph:
    """Simple graph for testing."""

    def __init__(self):
        return

    def successors(self, state):
        if state == 0: return [1, 2]
        if state == 1: return [2, 3, 4]
        if state == 2: return [4]
        if state == 3: return [5]
        if state == 4: return [3, 5]
        if state == 5: return []

    def isGoal(self, state):
        return state == 5


class SimpleValuedGraph:
    """Simple valued graph for testing."""

    def __init__(self):
        return

    def successors(self, state):
        if state == 0: return [(2, 1), (3, 2)]
        if state == 1: return [(2, 2), (5, 3), (1, 4)]
        if state == 2: return [(1, 4)]
        if state == 3: return [(2, 5)]
        if state == 4: return [(2, 3), (1, 5)]
        if state == 5: return []

    def isGoal(self, state):
        return state == 5


class State:
    """State for nPuzzle graph that stores the position of the blank."""

    def __init__(self, v):
        self.value = v
        self.blankPosition = v.index(0)

    def clone(self):
        return State(list(self.value))

    def __repr__(self):
        """Converts an instance in string.

           Useful for debug or with print(state)."""
        return str(self.value)

    def __eq__(self, other):
        """Overrides the default implementation of the equality operator."""
        if isinstance(other, State):
            return self.value == other.value
        elif other == None:
            return False
        return NotImplemented

    def __hash__(self):
        """Returns a hash of an instance.

           Useful when storing in some data structures."""
        return hash(str(self.value))


class Action:
    """Feasible actions for nPuzzle graph and their effects."""

    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    shift = [-1, -3, 1, 3]  # Initilalized for n=3, can be overwritten for other n

    @classmethod  # specifies that update is a class (not instance) method
    def update(cls, n):
        cls.shift[Action.UP] = -n
        cls.shift[Action.DOWN] = n


class nPuzzleGraph:
    """nPuzzle graph based on State and Action."""

    def __init__(self, n):
        self.n = n
        Action.update(n)

    def setInitialState(self, initialState):
        self.initialState = initialState

    def succ(self, state, action):
        nextState = state.clone()
        shift = Action.shift[action]
        blankPosition = nextState.blankPosition
        nextState.value[blankPosition] = nextState.value[blankPosition + shift]
        blankPosition += shift
        nextState.value[blankPosition] = 0
        nextState.blankPosition = blankPosition

        return nextState

    def successors(self, state):
        succs = []
        if (state.blankPosition % self.n != 0):
            succs.append(self.succ(state, Action.LEFT))
        if (state.blankPosition >= self.n):
            succs.append(self.succ(state, Action.UP))
        if (state.blankPosition % self.n != self.n - 1):
            succs.append(self.succ(state, Action.RIGHT))
        if (state.blankPosition < self.n * (self.n - 1)):
            succs.append(self.succ(state, Action.DOWN))
        return succs

    def isGoal(self, state):
        return state.value == [1, 2, 3, 4, 5, 6, 7, 8, 0]

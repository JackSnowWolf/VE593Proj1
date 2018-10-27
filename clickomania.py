class cState:
    """State for Clickomania graph."""

    def __init__(self, v):
        self.value = v
        self.IsFinal = False

    def clone(self):
        return cState(list(self.value))

    def __repr__(self):
        """Converts an instance in string.

           Useful for debug or with print(state)."""
        return str(self.value)

    def __eq__(self, other):
        """Overrides the default implementation of the equality operator."""
        if isinstance(other, cState):
            return self.value == other.value
        elif other == None:
            return False
        return NotImplemented

    def __hash__(self):
        """Returns a hash of an instance.

           Useful when storing in some data structures."""
        return hash(str(self.value))

    def __gt__(self, other):
        """Overrides the default implementation of the greater-than operator."""
        if isinstance(other, cState):
            return self
        elif other == None:
            return False
        return NotImplemented

    def __lt__(self, other):
        """Overrides the default implementation of the less-than operator."""
        if isinstance(other, cState):
            return self
        elif other == None:
            return False
        return NotImplemented


class Clickomania:
    """Clickomania valued graph based on State."""

    def __init__(self, N, M, K):
        """N for height, M for width """
        self.N = N
        self.M = M
        self.K = K
        self.isPenalty = False

    def setInitialState(self, initialState):
        self.initialState = initialState

    def pos_tr(self, pos):
        """
        This function is to help to convert 2D location to one dimension
        :param pos: the position of selected cell
        :return the position of the cell in the list
        """
        assert len(pos) == 2 and pos[0] < self.N and pos[1] < self.M
        return pos[0] * self.M + pos[1]

    def choose(self, pos, state):
        """
        This function is to select same color based on clickomania rule
        :param pos: the position of selected cell
        :param state: current clickomania
        :return a list of 0 and 1 to show selected cells
        """
        assert len(pos) == 2 and pos[0] < self.N and pos[1] < self.M
        ls = [0 for _ in range(self.M * self.N)]
        ls[self.pos_tr(pos)] = 1
        ls = self.choose_helper(pos, state, ls)
        return ls

    def choose_helper(self, pos, state, ls):
        """
        This function is to help to select same color based on clickomania rule
        :param pos: the position of selected cell
        :param state: current clickomania
        :param ls: the marked list that have already selected
        :return a list of 0 and 1 to show selected cells
        """
        pos_t = self.pos_tr(pos)
        if pos[0] > 0:
            next_pos = [pos[0] - 1, pos[1]]
            next_pos_t = self.pos_tr(next_pos)
            if state.value[pos_t] == state.value[next_pos_t] and ls[next_pos_t] != 1:
                ls[next_pos_t] = 1
                ls = self.choose_helper(next_pos, state, ls)
        if pos[0] < self.N - 1:
            next_pos = [pos[0] + 1, pos[1]]
            next_pos_t = self.pos_tr(next_pos)
            if state.value[pos_t] == state.value[next_pos_t] and ls[next_pos_t] != 1:
                ls[next_pos_t] = 1
                ls = self.choose_helper(next_pos, state, ls)
        if pos[1] > 0:
            next_pos = [pos[0], pos[1] - 1]
            next_pos_t = self.pos_tr(next_pos)
            if state.value[pos_t] == state.value[next_pos_t] and ls[next_pos_t] != 1:
                ls[next_pos_t] = 1
                ls = self.choose_helper(next_pos, state, ls)
        if pos[1] < self.M - 1:
            next_pos = [pos[0], pos[1] + 1]
            next_pos_t = self.pos_tr(next_pos)
            if state.value[pos_t] == state.value[next_pos_t] and ls[next_pos_t] != 1:
                ls[next_pos_t] = 1
                ls = self.choose_helper(next_pos, state, ls)

        return ls

    def eliminate(self, state, ls):
        """
        This function is to set selected cells to zero
        :return a new next state without fall down
        """
        assert sum(ls) > 1
        nextstate = state.clone()
        for pos, selected in enumerate(ls):
            if selected == 1:
                nextstate.value[pos] = 0
        return nextstate

    def falldown(self, state):
        """
        To fall down the cells without supporting and moving columns right next to empty columns
        :param state: the state need to be processed
        :return: a state don't need to fall down again
        """
        tag = False
        for i in range(self.M):
            curr_col = []
            for j in range(self.N):
                curr_col.append(state.value[self.pos_tr([j, i])])
            if sum(curr_col) == 0:
                tag = True
                continue
            elif 0 not in curr_col:
                continue
            else:
                while 0 in curr_col:
                    del curr_col[curr_col.index(0)]
                curr_col = [0 for _ in range(self.N - len(curr_col))] + curr_col
                for j in range(self.N):
                    state.value[self.pos_tr([j, i])] = curr_col[j]
        if tag:
            i = 0
            m = 0
            while 1:
                if i >= self.M: break
                curr_col = []
                for j in range(self.N):
                    curr_col.append(state.value[self.pos_tr([j, i])])
                if sum(curr_col) == 0:
                    for j in range(self.N):
                        curr_row = []
                        for k in range(self.M):
                            curr_row.append(state.value[self.pos_tr([j, k])])
                        del curr_row[i]
                        curr_row.append(0)
                        for k in range(self.M):
                            state.value[self.pos_tr([j, k])] = curr_row[k]
                    m = m + 1
                    if m + i > self.M: break
                else:
                    i = i + 1

        return state

    def successors(self, state):
        """
        find all possible solution of this state
        :param state: The current state
        :return: a list of (cost, nextstate), the penalty is counted into final step
        """
        succs = []
        marked_ls = [0 for _ in range(self.M * self.N)]
        for it in range(self.M * self.N):
            if marked_ls[it] == 1: continue
            if state.value[it] == 0:
                marked_ls[it] = 1
                continue
            marked_ls[it] = 1
            pos = [int(it / self.M), it % self.M]
            ls = self.choose(pos, state)
            clear_nums = sum(ls)
            if clear_nums > 1:
                for i in range(len(ls)):
                    if marked_ls[i] == 0 and ls[i] == 1:
                        marked_ls[i] = 1
                nextstate = self.eliminate(state, ls)
                nextstate = self.falldown(nextstate)
                score = (clear_nums - 1) ** 2
                if self.isFinal(nextstate):
                    penalty_score = self.penalty(nextstate)
                    score = score - penalty_score
                    nextstate.IsFinal = True
                succs.append((score, nextstate))
        return succs

    def isFinal(self, state):
        """
        judge whether this state is final state
        :param state: current state
        :return: True or False
        """
        marked_ls = [0 for _ in range(self.M * self.N)]
        for it in range(self.M * self.N):
            if marked_ls[it] == 1: continue
            if state.value[it] == 0:
                marked_ls[it] = 1
                continue
            marked_ls[it] = 1
            pos = [int(it / self.M), it % self.M]
            ls = self.choose(pos, state)
            clear_nums = sum(ls)
            if clear_nums > 1:
                return False
        return True

    def penalty(self, state):
        """
        calucate penalty for this state
        :param state: current state (which should be final state)
        :return: penalty score
        """
        penalty_score = 0
        value = state.value
        for i in range(1, self.K):
            amount = value.count(i)
            if amount > 0:
                penalty_score = penalty_score + (amount - 1) ** 2
        return penalty_score

    def isGoal(self, state):
        """
        :param state: current state
        :return: True or False
        """
        return state.IsFinal

class CSP:

    def __init__(self, n):
        self.size = n
        self._queens = []
        for i in range(n):
            q = Queen(i)
            for j in range(n):
                q.add_domain(j)
            self._queens.append(q)


    def check_constraints(self, a_row, a_col, b_row, b_col):
        if a_row == b_row:
            return False
        if (a_row + a_col) == (b_row + b_col):
            return False
        if (a_row - a_col) == (b_row - b_col):
            return False
        return True


class Queen:

    def __init__(self, col):
        self.col = col
        self.row = None
        self._domains = []

    def add_domain(self, domain):
        self._domains.append(domain)

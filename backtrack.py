from helpers import CSP, Queen
import numpy as np

def backtrack(csp):
    matrix = [["" for i in range(csp.size)] for j in range(csp.size)]
    counter = 0
    assignments = [None for i in range(csp.size)]
    while counter < csp.size and counter > -1:
        domains = csp._queens[counter]._domains
        queen = csp._queens[counter]
        row = select_value(csp, counter, assignments)
        assignments[counter] = row
        if row is None:
            counter -= 1
        else:
            counter += 1
            if counter < csp.size:
                csp._queens[counter]._domains = list(range(csp.size))

    if counter < 0:
        return "No Solution Found"
    for i in range(len(csp._queens)):
        queen = csp._queens[i]
        matrix[assignments[i]][queen.col] = "Q"
    return np.matrix(matrix)


def select_value(csp, counter, assignments):
    assignments = assignments[:counter]
    b = csp._queens[counter]
    domains = b._domains
    if counter == 0:
        if len(domains) == 0:
            return None
        return domains.pop(0)

    while len(domains) != 0:
        domain = domains.pop(0)
        if check_consistency(csp, assignments, domain, b.col):
            return domain
    return None


def check_consistency(csp, assignments, domain, col):
    for a in range(len(assignments)):
        if not csp.check_constraints(assignments[a], a, domain, col):
            return False
    return True
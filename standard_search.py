import numpy as np
from helpers import CSP, Queen


def standard_search(csp):
    matrix = [["" for i in range(csp.size)] for j in range(csp.size)]
    counter = 0
    stack = []
    solution = None
    for domain in csp._queens[0]._domains:
        assignments = []
        assignments.append(domain)
        stack.append(assignments)
    while len(stack) != 0:
        node = stack.pop()
        if len(node) == csp.size:
            if check_consistency(csp, node):
                solution = node
        else:
            col = len(node)
            for domain in csp._queens[col]._domains:
                new_node = node + [domain]
                stack.append(new_node)
    if solution is None:
        return "No Solution Found"
    else:
        for i in range(len(solution)):
            matrix[solution[i]][i] =  "Q"
        return np.matrix(matrix)

def check_consistency(csp, node):
    for i in range(len(node) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            if not csp.check_constraints(node[i], i, node[j], j):
                return False
    return True

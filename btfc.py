from helpers import CSP, Queen
import numpy as np

def btfc(csp):
    matrix = [["" for i in range(csp.size)] for j in range(csp.size)]
    prev_counter = -1
    counter = 0
    assignments = [None for i in range(csp.size)]
    n = csp.size
    origDict = {}
    while counter < n and counter > -1:
        if prev_counter < counter:
            original_domains = []
            i = 0
            while i < csp.size:
                queen = csp._queens[i]
                original_domains.append(list(queen._domains))
                i += 1
            origDict[counter] = original_domains
        row, csp = select_value_FC(csp, counter, assignments, origDict[counter])
        assignments[counter] = row
        #print(row, counter)
        #print(origDict)
        if row is None:
            #csp = reset_domains(csp, counter, original_domains)
            if counter != 0:
                j = 1
                while (counter + j) < csp.size:
                    reset = csp._queens[counter + j]
                    reset._domains = list(origDict[counter][counter + j])
                    #print(counter + j, reset._domains)
                    #print(reset.col, reset._domains)
                    j += 1
            prev_counter = counter
            counter -= 1

        else:
            prev_counter = counter
            counter += 1
    if counter < 0:
        return "No Solution Found"
    for i in range(len(csp._queens)):
        queen = csp._queens[i]
        matrix[assignments[i]][queen.col] = "Q"
    return np.matrix(matrix)


def select_value_FC(csp, counter, assignments, original_domains):
    boolean = False
    assignments = assignments[:counter]
    while len(csp._queens[counter]._domains) != 0:
        queen = csp._queens[counter]
        a = queen._domains.pop(0)
        for k in range(counter + 1, csp.size):
            k_queen = csp._queens[k]
            iterable = k_queen._domains[:]
            for value in iterable:
                if not (check_consistency(csp, assignments, a, queen.col) and check_consistency(csp, assignments, value, k_queen.col) and csp.check_constraints(a, queen.col, value, k_queen.col)):
                    k_queen._domains.remove(value)
            if len(k_queen._domains) == 0:
                j = 1
                while (counter + j) < csp.size:
                    reset = csp._queens[counter + j]
                    reset._domains = original_domains[counter + j]
                    j += 1
                boolean = True
                break
            else:
                boolean = False
        if boolean is False:
            return a, csp
    return None, csp

def check_consistency(csp, assignments, row, col):
    for a in range(len(assignments)):
        if assignments[a] == None:
            continue
        if not csp.check_constraints(assignments[a], a, row, col):
            return False
    return True

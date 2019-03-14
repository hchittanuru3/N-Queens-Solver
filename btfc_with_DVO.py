from helpers import CSP, Queen
import numpy as np
import operator

def btfc_with_DVO(csp):
    matrix = [["" for i in range(csp.size)] for j in range(csp.size)]
    assignments = {}
    order = list(range(csp.size))
    prev_counter = -1
    i = 0
    origDict = {}
    while i < csp.size and i >= 0:
        col = order[i]
        if prev_counter < i:
            original_domains = []
            for d in order:
                original_domains.append(list(csp._queens[d]._domains))
            origDict[col] = original_domains
        row, csp = select_value_FC(csp, col, assignments, origDict[col], order, i)
        assignments[col] = row
        if row is None:
            if i != 0:
                arr = order[i + 1:]
                for elem in arr:
                    reset = csp._queens[elem]
                    reset._domains = list(origDict[col][elem])
            prev_counter = i
            i -= 1
        else:
            if i != (csp.size - 1):
                next_queen = select_min(csp, order, i)
                order.remove(next_queen)
                order = order[:i + 1] + [next_queen] + order[i+1:]
                #print(order)
            prev_counter = i
            i += 1
    if i < 0:
        return "No Solution Found"
    else:
        for i in range(len(csp._queens)):
            queen = csp._queens[i]
            matrix[assignments[i]][queen.col] = "Q"
        return np.matrix(matrix)


def select_value_FC(csp, queen, assignments, original_domains, order, counter):
    boolean = False
    new_order = order[:counter]
    unassigned = order[counter + 1:]
    curr_queen = csp._queens[queen]
    #print(curr_queen._domains, order, unassigned)
    while len(curr_queen._domains) != 0:
        domain = select_domain(csp, assignments, curr_queen)
        curr_queen._domains.remove(domain)
        for k in unassigned:
            k_queen = csp._queens[k]
            iterable = k_queen._domains[:]
            for value in iterable:
                #print(domain, curr_queen.col, value, k_queen.col)
                if not (check_consistency(csp, assignments, domain, curr_queen.col, new_order) and check_consistency(csp, assignments, value, k_queen.col, new_order) and csp.check_constraints(domain, curr_queen.col, value, k_queen.col)):
                    k_queen._domains.remove(value)
            if len(k_queen._domains) == 0:
                for u in unassigned:
                    reset = csp._queens[u]
                    csp._queens[u]._domains = list(original_domains[u])
                boolean = True
                break
            else:
                boolean = False
        if boolean is False:
            return domain, csp
    return None, csp



def select_min(csp, order, counter):
    unassigned = order[counter + 1:]
    min_value = unassigned[0]
    for i in unassigned[1:]:
        if len(csp._queens[i]._domains) < len(csp._queens[min_value]._domains):
            min_value = i
    return min_value

def check_consistency(csp, assignments, row, col, order):
    for i in order:
        if not csp.check_constraints(assignments[i], i, row, col):
            return False
    return True

def select_domain(csp, unassigned, queen):
    hashmap = {}
    for i in queen._domains:
        hashmap[i] = 1
    for i in unassigned:
        curr_queen = csp._queens[i]
        for j in curr_queen._domains:
            if j in hashmap.keys():
                hashmap[j] += 1
    return min(hashmap.items(), key=operator.itemgetter(1))[0]

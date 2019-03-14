import time
import sys
import matplotlib.pyplot as plt
import numpy as np
from standard_search import standard_search
from btfc import btfc
from backtrack import backtrack
from btfc_with_DVO import btfc_with_DVO
from helpers import CSP

def runner():
    if sys.argv[1] == "plot":
        plot()
        return
    n = int(sys.argv[2])
    if sys.argv[1] == "1":
        print(standard_search(CSP(n)))
    elif sys.argv[1] == "2":
        print(backtrack(CSP(n)))
    elif sys.argv[1] == "3":
        print(btfc(CSP(n)))
    elif sys.argv[1] == "4":
        print(btfc_with_DVO(CSP(n)))
    else:
        print("Wrong arguments.")


def plot():

    #x_new = np.linspace(min(x), max(y), 300)
    #smooth_y = spline(x, y, x_new)

    x = []
    y = []
    n = 1
    functions = [standard_search, backtrack, btfc, btfc_with_DVO]
    min_y = float('inf')
    max_y = -float('inf')
    min_x = float('inf')
    max_x = -float('inf')

    i = 0
    while i < 4:
        start_time = time.time()
        functions[i](CSP(n))
        end_time = time.time()
        diff = end_time - start_time
        if diff > 10:
            print(functions[i].__name__)
            print(x)
            print(y)
            z = np.polyfit(x, y, 2)
            f = np.poly1d(z)
            #x_new = np.linspace(x[0], x[-1], 100)
            y_new = f(x)
            if min(x) < min_x:
                min_x = min(x)
            if max(x) > max_x:
                max_x = max(x)
            if min(y) < min_y:
                min_y = min(y)
            if max(y) > max_y:
                max_y = max(y)
            plt.plot(x, y_new, label=functions[i].__name__)
            i += 1
            n = 1
            x = []
            y = []
        else:
            print(n)
            x.append(n)
            y.append(diff)
            n += 1

    # Graph UI Setup
    plt.xlabel('# of Queens, n')
    plt.ylabel('Computational Time (s) (logarithmic)')
    plt.title('N vs. Time')
    plt.ylim(min_y, max_y)
    plt.xlim(min_x, max_x)
    #plt.yscale('log')
    plt.legend(["Standard Search", "BT Search", "BT Search w/ FC", "BT Search w/ FC and DVO"], loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
    return

def fit(x, a, b):
    return a*x + b

if __name__ == '__main__':
    runner()



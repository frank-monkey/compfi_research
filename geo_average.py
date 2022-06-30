#optimized geometric average for calls and puts O(n^3) complexity
import numpy as np
np.set_printoptions(suppress=True)

def call(S_0, K):
    return max(0, S_0 - K)

def put(S_0, K):
    return max(0, K - S_0)

def chooser(S_0, K):
    return max(S_0 - K, K - S_0)

def geo_average(pricing_method, S_0, K, n, r, u, d):
    #generates a list of 0s and 1s to represent paths possible
    combinations = [list(('{:0' + str(n) + 'b}').format(x)) for x in range(2**n)] 
    p = ((1 + r - d)/(u - d))
    q = 1 - p
    sum = 0
    for comb in combinations:
        probability, price = 1, S_0
        for i in range(len(comb)):
            if comb[i]=='1':
                probability *= p
                price *= u**i
            else:
                probability *= q
                price *= d**i
        sum += probability * price
    print(((1/(r+1))**n * sum))

geo_average(call, 10, 5, 5, 0.25, 2, 0.5)
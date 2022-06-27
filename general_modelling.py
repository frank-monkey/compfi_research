import math
import numpy as np
import pandas as pd
np.set_printoptions(suppress=True)

def binomial_pricing(S_0, n, u, d):
    prices = np.zeros((n+1, n+1))
    prices[0][0] = S_0
    for j in range(1,n+1):
        prices[j][j]=u*prices[j-1][j-1]
        for i in range(0, j):
            prices[i][j] = d*prices[i][j-1]
    print(prices)
    return prices

def bachelier_pricing(S_0, n, mu, beta): 
    prices = np.zeros((n+1, n+1))
    prices[0][0] = S_0
    for j in range(1,n+1):
        prices[j][j]=mu*(1+prices[j-1][j-1])+beta
        for i in range(0, j):
            prices[i][j] = mu*(1+prices[i][j-1])-beta
    print(prices)
    return prices

def arithmetic_bachelier_pricing(S_0, n, alpha, beta): 
    prices = np.zeros((n+1, n+1))
    prices[0][0] = S_0
    for j in range(1,n+1):
        prices[j][j]=prices[j-1][j-1]+alpha+beta
        for i in range(0, j):
            prices[i][j] = prices[i][j-1]+alpha-beta
    print(prices)
    return prices



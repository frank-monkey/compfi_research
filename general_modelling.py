import math
import numpy as np
import pandas as pd
np.set_printoptions(suppress=True)

#modelling methods
def binomial_model(S_0, n, u, d):
    prices = np.zeros((n+1, n+1))
    prices[0][0] = S_0
    for j in range(1,n+1):
        prices[j][j]=u*prices[j-1][j-1]
        for i in range(0, j):
            prices[i][j] = d*prices[i][j-1]
    print(prices)
    return prices

def bachelier_model(S_0, n, mu, beta): 
    prices = np.zeros((n+1, n+1))
    prices[0][0] = S_0
    for j in range(1,n+1):
        prices[j][j]=mu*(1+prices[j-1][j-1])+beta
        for i in range(0, j):
            prices[i][j] = mu*(1+prices[i][j-1])-beta
    print(prices)
    return prices

def arithmetic_bachelier_model(S_0, n, alpha, beta): 
    prices = np.zeros((n+1, n+1))
    prices[0][0] = S_0
    for j in range(1,n+1):
        prices[j][j]=prices[j-1][j-1]+alpha+beta
        for i in range(0, j):
            prices[i][j] = prices[i][j-1]+alpha-beta
    print(prices)
    return prices

#option pricing methods
def call(S, K):
    return max(0, S - K)

def put(S, K):
    return max(0, K - S)

def chooser(S, K):
    return abs(S - K)

def squared_price(S, K):
    return S**2

def summation_root(S, K):
    return np.sum(S)**(1/len(S))

def product_root(S, K):
    return np.prod(S)**(1/len(S))

def path_independent_pricing(prices, option_pricing, K, p, n, r):
    q=1-p
    op = lambda z : option_pricing(z, K)
    V = np.zeros((n+1, n+1))
    for j in range(0, n):
        V[j][n] = op(prices[j][n])

    for j in range(n-1, -1, -1):
        for i in range(n-1, j-1, -1):
            V[j][i] = (1/(r+1))*(p*V[j][i+1]+q*V[j+1][i+1])
    print(V)
    print(V[0][0])

def path_dependent_pricing(prices, option_pricing, K, p, n, r):
    q=1-p
    sum = 0
    op = lambda z : option_pricing(z, K)
    
    combinations = [list('{:03b}'.format(x)) for x in range(2**n)]

    for comb in combinations:
        probability = 1
        ret_prices = []
        row = 0
        col = 0
        for i in len(comb):
            if comb[i].equals('0'):
                probability*=p
                row+=1
                col+=1
                ret_prices[i]=prices[row][col]
            else:
                probability*=q
                col+=1
                ret_prices[i] = prices[row][col]

        sum+=probability*op(ret_prices)
    print(sum)


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
    return max(0, S[0] - K)

def put(S, K):
    return max(0, K - S[0])

def chooser(S, K):
    return max(S[0] - K, K - S[0])

def squared_price(S, K):
    return S[0]**2

def summation_root(S, K):
    return np.sum(S)**(1/len(S))

def product_root(S, K):
    return np.prod(S)**(1/len(S))

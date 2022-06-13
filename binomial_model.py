#Frank Sacco Computational Finance Research
#13/6/22

import math
import numpy as np
np.set_printoptions(suppress=True)

S_0 = 8 #initial price
K = 10 #strike

n = 5 #periods till maturity

r = 0.25 #interest rates (in decimal form)
u = 2 #upside factor
d = 0.5 #downside factor

#these methods abstract calculations of calls and puts 
# to make it easy to implement unique options
# X is strike, price is price of stock 

@staticmethod
def call(S_0, K):
    return max(0, S_0 - K)

@staticmethod
def put(S_0, K):
    return max(0, K - S_0)

@staticmethod
def squared_price(S_0, K):
    return S_0**2

#calculates using non-recursive derived formula
@staticmethod
def non_recursive(pricing_method, S_0, K, n, r, u, d):
    p_hat = ((1+r-d)/(u-d))
    q_hat = 1 - p_hat
    print("p_hat = " + str(p_hat) + " q_hat = " + str(q_hat))
    sum = 0 
    for k in range (0,n):
        sum += pricing_method(S_0*(u**k)*(d**(n-k)), K)*math.comb(n,k)*(p_hat**k)*(q_hat**(n-k))
    return 1/((1+r)**n)*sum

#pure recursion
@staticmethod
def recursive_binomial_model(pricing_method, S_0, K, n, r, u, d):
    p_hat = ((1+r-d)/(u-d))
    q_hat = 1 - p_hat
    #print("p_hat = " + str(p_hat) + " q_hat = " + str(q_hat))
    if (n==0):
        return pricing_method(S_0, K)
    else:
        return (1/(1+r))*(p_hat*recursive_binomial_model(pricing_method, u*S_0, K, n-1, r, u, d) 
            + q_hat*recursive_binomial_model(pricing_method, d*S_0, K, n-1, r, u, d))

@staticmethod
def np_binomial_model(pricing_method, S_0, K, n, r, u, d):
    prices = np.zeros((n+1, n+1))
    prices[0][0] = S_0
    for j in range(1,n+1):
        prices[0][j]=d*prices[0][j-1]
        prices[j][j]=u*prices[j-1][j-1]
        for i in range(1, j):
            prices[i][j] = d*prices[i][j-1]
    print(prices)

    p_hat = ((1+r-d)/(u-d))
    q_hat = 1 - p_hat
    print("p_hat = " + str(p_hat) + " q_hat = " + str(q_hat))

    x = lambda p : pricing_method(p, K)

    V = np.zeros((n+1, n+1))

    for j in range(0, n):
        V[j][n] = x(prices[j][n])

    for j in range(0, n-1):
        for i in range(n-1, j-1, -1):
            V[j][i] = (1/(r+1))*(p_hat*V[j][i+1]+p_hat*V[j+1][i+1])
    print(V)

print(non_recursive(put, S_0, K, n, r, u, d))
print(recursive_binomial_model(put, S_0, K, n, r, u, d))
print(np_binomial_model(put, S_0, K, n, r, u, d))
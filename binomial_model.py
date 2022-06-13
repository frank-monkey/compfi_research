#Frank Sacco Computational Finance Research
#13/6/22

import math

X = 10 #strike
S_0 = 8 #initial price

n = 3

r = 0.25
u = 2
d = 0.5

#these methods abstract calculations of calls and puts 
# to make it easy to implement unique options
# X is strike, price is price of stock 
@staticmethod
def call(self, X, price):
    return max(0, price-X)
@staticmethod
def put(self, X, price):
    return max(0, X-price)

#calculates using non-recursive derived formula
@staticmethod
def non_recursive(pricing_method, X, S_0, n, r, u, d):
    p_hat = ((1+r+d)/(u-d))
    q_hat = 1 - p_hat
    sum = 0 
    for k in range (0,n):
        sum += pricing_method(X*(u**k)*(d**(n-k)),S_0)*math.comb(n,k)*(p_hat**k)*(q_hat**(n-k))
    return 1/((1+r)**n)*sum

@staticmethod
def binomial_model(n, r, u, d):
    helper(n, r , u, d, ((1+r+d)/(u-d)))

def helper(n, r, u, d, p_hat)
    if (n==0):
        return 1
    else:
        return (1/(1+r))*(p_hat*u*binomial_model(n-1, r, p_hat) + (1-p_hat)*d*binomial_model(n-1, r, p_hat))


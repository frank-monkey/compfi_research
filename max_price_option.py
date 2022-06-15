#calculate an option which pays out maximum price the stock was throughout the time period
import math
import numpy as np
np.set_printoptions(suppress=True)

#2^n implementation
def max_price_rec(S_0, K, n, r, u, d):
    p=((1+r-d)/(u-d))
    q=1-p
        #print("p_hat = " + str(p_hat) + " q_hat = " + str(q_hat))
    return max_price_rec_helper(S_0, K, n, r, u, d, S_0, p, q)

def max_price_rec_helper(S_0, K, n, r, u, d, max_price, p_hat, q_hat):
    if(S_0>max_price):
        max_price=S_0
    if (n==0):
        return max_price
    else:
        return (1/(1+r))*(p_hat*max_price_rec_helper(u*S_0, K, n-1, r, u, d, max_price, p_hat, q_hat) 
            + q_hat*max_price_rec_helper(d*S_0, K, n-1, r, u, d, max_price, p_hat, q_hat))

print(max_price_rec(100, 80, 5, 0.25, 2, 1/2)) 
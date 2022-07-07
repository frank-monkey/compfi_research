import numpy as np

def call(S_0, K):
    return max(0, S_0 - K)

def put(S_0, K):
    return max(0, K - S_0)

def chooser(S_0, K):
    return max(S_0 - K, K - S_0)

def squared_price(S_0, K):
    return S_0**2

#path dependent options
def summation_root(S, K, t):
    return max(0,np.sum(S)**(1/len(S)))

def product_root(S, K, t):
    return max(0,np.prod(S)**(1/len(S)))

def arithmetic_asian_call(S, K, t):
    S=S[t:]
    return call(np.sum(S)/len(S),K)

def arithmetic_asian_put(S, K, t):
    S=S[t:]
    return put(np.sum(S)/len(S),K)

def arithmetic_asian_chooser(S, K, t):
    S=S[t:]
    return chooser(np.sum(S)/len(S),K)

def geometric_asian_call(S, K, t):
    S=S[t:]
    return call(np.prod(S)**(1/len(S)),K)

def geometric_asian_put(S, K, t):
    S=S[t:]
    return put(np.prod(S)**(1/len(S)),K)

def geometric_asian_chooser(S, K, t):
    S=S[t:]
    return chooser(np.prod(S)**(1/len(S)),K)
    
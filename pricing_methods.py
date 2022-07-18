import numpy as np

def call(S_0: float, K: float) -> float:
    return max(0, S_0 - K)

def put(S_0: float, K: float) -> float:
    return max(0, K - S_0)

def chooser(S_0: float, K: float) -> float:
    return max(S_0 - K, K - S_0)

def squared_price(S_0: float, K: float) -> float:
    return S_0**2

#Methods for use in general_modelling
def summation_root(S: np.float64, K: float) -> float:
    return max(0,np.sum(S)**(1/len(S)))

def product_root(S: np.float64, K: float) -> float:
    return max(0,np.prod(S)**(1/len(S)))

def arithmetic_asian_call(S: np.float64, K: float) -> float:
    return call(np.sum(S)/len(S),K)

def arithmetic_asian_put(S: np.float64, K: float) -> float:
    return put(np.sum(S)/len(S),K)

def geometric_asian_call(S: np.float64, K: float) -> float:
    return call(np.prod(S)**(1/len(S)),K)

def geometric_asian_put(S: np.float64, K: float) -> float:
    return put(np.prod(S)**(1/len(S)),K)
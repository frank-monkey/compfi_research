import numpy as np
import pricing_methods
np.set_printoptions(suppress=True, precision=3)

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

def path_dependent_pricing(prices, option_pricing, K, n, r):
    probabilities = np.zeros((n, n)) #chance of going up each seperate move
    for j in range(0,n):
        for i in range(0, j+1):
            probabilities[i][j] =  ((1+r)*prices[i][j]-prices[i][j+1])/(prices[i+1][j+1]-prices[i][j+1])
    print(probabilities)

    sum = 0
    op = lambda z : option_pricing(z, K)
    combinations = [list(('{:0' + str(n) + 'b}').format(x)) for x in range(2**n)] #generates a list of 0s and 1s to represent paths possible
    #print(combinations)
    for comb in combinations:
        probability = 1
        ret_prices = [] #holds pathing of prices to put into pricing method
        row, col = 0, 0
        for i in comb:
            p = probabilities[row][col]
            q = p-1
            if i=='0':
                probability*=p
                row+=1
                col+=1
                ret_prices.append(prices[row][col])
            else:
                probability*=q
                col+=1
                ret_prices.append(prices[row][col])
        #print(ret_prices)
        #print(op(ret_prices))
        sum += probability * op(ret_prices)
    print(sum)
    print(((1/(r+1))**n*sum))

path_dependent_pricing(binomial_model(10, 2, 2, 0.5), pricing_methods.geometric_asian_call, 5, 2, 0.25) 

#path_dependent_pricing(bachelier_model(10, 10, 1, 2), product_root, -1, 10, 0.03) 
#path_dependent_pricing(binomial_model(8, 10, 2, 0.5), asian_call, 8, 10, 0.25) 
#path_dependent_pricing(arithmetic_bachelier_model(10, 5, 0.3, 0.2), product_root, -1, 0.5, 5) 
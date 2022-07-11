#Can do any asian model except choosers
import numpy as np
import pricing_methods
np.set_printoptions(suppress=True, precision=3)

#modelling methods
def binomial_model(S_0, n, u, d):
    prices = np.zeros((2**n, n+1))
    prices[0][0] = S_0
    for j in range(0, n):
        for i in range(0, 2**j):
            prices[2*i+1][j+1] = u*prices[i][j] #up case
            prices[2*i][j+1] = d*prices[i][j] #down case
    print(prices)
    return prices

def bachelier_model(S_0, n, mu, beta): 
    prices = np.zeros((2**n, n+1))
    prices[0][0] = S_0
    for j in range(0, n):
        for i in range(0, 2**j):
            prices[2*i+1][j+1] = mu*prices[i][j]+beta #up case
            prices[2*i][j+1] = mu*prices[i][j]-beta #down case
    print(prices)
    return prices

def arithmetic_bachelier_model(S_0, n, alpha, beta): 
    prices = np.zeros((2**n, n+1))
    prices[0][0] = S_0
    for j in range(0, n):
        for i in range(0, 2**j):
            prices[2*i+1][j+1] = prices[i][j]+alpha+beta #up case
            prices[2*i][j+1] = prices[i][j]+alpha-beta #down case
    print(prices)
    return prices

def path_dependent_pricing(prices, option_pricing, K, n, r, t=0):
    probabilities = np.zeros((2**(n-1), n)) #p_hat of each move
    for j in range(0,n):
        for i in range(0, 2**j):
            S_0 = prices[i][j]
            up = prices[2*i+1][j+1]
            down = prices[2*i][j+1]
            probabilities[i][j] =  ((1+r)*S_0-down)/(up-down)
    print(probabilities)

    sum = 0
    op = lambda z : option_pricing(z, K, t)
    for i in range(2**n):
        comb = ('{:0' + str(n) + 'b}').format(i) #outputs combination of '1's and '0's corresponding to binary code of i
        probability = 1
        ret_prices = [] #holds history of prices to put into pricing method
        row, col = 0, 0
        for i in comb:
            p = probabilities[row][col]
            q = 1 - p
            if i=='0': #up
                probability*=p
                row=2*row+1
                col+=1
                ret_prices.append(prices[row][col])
            else: #down
                probability*=q
                row*=2
                col+=1
                ret_prices.append(prices[row][col])
        sum += probability * op(ret_prices)
    print("interest-free price = " + str(sum))
    return (((1/(r+1))**n * sum))

#binomial_model(10,4,2,0.5)
#bachelier_model(10,4,2,0.5)
#arithmetic_bachelier_model(10,4,2,0.5)

#print(path_dependent_pricing(binomial_model(8, 3, 2, 0.5), pricing_methods.geometric_asian_call, 16, 3, 0.25, 2) )
#print(path_dependent_pricing(binomial_model(10, 5, 2, 0.5), pricing_methods.geometric_asian_call, 5, 5, 0.25) )
print(path_dependent_pricing(bachelier_model(100, 5, 0.3, 0.5), pricing_methods.arithmetic_asian_call, 5, 5, 0.25, 1) )
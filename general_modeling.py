# Will process most options in various models in O(n^2) time
# More optimized versions of each option in other files
import numpy as np
import pricing_methods
np.set_printoptions(suppress=True, precision=3)

def binomial_model(S_0, n, u, d):
    prices = np.zeros((2**n, n+1))
    prices[0][0] = S_0
    for j in range(0, n):
        for i in range(0, 2**j):
            prices[2*i+1][j+1] = u*prices[i][j] #up case
            prices[2*i][j+1] = d*prices[i][j] #down case
    #print(prices)
    return prices

def bachelier_model(S_0, n, mu, beta): 
    prices = np.zeros((2**n, n+1))
    prices[0][0] = S_0
    for j in range(0, n):
        for i in range(0, 2**j):
            prices[2*i+1][j+1] = mu*prices[i][j]+beta #up case
            prices[2*i][j+1] = mu*prices[i][j]-beta #down case
    #print(prices)
    return prices

def arithmetic_bachelier_model(S_0, n, alpha, beta): 
    prices = np.zeros((2**n, n+1))
    prices[0][0] = S_0
    for j in range(0, n):
        for i in range(0, 2**j):
            prices[2*i+1][j+1] = prices[i][j]+alpha+beta #up case
            prices[2*i][j+1] = prices[i][j]+alpha-beta #down case
    #print(prices)
    return prices

#prev_prices will add previous prices to the beginning of a method
def path_dependent_pricing(pricing_model, option_pricing, S_0, K, n, r, var1, var2, prev_prices=[]):
    op = lambda S : option_pricing(S, K)
    if(n==0 and not prev_prices):
        return op([S_0])
    elif(n==0 and prev_prices):
        return op(prev_prices)
    prices = pricing_model(S_0, n, var1, var2)
    probabilities = np.zeros((2**(n-1), n)) #p_hat of each move
    for j in range(0,n):
        for i in range(0, 2**j):
            S_0 = prices[i][j]
            up = prices[2*i +1][j+1]
            down = prices[2*i][j+1]
            probabilities[i][j] =  ((1+r)*S_0 - down)/(up - down)

    sum = 0
    for i in range(2**n):
        #outputs combination of '1's and '0's corresponding to binary code of i
        comb = ('{:0' + str(n) + 'b}').format(i)
        probability = 1
        row, col = 0, 0
        if(prev_prices): #if previous prices are passed in use those
            ret_prices = prev_prices.copy()
        else:
            ret_prices = [prices[0][0]]
        for i in comb:
            p = probabilities[row][col]
            q = 1 - p
            if i == '0': #up
                probability *= p
                row = 2*row + 1
                col += 1
            else: #down
                probability *= q
                row *= 2
                col += 1
            ret_prices.append(prices[row][col])
        sum += probability * op(ret_prices)
    return ((sum * (1/(r+1))**n))

#Returns arithmetic average of price between tau and T - non zero interest rates don't work
def arithmetic_asian_tail_chooser(pricing_model, S_0, K, n, tau, r, var1, var2):
    r = 0
    op = lambda S: max(path_dependent_pricing(pricing_model, pricing_methods.arithmetic_asian_call, S, K, n-tau, r, var1, var2), path_dependent_pricing(pricing_model, pricing_methods.arithmetic_asian_put, S, K, n-tau, r, var1, var2))
    if(tau==0):
        return max(path_dependent_pricing(pricing_model, pricing_methods.arithmetic_asian_call, S_0, K, n, r, var1, var2), path_dependent_pricing(pricing_model, pricing_methods.arithmetic_asian_put, S_0, K, n, r, var1, var2))
    prices = pricing_model(S_0, tau, var1, var2)
    probabilities = np.zeros((2**(tau-1), tau)) #p_hat of each move
    for j in range(0,tau):
        for i in range(0, 2**j):
            S_0 = prices[i][j]
            up = prices[2*i+1][j+1]
            down = prices[2*i][j+1]
            probabilities[i][j] =  ((1+r)*S_0 - down)/(up - down)

    sum = 0
    for i in range(2**tau):
        #outputs combination of '1's and '0's corresponding to binary code of i
        comb = ('{:0' + str(tau) + 'b}').format(i)
        probability = 1
        row, col = 0, 0
        for i in comb:
            p = probabilities[row][col]
            q = 1 - p
            if i == '0': #up
                probability *= p
                row = 2*row + 1
                col += 1
            else: #down
                probability *= q
                row *= 2
                col += 1
            price = prices[row][col]
        sum += probability * op(price)
    return (((1/(r+1))**(n-tau)) * sum)

#returns price between 0 and T regardless of tau, nonzero interest rates don't work
def arithmetic_asian_full_chooser(pricing_model, S_0, K, n, tau, r, var1, var2):
    r = 0
    op = lambda S, passed_prices : max(path_dependent_pricing(pricing_model, pricing_methods.arithmetic_asian_call, S, K, n-tau, r, var1, var2, passed_prices), path_dependent_pricing(pricing_model, pricing_methods.arithmetic_asian_put, S, K, n-tau, r, var1, var2, passed_prices))
    if(tau==0):
        return op(S_0, tau)
    prices = pricing_model(S_0, tau, var1, var2)
    probabilities = np.zeros((2**(tau - 1), tau)) #p_hat of each move
    for j in range(0, tau):
        for i in range(0, 2**j):
            S_0 = prices[i][j]
            up = prices[2*i+1][j+1]
            down = prices[2*i][j+1]
            probabilities[i][j] =  ((1+r)*S_0-down)/(up-down)
    #print(probabilities)

    sum = 0
    for i in range(2**tau):
        comb = ('{:0' + str(tau) + 'b}').format(i) #outputs combination of '1's and '0's corresponding to binary code of i
        probability = 1
        row, col = 0, 0
        passed_prices = [prices[0][0]]
        for i in comb:
            p = probabilities[row][col]
            q = 1 - p
            if i=='0': #up
                probability*=p
                row=2*row + 1
                col+=1
                passed_prices.append(prices[row][col])
            else: #down
                probability*=q
                row*=2
                col+=1
                passed_prices.append(prices[row][col])
        sum += probability * op(passed_prices[-1], passed_prices)
    return (((1/(r+1))**(n-tau)) * sum)
#binomial_model(10,4,2,0.5)
#bachelier_model(10,4,1.1,0.5)
#arithmetic_bachelier_model(10,4,2,0.5)

#print(path_dependent_pricing(binomial_model(8, 3, 2, 0.5), pricing_methods.geometric_asian_call, 16, 3, 0.25, 2) )
#print(path_dependent_pricing(binomial_model(10, 5, 2, 0.5), pricing_methods.geometric_asian_call, 5, 5, 0.25) )
#print(path_dependent_pricing(bachelier_model(10,4,1.1,0.5), pricing_methods.arithmetic_asian_call, 5, 5, 0.25, 1) )

S_0 = 8 #initial price
K = 13 #strike
n : int  = 15 #periods till maturity
r = 0 #interest rates (in decimal form)
u = 2 #upside factor
d = 0.5 #downside factor
tau : int = 0 #time call or put has to be chosen

#print(path_dependent_pricing(binomial_model, pricing_methods.arithmetic_asian_put, S_0, K, n, r, u, d) )
#print(path_dependent_pricing(binomial_model(S_0, n, u, d), pricing_methods.arithmetic_asian_put, K, n, r) )


#print(path_dependent_pricing(binomial_model, pricing_methods.arithmetic_asian_call, S_0, K, n, r, u, d) )
'''
print("full chooser = " + str(arithmetic_asian_full_chooser(binomial_model, S_0, K, n, tau, r, u, d)/((1+r)**tau)))
#print("tail chooser = " + str(arithmetic_asian_tail_chooser(binomial_model, S_0, K, n, tau, r, u, d)))
'''
#print("price of a put = " + str(path_dependent_pricing(binomial_model, pricing_methods.arithmetic_asian_put, S_0, K, n, r, u, d)))
#print("price of a call = " + str(path_dependent_pricing(binomial_model, pricing_methods.arithmetic_asian_call, S_0, K, n, r, u, d)))
#print("price of a put and a call = " + str(path_dependent_pricing(binomial_model, pricing_methods.arithmetic_asian_call, S_0, K, n, r, u, d)+ path_dependent_pricing(binomial_model, pricing_methods.arithmetic_asian_put, S_0, K, n, r, u, d) ))
# ^^^^ price of a put and a call expiring at T at time 0




#print(arithmetic_asian_full_chooser(bachelier_model, 100, 120, 5, 1, 0, 1.1, 50))
#print(arithmetic_asian_full_chooser(bachelier_model, 100, 120, 5, 2, 0, 1.1, 50))

n=2

#print(arithmetic_asian_full_chooser(bachelier_model, 100, 120, n, 0, 0, 1.1, 50))
#print(arithmetic_asian_full_chooser(bachelier_model, 100, 120, n, 1, 0, 1.1, 50))#should be 62.44
#print(arithmetic_asian_full_chooser(bachelier_model, 100, 120, n, 2, 0, 1.1, 50))#should also be 62.44

print(arithmetic_asian_full_chooser(bachelier_model, 100, 120, 3, 3, 0, 1.1, 50))
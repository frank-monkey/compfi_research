import plotly.express as px
import pandas as pd
import general_modeling as gm
import math
import numpy
import binomial_model as bm

S_0 = 100 #initial price
K = 200 #strike
n : int  = 15 #periods till maturity
r = 0 #interest rates (in decimal form)
time = 0.1
diff_t = time/n
sigma = 0.03

u = math.e**(sigma * diff_t)
d = math.e**(-sigma * diff_t)

root3_sigma = sigma/(3 ** 0.5)
root3_u = math.e**(root3_sigma * diff_t)
root3_d = math.e**(-root3_sigma * diff_t)


bin, root3_approx, bs_aprox = 0,0,0
bin = gm.path_dependent_pricing(gm.binomial_model, gm.pricing_methods.arithmetic_asian_call, S_0, K, n, r, u, d)
#bach_approx = gm.path_dependent_pricing(gm.binomial_model, gm.pricing_methods.arithmetic_asian_call, S_0, K, n, r, u, d)
root3_approx = bm.non_recursive(bm.call, S_0, K, n, 0, root3_u, root3_d)
bs_approx = ((numpy.log(2/(sigma**2 * time**2)) + numpy.log((sigma**(-2)) * ((math.e ** (sigma**2 * time)) - 1) - time))/time) ** 0.5
#bs_approx = 0

#df = pd.DataFrame([[bin], [bach_approx], [bs_approx]], columns = ['Binomial', 'bach_approx', 'bs_approx'])
fig=px.scatter(x = [0,1,2], y = [bin, root3_approx, bs_approx], 
template='plotly_dark', title = 'Arithmetic Asian Choosers')

print("binary model " + str(bin))
print("root 3 approx " + str(root3_approx))
print("black-scholes approx " + str(bs_approx))
fig.show()
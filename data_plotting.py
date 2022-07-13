import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import general_modelling
import matplotlib.pyplot as plt

S_0 = 8 #initial price
K = 13 #strike
n : int  = 10 #periods till maturity
r = 0.25 #interest rates (in decimal form)
u = 2 #upside factor
d = 0.5 #downside factor
tau : int = 10 #time call or put has to be chosen


x=[]
y=[]
z=[]
for i in range(0, n+1, 1):
    x.append(i)
    y.append(general_modelling.arithmetic_asian_full_chooser(general_modelling.binomial_model, S_0, K, n, i, r, u, d))
    z.append(general_modelling.arithmetic_asian_tail_chooser(general_modelling.binomial_model, S_0, K, n, i, r, u, d))

plt.scatter(x, y, alpha=0.5, color='r')
plt.scatter(x, z, alpha=0.5, color='g')
plt.show()
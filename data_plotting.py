import plotly.express as px
import pandas as pd
import general_modelling

S_0 = 100 #initial price
K = 250 #strike
n : int  = 10 #periods till maturity
r = 0 #interest rates (in decimal form)
a = 1.1 
b = 50
#tau : int = 10 #time call or put has to be chosen

x=[]
y=[]
z=[]
for i in range(0, n+1, 1):
    x.append(i)
    y.append(general_modelling.arithmetic_asian_full_chooser(general_modelling.bachelier_model, S_0, K, n, i, r, a, b))
    z.append(general_modelling.arithmetic_asian_tail_chooser(general_modelling.bachelier_model, S_0, K, n, i, r, a, b))

df = pd.DataFrame(list(zip(y, z)), columns = ['Full', 'Tail'])
fig=px.scatter(df, x=df.index, y=[df.Full, df.Tail], labels={'index' : 'time', 'value' : 'time-zero price'}, 
template='plotly_dark', title = 'Arithmetic Asian Choosers')
fig.add_hline(y=general_modelling.arithmetic_asian_full_chooser(general_modelling.bachelier_model, S_0, K, n, 0, r, a, b), line_dash='dash')
fig.add_hline(y=general_modelling.arithmetic_asian_full_chooser(general_modelling.bachelier_model, S_0, K, n, n, r, a, b), line_dash='dash')
fig.show()
print(df)
print(y)
print(z)

'''
plt=px.scatter(df, x=index, y='ret', color='sharpe', labels={'stdev': "Standard Deviation",
'ret': 'Average Return', 'sharpe': 'Sharpe Ratio'}, hover_data=tickers, template='plotly_dark', title='Sharpe Optimization')
'''
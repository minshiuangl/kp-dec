#Load packages
import pandas as pd
import numpy as np
import datetime

#Load relevant file
dt = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-traded-15-raw.csv')


#Find arbitrage opportunities in the sesssions
    #1) ask (j+1) < ask(j)
    #2) bid (j+1) > bid(j)
  
#Dummy variable for Payoff    
p1 = [1, 1, 1, 0]
p2 = [1, 0, 0, 0]
p3 = [1, 1, 1, 0]
p4 = [1, 1, 0, 0]
p5 = [1, 1, 1, 1]
p = {"": '', 1: p1, 2: p2, 3: p3, 4: p4, 5: p5, 6: p2}

#Complexity
c1 = [10, 11, 9, 4]
c2 = [13, 105, 2, 2]
c3 = [16, 16, 339, 18]
c4 = [12, 12, 2, 2]
c5 = [15, 16, 41, 65]
c6 = [11, 2, 2, 2]
c = {"": '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}

#Dummay variable for Optimal solution
y1 = [0, 0, 1, 0]
y2 = [1, 0, 0, 0]
y3 = [0, 0, 1, 0]
y4 = [0, 0, 0, 0]
y5 = [0, 0, 0, 1]
y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y4}

#Optimal solution
y0 = [164, 254, 1160, 549, 409, 464]


#Create variables and find arbitrage opportunities
arb = pd.DataFrame()
final = pd.DataFrame()
for i in range(1, 6):
    mask = dt.session == i
    file = dt[mask]
    for j in range(1, 7):
        mask = file.problem == j
        temp = file[mask]
        temp = temp.sort_values(by=['tradetime'])
        temp['arbitrage_bid'] = np.where((temp.tradetime <= temp.tradetime.shift()) & \
            (temp.security > temp.security.shift()) & (temp.bid > temp.bid.shift()) & \
            (temp.side == 'BUY'), 1, 0)
        temp['arbitrage_ask'] = np.where((temp.tradetime <= temp.tradetime.shift()) & \
            (temp.security > temp.security.shift()) & (temp.ask < temp.ask.shift()) & \
            (temp.side == 'SELL'), 1, 0)
        for k in range(1, 5):   
            mask = temp.security == k
            t = temp[mask].sort_values(by=['tradetime']).reset_index(drop=True)
            t['payoff'] = np.nan
            t['payoff'] = t['payoff'].fillna(int(p[j][k-1]))
            t['propagation'] = np.nan
            t['propagation'] = t['propagation'].fillna(int(c[j][k-1]))
            t['optimal'] = np.nan
            t['optimal'] = t['optimal'].fillna(int(c[j][k-1]))
            arb = arb.append(t)
            last = t.last_valid_index()
            final = final.append(t.loc[last])

dt = arb

print(np.sum(dt.arbitrage_bid))
print(np.sum(dt.arbitrage_ask))

dt = dt.reset_index(drop=True)

#Create a new dataframe for arbitrage opportunities
indexb = dt[dt['arbitrage_bid']==1].index.values.astype(int)
indexa = dt[dt['arbitrage_ask']==1].index.values.astype(int)

temp = pd.DataFrame()
for i in range(len(indexb)):
    temp = temp.append(dt.loc[indexb[i]])
for i in range(len(indexa)):
    temp = temp.append(dt.loc[indexa[i]])

order = temp.reset_index(drop=True)

index = []
for i in range(len(order.order)):
    o = int(order.order[i])
    temp = dt[dt['consumer'] == o].index.values.astype(int)
    if np.isnan(temp) == False:
        index.append(int(temp))
    else:
        index.append(np.nan)
 
consumer = pd.DataFrame()    
for i in range(len(index)):
    if np.isnan(index[i]) == False:
        consumer = consumer.append(dt.loc[index[i]])
        
        
order['consumer'] = order['consumer'].astype(int)
order['order'] = order['order'].astype(int)
consumer['consumer'] = consumer['consumer'].astype(int)
consumer['order'] = consumer['order'].astype(int)

order = order[['order', 'problem', 'security', 'tradetime', 'side', \
               'trade', 'session', 'type', 'arbitrage_bid', 'payoff', \
               'arbitrage_ask', 'participant_id']].reset_index(drop=True)
consumer = consumer[['consumer', 'order', 'tradetime', 'side', 'trade', \
                     'type']].reset_index(drop=True)

c = pd.DataFrame()
o = pd.DataFrame()
for i in range(len(order.order)):
    for j in range(len(consumer.consumer)):
        if order.order[i] == consumer.consumer[j]:
            c = c.append(consumer.loc[j])
            o = o.append(order.loc[i])

c = c.reset_index(drop=True)
o = o.reset_index(drop=True)

unique = np.unique(o.order).astype(int)
uni = np.unique(order.order).astype(int)
unique = list(set(uni) ^ set(unique))
temp = pd.DataFrame()
for j in range(len(order.order)):
    for i in range(len(unique)):
        if order.order[j] == unique[i]:
            temp = temp.append(order.loc[j])
            
o = o.append(temp).reset_index(drop=True)
data = c.join(o, how='right', lsuffix='_x', rsuffix='_y')
data = data.fillna(0)

data['order'] = data['order_x'].astype(int)
data['consumer'] = data['order_y'].astype(int)
data['trade'] = data['trade_x'] + data['trade_y']
data = data.drop(columns=['trade_x', 'trade_y', 'order_x', 'order_y'])

mask = data.side_x == 0
temp = data[mask].reset_index(drop=True)
data = data[~mask]

final = final.reset_index(drop=True)
time = pd.DataFrame()
for j in range(len(final.order)):
    for i in range(len(temp.order)):
        if temp.problem[i] == final.problem[j] and \
        temp.session[i] == final.session[j] and \
        temp.security[i] == final.security[j]:
            temp['tradetime_x'][i] = final.tradetime[j]

data = data.append(temp)
data = data.sort_values(by=['consumer']).reset_index(drop=True)

data['time'] = np.nan
for i in range(len(data.session)):
    if data.tradetime_x[i] != 0:
        data['tradetime_x'][i] = datetime.datetime.strptime(data.tradetime_x[i], '%H:%M:%S')
        data['tradetime_y'][i] = datetime.datetime.strptime(data.tradetime_y[i], '%H:%M:%S')
        data['time'][i] = data['tradetime_x'][i] - data['tradetime_y'][i]

data.time = data.time.apply(str)
data['tradetime_x'] = data['tradetime_x'].apply(str)
data['tradetime_y'] = data['tradetime_y'].apply(str)

data['type'] = np.where(data['type_y'] == 'CANCEL', data['type_y'], data['type_x'])
data = data.drop(columns=['type_y', 'type_x'])

#Save file for arbitrage opportunities
data.to_csv('/Users/MLEE/Desktop/arbitrage.csv')



#Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import datetime
import math
from scipy import integrate

# =============================================================================
# =============================================================================
# # Compute Trading Results of each Session
# =============================================================================
# =============================================================================

# =============================================================================
# Load relevant files
# =============================================================================
#Choose Experiment Session
nk = 5

#Choose Instance
m = ['', 'Ant', 'Beaver', 'Camel', 'Dolphin', 'Elephant', 'Frog']
e = ['', '-EASY', '-HARD', '-HARD', '-EASY', '-HARD', '-EASY']
mk = 5


#Load csv file
df = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/' \
                 + str(nk) + str(m[mk]) + '-v2.csv')

# =============================================================================
# Set Date
# =============================================================================
date = df.lastModifiedDate[0]
date = date.partition('T')[0]
datetime.datetime.strptime(date, '%Y-%m-%d')

# =============================================================================
# Set Variables
# =============================================================================
#Create trade variable
myTrade = []

for i in range(0, len(df.consumer)):
    #t1 = 1 if df.consumer > 0 else 0
    t1 = 1 if df.consumer[i] > 0 else 0   
    #t2 = 1 if df.order > df.consumer else 0          
    t2 = 1 if df.order[i] > df.consumer[i] else 0  
    #t3 = 1 if df.type == 'LIMIT' else 0
    t3 = 1 if df.type[i] == 'LIMIT' else 0          
    myTrade.append(t1*t2*t3)

df['trade'] = myTrade

#Determine traded price 
myPrice = []

for i in range(0, len(df.consumer)):
    #p = df.price if df.trade = 1 else 0
    p = df.trade[i]*df.price[i]                      
    myPrice.append(p)
        
df['tradeprice'] = myPrice

#Determine whether securities were traded in market
market = range(min(df.market)-1, max(df.market)+1)

mySecurity = {}
ms = {}

for j in range(1, 5):
    mySecurity[j] = [] 
    for i in range(0, len(df.consumer)):
        ms[j] = df.tradeprice[i] if df.market[i] == market[j] and \
        df.trade[i] == 1 else float('nan')
        mySecurity[j].append(ms[j])
    df['security' + str(j)] = mySecurity[j]

# =============================================================================
# Reformat Time
# =============================================================================
#Create new column, where lastModifiedDate is converted to a string variable
    #Separate time stamp, and include only hrs, mins, secs, microsecs
if nk == 5 and mk == 2:
    myTime = []
    for i in range(0, len(df.consumer)):
        t = datetime.datetime.strptime(df.lastModifiedDate[i], \
                                       '%Y-%m-%dT%H:%M:%S.%f') \
                                       + datetime.timedelta(hours=5, minutes=30)
        t = datetime.datetime.strftime(t, '%Y-%m-%dT%H:%M:%S.%f')
        myTime.append(t)
    df['time'] = myTime
    df['time'] = df['time'].str.partition('T')[2]
else:
    df['time'] = df['lastModifiedDate'].str.partition('T')[2]

for i in range(len(df.time)): 
    s = df['time'][i].partition('.')
    if s[1] == '':
        s = s[0] + '.000'
        df.time[i] = s

#Set start time 
starttime = df.createdDate[0]
if nk == 5 and mk == 2:
    starttime = datetime.datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%f') \
    + datetime.timedelta(hours=5, minutes=30)
    starttime = datetime.datetime.strftime(starttime, '%Y-%m-%dT%H:%M:%S.%f')
starttime = starttime.partition('T')[2]
starttime = datetime.datetime.strptime(starttime, '%H:%M:%S.%f')

#Set trading time
myTime = []
for i in range(0, len(df.consumer)):
    t1 = datetime.datetime.strptime(df.time[i], '%H:%M:%S.%f') - starttime
    myTime.append(t1)

myTime[0] = starttime - starttime

df['tradetime'] = myTime 

#Convert trading time to seconds
df['trading_seconds'] = df['tradetime'].dt.total_seconds()

#Reformat tradetime to only inlcude mins and secs
df['tradingtime'] = df.tradetime.apply(str)

temp_lst = []
for i in range(len(df.tradingtime)):
    temp = df.tradingtime[i][10:15]
    temp_lst.append(temp)

df['tradingtime'] = np.array(temp_lst)

#Reformat tradetime to time format for graph
myTime = []

for i in range(len(df.consumer)):
    t = datetime.datetime.strptime(df.tradingtime[i], '%M:%S').time()
    myTime.append(t)

df.tradetime = myTime

# =============================================================================
# =============================================================================
# # Create Bid-Ask Spread
# =============================================================================
# =============================================================================
#Create new dataframe to filter bid-ask spread
dt = df[['tradetime', 'owner', 'tradingtime', 'side', 'price', 'market', \
         'trade', 'order', 'original', 'consumer', 'type', 'trading_seconds']]
dt = dt.sort_values(['tradingtime'])
dt = dt.reset_index(drop=True)

#Convert nan in consumer to -1
dt.consumer = dt.consumer.fillna(-1)
dt.consumer = dt.consumer.astype(int)

#Remove orginal order with multiple units that are later splitted
mySecurity = {}

for j in range(1, 5):
    mySecurity[j] = []
    for i in range(0, len(dt.tradetime)):
        if dt.market[i] == market[j] and dt.consumer[i] == 0:
            ms = np.nan
        elif dt.market[i] == market[j] and dt.consumer[i] != 0:
            ms = dt.price[i] 
        else:
            ms = np.nan
        mySecurity[j].append(ms)
    dt['security' + str(j)] = mySecurity[j]
    
dt = dt[dt.consumer != 0]
dt = dt.reset_index(drop=True)

# =============================================================================
# Create new dataframe for each security
# =============================================================================
security = {}
for i in range(1, 5):
    security[i] = dt[dt.market == market[i]]
    security[i] = security[i].drop(columns=['market', 'tradingtime', \
            'price', 'original'])
    security[i] = security[i].sort_values(by=['tradetime', 'order'])
    security[i] = security[i].reset_index(drop=True)

security[1] = security[1].drop(columns=['security2', 'security3', 'security4'])
security[2] = security[2].drop(columns=['security1', 'security3', 'security4'])
security[3] = security[3].drop(columns=['security1', 'security2', 'security4'])
security[4] = security[4].drop(columns=['security1', 'security2', 'security3'])


# =============================================================================
# =============================================================================
# #Bid-Ask Spread
# =============================================================================
# =============================================================================

# =============================================================================
# Bid
# =============================================================================
#Create indidivdual column for each bid order
buy = {}
for k in range(1, 5):
    buy[k] = pd.DataFrame()
    for j in range(0, len(security[k].tradetime)):  
        mySecurity = []
        for i in range(0, len(security[k].tradetime)):
            if security[k].side[i] == 'BUY' and i == j and security[k].order[i] \
            < security[k].consumer[i]: 
                ms = security[k]['security' + str(k)][i]
            elif security[k].side[i] == 'BUY' and i == j and \
            security[k].consumer[i] == -1:
                ms = security[k]['security' + str(k)][i]
            else:
                ms = np.nan
            mySecurity.append(ms)
        buy[k][str(j)+ 'BUY'] = mySecurity

#Forward fill all lasting bids in market (where consumer == -1)
for k in range(1, 5):
    for i in range(0, len(security[k].tradetime)):
        if security[k].side[i] == 'BUY' and security[k].consumer[i] == -1:
            buy[k][str(i)+ 'BUY'] = buy[k][str(i)+ 'BUY'].fillna(method='pad')

#Find last entry index location for each bid that is cancelled &
#Find last entry index location for each bid that is traded 
indexcb = {}
indextb = {}

for k in range(1, 5):
    temp1 = []
    temp2 = []
    for i in range(len(security[k].side)):
        if security[k].side[i] == 'BUY':
            temp1 = security[k].loc[security[k]['type'] == 'CANCEL'].index.values.tolist()
            temp2 = security[k].loc[security[k]['trade'] == 1].index.values.tolist()
    xlst = []
    for i in range(len(temp1)):
        x = security[k].consumer[temp1[i]]
        xlst.append(x)
    indexcb[k] = pd.DataFrame()
    indexcb[k] = {'consumer': xlst, 'indexno': temp1}
    indexcb[k] = pd.DataFrame(indexcb[k])
    ylst = []
    for i in range(len(temp2)):
        y = security[k].consumer[temp2[i]]
        ylst.append(y)
    indextb[k] = pd.DataFrame()
    indextb[k] = {'consumer': ylst, 'indexno': temp2}
    indextb[k] = pd.DataFrame(indextb[k])

#Forward fill bids between submitted and cancelled 
bid = {}
for k in range(1, 5):
    bid[k] = pd.DataFrame()
    maxbid = []
    for i in range(len(indexcb[k].consumer)):
        temp1 = []
        for j in range(0, len(security[k].tradetime)):
            if indexcb[k].consumer[i] == security[k].order[j] and \
            security[k].side[j] == 'BUY':
                temp1 = indexcb[k].indexno[i] + 1
                buy[k][str(j)+ 'BUY'] = buy[k][str(j)+ 'BUY'].fillna(method='pad')[:temp1]
    for i in range(len(indextb[k].consumer)):
        temp2 = []
        for j in range(0, len(security[k].tradetime)):
            if indextb[k].consumer[i] == security[k].order[j] and \
            security[k].side[j] == 'BUY':
                temp2 = indextb[k].indexno[i] + 1
                buy[k][str(j)+ 'BUY'] = buy[k][str(j)+ 'BUY'].fillna(method='pad')[:temp2]
    maxbid = np.array(buy[k].max(axis=1))
    bid[k]['tradetime'] = security[k]['tradetime']
    bid[k]['trading_seconds'] = security[k]['trading_seconds']
    bid[k]['bid'] = maxbid

# =============================================================================
# Ask 
# =============================================================================
#Create indidivdual column for each ask order
sell = {}
for k in range(1, 5):
    sell[k] = pd.DataFrame()
    for j in range(0, len(security[k].tradetime)):  
        mySecurity = []
        for i in range(0, len(security[k].tradetime)):
            if security[k].side[i] == 'SELL' and i == j and security[k].order[i] \
            < security[k].consumer[i]: 
                ms = security[k]['security' + str(k)][i]
            elif security[k].side[i] == 'SELL' and i == j and \
            security[k].consumer[i] == -1:
                ms = security[k]['security' + str(k)][i]
            else:
                ms = np.nan
            mySecurity.append(ms)
        sell[k][str(j)+ 'SELL'] = mySecurity

#Forward fill all lasting bids in market (where consumer == -1)
for k in range(1, 5):
    for i in range(0, len(security[k].tradetime)):
        if security[k].side[i] == 'SELL' and security[k].consumer[i] == -1:
            sell[k][str(i)+ 'SELL'] = sell[k][str(i)+ 'SELL'].fillna(method='pad')

#Find last entry index location for each ask that is cancelled  &
#Find last entry index location for each ask that is traded 
indexcs = {}
indexts = {}

for k in range(1, 5):
    temp1 = []
    temp2 = []
    for i in range(len(security[k].side)):
        if security[k].side[i] == 'SELL':
            temp1 = security[k].loc[security[k]['type'] == 'CANCEL'].index.values.tolist()
            temp2 = security[k].loc[security[k]['trade'] == 1].index.values.tolist()
    xlst = []
    for i in range(len(temp1)):
        x = security[k].consumer[temp1[i]]
        xlst.append(x)
    indexcs[k] = pd.DataFrame()
    indexcs[k] = {'consumer': xlst, 'indexno': temp1}
    indexcs[k] = pd.DataFrame(indexcs[k])
    ylst = []
    for i in range(len(temp2)):
        y = security[k].consumer[temp2[i]]
        ylst.append(y)
    indexts[k] = pd.DataFrame()
    indexts[k] = {'consumer': ylst, 'indexno': temp2}
    indexts[k] = pd.DataFrame(indexts[k])

#Forward fill bids between submitted and cancelled 
ask = {}
for k in range(1, 5):
    ask[k] = pd.DataFrame()
    minask = []
    for i in range(len(indexcs[k].consumer)):
        temp1 = []
        for j in range(len(security[k].tradetime)):
            if indexcs[k].consumer[i] == security[k].order[j] and security[k].side[j] == 'SELL':
                temp1 = indexcs[k].indexno[i] + 1
                sell[k][str(j)+ 'SELL'] = sell[k][str(j)+ 'SELL'].fillna(method='pad')[:temp1]
    for i in range(len(indexts[k].consumer)):
        temp2 = []
        for j in range(len(security[k].tradetime)):
            if indexts[k].consumer[i] == security[k].order[j] and security[k].side[j] == 'SELL':
                temp2 = indexts[k].indexno[i] + 1
                sell[k][str(j)+ 'SELL'] = sell[k][str(j)+ 'SELL'].fillna(method='pad')[:temp2]
    minask = np.array(sell[k].min(axis=1))
    ask[k]['tradetime'] = security[k]['tradetime']
    ask[k]['trading_seconds'] = security[k]['trading_seconds']
    ask[k]['ask'] = minask
    
bidask = {}
for k in range(1, 5):
    bidask[k] = pd.concat([security[k], bid[k].bid, ask[k].ask], axis=1)

# =============================================================================
# =============================================================================
# # Determine average price at every 15/30 secs and create confidence interval at +/- 1 STD
# =============================================================================
# =============================================================================
# =============================================================================
# Create 30secs bins to calculate average price
# =============================================================================
timerange = np.arange(0, 630, 30)
bins = np.arange(30, 630, 30)
pcm = pd.DataFrame()
pcm['tradetime'] = timerange
securities = ['security1', 'security2', 'security3', 'security4']

df['bin'] = pd.cut(df.trading_seconds, timerange, labels = bins, \
  include_lowest=True).astype(float).to_frame()
df = df.reset_index(drop = True)

for n in range(4):
    mktmean = []
    mktstd = []
    for j in range(len(bins)):
        temp = []
        for i in range(len(df.bin)):
            if df.bin[i] == bins[j]:
                temp.append(df[securities[n]][i])
            else: 
                temp.append(np.nan)
            mean = np.nanmean(temp)
            z = np.count_nonzero(temp)
            if z != []:
                std = np.nanstd(temp, ddof=1)/math.sqrt(z)
        mktmean.append(mean)
        mktstd.append(std)
        if j == len(bins)-1:
            mktmean.append(mean)
            mktstd.append(std)
    pcm[securities[n]] = mktmean
    pcm[securities[n] + '-std'] = mktstd

# =============================================================================
# Calculate price convergence of each market using integration 
# =============================================================================
integrals = []
y1 = [100, 100, 100, 0]
y2 = [100, 0, 0, 0]
y3 = [100, 100, 100, 0]
y4 = [100, 100, 0, 0]
y5 = [100, 100, 100, 100]
y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y2}
pcm.tradetime = pcm.tradetime / 60

for i in range(1, 5):
    maxindex = pcm['security' + str(i)].last_valid_index()
    minindex = pcm['security' + str(i)].first_valid_index() 
    tempfile = pcm.loc[:maxindex, :]
    if minindex != 0: 
        tempfile = tempfile.replace(tempfile['security' + str(i)][0], 50)
        tempfile[:minindex] = tempfile.fillna(method = 'ffill')
        tempfile = tempfile.dropna(subset=['security' + str(i)])
    else: 
        tempfile = tempfile.dropna(subset=['security' + str(i)])
    if y[mk][i-1] == 100: 
        integral = integrate.simps(tempfile['security' + str(i)], tempfile.tradetime)
        brange = np.ones(len(tempfile['security' + str(i)]))*100
        bound = integrate.simps(brange, tempfile.tradetime)
        integral = bound - integral
    else: 
        integral = integrate.simps(tempfile['security' + str(i)], tempfile.tradetime)
    integrals.append(integral)

#Save price convergence as new file     
if nk == 2:
    marketpc = {}
marketpc[nk] = pd.DataFrame(integrals, columns = ['Problem' + str(mk)])

if nk == 6: 
    mktpc = pd.DataFrame()
    for k in range(2, 7):
        mktpc = mktpc.append(marketpc[k])
    mktpc.to_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/convergence-problem-' \
                 + str(mk) + '-v2.csv')

pcm.tradetime = pcm.tradetime * 60

# =============================================================================
# Plot Graphs
# =============================================================================
#Set Parameters
plt.figure(figsize=(6,4))
plt.xlabel('Trading Time (seconds)')
plt.ylabel('Price (cents)')
plotrange = np.arange(0,4)

c1 = ['limegreen', 'limegreen', 'limegreen', 'darkgreen']
c2 = ['limegreen', 'red', 'darkgreen', 'darkgreen']
c3 = ['darkorange', 'darkorange', 'darkred', 'darkorange']
c4 = ['limegreen', 'limegreen', 'darkgreen', 'darkgreen']
c5 = ['darkorange', 'darkorange', 'red', 'red']
c6 = ['limegreen', 'darkgreen', 'darkgreen', 'darkgreen']
color = {0: '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}

m1 = ['o', 'x', '^', 'o']
m2 = ['o', 'o', 'o', 'x']
m3 = ['o', 'x', 'o', '^']
m4 = ['o', 'x', 'o', 'x']
m5 = ['o', 'x', 'o', 'x']
m6 = ['o', 'o', 'x', '^']
marker = {0: '', 1: m1, 2: m2, 3: m3, 4: m4, 5: m5, 6: m6}

l1 = ['Security 72   = 100', 'Security 144 = 100', 'Security 164 = 100', 'Security 235 = 0']
l2 = ['Security 254 = 100', 'Security 296 = 0', 'Security 454 = 0', 'Security 494 = 0']
l3 = ['Security 871   = 100', 'Security 1000 = 100', 'Security 1160 = 100', 'Security 1251 = 0']
l4 = ['Security 288 = 100', 'Security 361 = 100', 'Security 577 = 0', 'Security 602 = 0']
l5 = ['Security 127 = 100', 'Security 203 = 100', 'Security 331 = 100', 'Security 409 = 100']
l6 = ['Security 361 = 100', 'Security 468 = 0', 'Security 489 = 0', 'Security 532 = 0']
label = {"": '', 1: l1, 2: l2, 3: l3, 4: l4, 5: l5, 6: l6}
 
y1 = [100.5, 100.9, 100.1, -0.1]
y2 = [100.1, -0.9, -0.5, -0.1]
y3 = [100.1, 100.5, 100.9, -0.1]
y4 = [100.1, 100.5, -0.1, -0.5]
y5 = [100.1, 100.5, 100.9, 101.3]
y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y2}
 
#Plot 
for i in plotrange:
    plt.title(str(m[mk]) + '-' + str(date) + str(e[mk]))
    plt.plot(df.trading_seconds, df['security' + str(i+1)],'o', \
                                    color= color[mk][i], markersize=5, \
                                    marker=marker[mk][i], label = label[mk][i])
    plt.axhline(y = y[mk][i], color = color[mk][i], linestyle='-', linewidth=1.5)
    plt.legend(bbox_to_anchor=(1, 0.7), loc=2, borderaxespad=0.25, \
               title="Securities and Payoffs")

plt.xlim(0, 600)
plt.show()
 
# =============================================================================
# Bid-ask Spread
# =============================================================================
#Set Parameters
fig = plt.figure(figsize=(15,10))

y1 = [100, 100, 100, 0]
y2 = [100, 0, 0, 0]
y3 = [100, 100, 100, 0]
y4 = [100, 100, 0, 0]
y5 = [100, 100, 100, 100]
y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y2}

#Plot 
for i in plotrange: 
    fig.subplots_adjust(hspace = 0.3)
    ax = fig.add_subplot(2,2, i+1)
    ax.plot(df.trading_seconds, df['security' + str(i+1)],'o', \
                                   color= color[mk][i], markersize=5, label = label[mk][i])
    ax.axhline(y = y[mk][i], color = color[mk][i], linestyle='-', linewidth=1)
    ax.plot(bidask[i+1].trading_seconds, bidask[i+1].bid, '|', markersize=9, \
            linestyle = '--', color= 'dodgerblue', label = '_nolegend_', \
            drawstyle='steps-post', linewidth=1)
    ax.plot(bidask[i+1].trading_seconds, bidask[i+1].ask, '|', markersize=9, \
            linestyle = '--', color= 'hotpink', label = '_nolegend_', \
            drawstyle='steps-post', linewidth=1)
    ax.set_xlabel('Trading Time (seconds)')
    ax.set_ylabel('Price (cents)')
    ax.set_xlim(0, 600)
    ax.set_ylim(-5, 105)
    ax.title.set_text(label[mk][i])
 
fig.suptitle('Bid-Ask Spread \n' + str(m[mk]) + '-' + str(date) + str(e[mk]), \
             fontsize = 16, y=0.95)
plt.show()
 
 
# =============================================================================
# Plot Individual Trading Data
# =============================================================================
#Set Parameters
fig = plt.figure(figsize=(40,32))
outer = gridspec.GridSpec(5, 4, wspace=0.2, hspace=0.2)
unique = pd.unique(df.owner)
unique = np.append(unique, [4852])
unique.sort()
plotrange = np.arange(len(unique))

y1 = [100.5, 100.9, 100.1, -0.1]
y2 = [100.1, -0.9, -0.5, -0.1]
y3 = [100.1, 100.5, 100.9, -0.1]
y4 = [100.1, 100.5, -0.1, -0.5]
y5 = [100.1, 100.5, 100.9, 101.3]
y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y2}

#Plot
for i in plotrange: 
    inner = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer[i], \
                                             wspace=0.25, hspace=0.3)
    tempfile = df.query('owner ==' + str(unique[i]))
    for j in range(4):
        ax = plt.Subplot(fig, inner[j])
        ax.plot(tempfile.trading_seconds, tempfile['security' + str(j+1)], \
                                                   color= color[mk][j], markersize=5, \
                                                   label = label[mk][j], linestyle='')
        ax.axhline(y = y[mk][j], color = color[mk][j], linestyle='-', linewidth=1)  
        tempfileba = bidask[j+1].query('owner ==' + str(unique[i]))
        if tempfileba.empty != True:  
            ax.plot(tempfileba.trading_seconds, tempfileba.bid, '|', \
                    markersize=9, linestyle = '--', color= 'dodgerblue', \
                    label = '_nolegend_', drawstyle='steps-post', linewidth=1)
            ax.plot(tempfileba.trading_seconds, tempfileba.ask, '|', \
                    markersize=9, linestyle = '--', color= 'hotpink', \
                    label = '_nolegend_', drawstyle='steps-post', linewidth=1)
        fig.add_subplot(ax)
        ax.set_xlim(0, 600)
        ax.set_ylim(-5, 105)
        if j == 0: 
            ax.title.set_text('Participant ' + str(i+1) + '\n' + str(label[mk][j]))
            ax.set_ylabel('Price (cents)')
        else: 
            ax.title.set_text(str(label[mk][j]))
        if j == 3:
            ax.set_xlabel('Trading Time (seconds)')
        else: 
            ax.set_xlabel('')

fig.suptitle('Individaul Bid-Ask Spread- ' + str(m[mk]) + '-' + str(date) \
             + str(e[mk]), fontsize = 16, y=0.91)
plt.show()


# =============================================================================
# Individual Trading Data v7.1
# =============================================================================
#fig = plt.figure(figsize=(25,20))
#unique = pd.unique(df.owner)
#unique = np.append(unique, [4852])
#unique.sort()
#plotrange = np.arange(len(unique))
#
#m1 = ['o', 'x', '^', 'o']
#m2 = ['o', 'o', 'o', 'x']
#m3 = ['o', 'x', 'o', 'o']
#m4 = ['o', 'x', 'o', 'o']
#m5 = ['o', 'x', 'o', 'x']
#m6 = ['o', 'o', 'x', '^']
#marker = {0: '', 1: m1, 2: m2, 3: m3, 4: m4, 5: m5, 6: m6}
#
#y1 = [100.5, 100.9, 100.1, -0.1]
#y2 = [100.1, -0.9, -0.5, -0.1]
#y3 = [100.1, 100.5, 100.9, -0.1]
#y4 = [100.1, 100.5, -0.1, -0.5]
#y5 = [100.1, 100.5, 100.9, 101.3]
#y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y2}
#
#for i in plotrange: 
#    fig.subplots_adjust(hspace = 0.3)
#    ax = fig.add_subplot(4,4, i+1)
#    tempfile = df.query('owner ==' + str(unique[i]))
#    for j in range(4):
#        ax.plot(tempfile.tradetime, tempfile['security' + str(j+1)], \
#                                             marker=marker[mk][j], color= color[mk][j], \
#                                             markersize=5, label = label[mk][j], linestyle='')
#        ax.axhline(y = y[mk][j], color = color[mk][j], linestyle='-', linewidth=1)  
#        tempfileba = bidask[j+1].query('owner ==' + str(unique[i]))
#        if tempfileba.empty != True:  
#            ax.plot(tempfileba.tradetime, tempfileba.bid, '|', markersize=9, \
#                    linestyle = '--', color= 'dodgerblue', label = '_nolegend_', \
#                    drawstyle='steps-post', linewidth=1)
#            ax.plot(tempfileba.tradetime, tempfileba.ask, '|', markersize=9, \
#                    linestyle = '--', color= 'hotpink', label = '_nolegend_', \
#                    drawstyle='steps-post', linewidth=1)
#        ax.set_xlabel('Trading Time')
#        ax.set_ylabel('Price (cents)')
#        ax.set_xlim(min(df.tradetime), maxtradetime)
#        ax.set_ylim(-5, 105)
#        ax.title.set_text('Participant ' + str(i+1))
#        if i == 7:
#            ax.legend(bbox_to_anchor=(1, 0.7), loc=2, borderaxespad=0.25, \
#                      title="Securities and Payoffs")
#
#fig.suptitle('Individaul Bid-Ask Spread- ' + str(m[mk]) + '-' + str(date) + str(e[mk]), \
#             fontsize = 16, y=0.95)
#plt.show()


# =============================================================================
# Save as new Dataframe
# =============================================================================
#Create new dataframe
dt = df[['tradetime','security1', 'security2','security3', 'security4', 'trading_seconds']]
#print(dt)

dt.to_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/' + str(nk) + str(m[mk]) + '-adjusted.csv') 

for k in range(1, 5):
    bidask[k].to_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/' + str(nk) + str(m[mk]) \
          + 'bidask' + str(k) + '.csv')

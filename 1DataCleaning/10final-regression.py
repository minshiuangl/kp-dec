#Load packages
import pandas as pd
import numpy as np
import dask.dataframe as dd

# =============================================================================
# Load KP data   
# =============================================================================
#Renumber participant_id
df = {}
participants = {}
l = 0
for i in range(2, 7):
    df[i] = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/' + str(i) + 'KP-individual-moves-15.csv')
    df[i] = df[i].drop(columns=['Unnamed: 0'])
    participants[i] = np.unique(df[i].participant_id)
    if i != 2:
        l += len(participants[i-1])
    for k in range(len(participants[i])):
        if i == 2: 
            df[i].participant_id = np.where(df[i].participant_id \
              == participants[i][k], int(k), df[i].participant_id)
        else: 
            df[i].participant_id = np.where(df[i].participant_id \
              == participants[i][k], int(k + l), df[i].participant_id)

#Combine Dataframes
dt = pd.DataFrame()
for i in range(2, 7):
    dt = dt.append(df[i], ignore_index=True)

dt.problem = dt['problem'].astype(int)
dt.participant_id = dt['participant_id'].astype(int)

problems = np.unique(dt.problem)

mask = dt['participant_id'] == 68
dt = dt[~mask]

participants = np.unique(dt.participant_id)

# =============================================================================
# Load Trading data
# =============================================================================
df = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-security-15.csv')
df = df.drop(columns=['Unnamed: 0'])
df.problem = df['problem'].astype(int)
df.participant_id = df['participant_id'].astype(int)
df = df.sort_values(by=['participant_id', 'problem'])

traded = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-traded-15.csv')
traded = traded.drop(columns=['Unnamed: 0'])

#Find number of participants in each problem, each session
td = pd.DataFrame()
s = np.unique(traded.session)
for i in range(len(s)):
    trade = pd.DataFrame()
    mask = traded['session'] == s[i]
    trade = traded[mask]
    temp = pd.DataFrame()
    mask = dt['session'] == s[i]
    temp = dt[mask]
    p = len(np.unique(temp.participant_id)) - 1
    trade = trade.append([trade]*p, ignore_index=True)
    td = td.append(trade)

td.session = td['session'].astype(int)    
traded = td.sort_values(by=['session', 'problem', 'security'])

#Repeat knapsack problem data for four individual securities
td = pd.DataFrame()
for i in range(len(participants)):
    temp = pd.DataFrame()
    mask = dt['participant_id'] == participants[i]
    temp = dt[mask]
    temp = temp.append([temp]*3, ignore_index=True)
    td = td.append(temp)
    
dt = td.sort_values(by=['participant_id', 'problem'])

# =============================================================================
# Merge Datasets
# =============================================================================
dt = dt.reset_index(drop=True)
df = df.reset_index(drop=True)
data = dd.merge(dt, df, left_index=True, right_index=True)
data = data.drop(columns=['tradetime_y', 'problem_y', \
                          'participant_id_y', 'session_y'])
data = data.rename(columns={'tradetime_x': 'tradetime', \
                            'problem_x': 'problem', 'participant_id_x': \
                            'participant_id', 'session_x': 'session'})

data = data.sort_values(by=['session', 'problem', 'security'])
    
traded = traded.reset_index(drop=True)
data = dd.merge(data, traded, left_index=True, right_index=True)
data = data.drop(columns=['tradetime_y', 'problem_y', 'session_y', 'security_y', \
                          'complexity_y'])
data = data.rename(columns={'tradetime_x': 'tradetime', 'problem_x': 'problem', \
                            'session_x': 'session', 'security_x': 'security',
                            'complexity_x': 'complexity'})
    
#Convert price data from cents to dollars
data.bid = data.bid / 100
data.ask = data.ask / 100
data.tradeprice = data.tradeprice / 100
data.marketbid = data.marketbid / 100
data.marketask = data.marketask / 100
data.tradeprice_lag = data.tradeprice_lag / 100
data.marketbid_lag = data.marketbid_lag / 100
data.marketask_lag = data.marketask_lag / 100
data.change_in_tradeprice = data.change_in_tradeprice / 100
data.change_in_marketbid = data.change_in_marketbid / 100
data.change_in_marketask = data.change_in_marketask / 100

data.to_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-data-15.csv')


# =============================================================================
# Create new variables for regression
# =============================================================================
y1 = [72, 144, 164, 235]
y2 = [254, 296, 454, 494]
y3 = [871, 1000, 1160, 1251]
y4 = [288, 361, 577, 602]
y5 = [127, 203, 331, 409]
y6 = [361, 468, 489, 532]
y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y6}

c1 = [3, 4, 2, 1]
c2 = [3, 4, 1, 2]
c3 = [1, 2, 4, 3]
c4 = [3, 4, 2, 1]
c5 = [1, 2, 3, 4]
c6 = [4, 3, 2, 1]
c = {"": '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}

p1 = [1, 1, 1, 0]
p2 = [1, 0, 0, 0]
p3 = [1, 1, 1, 0]
p4 = [1, 1, 0, 0]
p5 = [1, 1, 1, 1]
p = {"": '', 1: p1, 2: p2, 3: p3, 4: p4, 5: p5, 6: p2}

y0 = [164, 254, 1160, 549, 409, 464]
p0 = [0, 1, 1, 0, 1, 0]

file = pd.DataFrame()       
for n in range(len(problems)):
    temp = pd.DataFrame()
    mask = data['problem'] == problems[n]
    temp = data[mask]
    temp = temp.reset_index(drop=True)
    
    #Create dummy variables for positive market bid/price
    temp['ten'] = np.where((temp['tradeprice'] >= 0.1) | (temp['marketask'] >= 0.1), 1, 0)
    temp['twenty'] = np.where((temp['tradeprice'] >= 0.2) | (temp['marketask'] >= 0.2), 1, 0)
    temp['fifty'] = np.where((temp['tradeprice'] >= 0.5) | (temp['marketbid'] >= 0.5), 1, 0)
    temp['eighty'] = np.where((temp['tradeprice'] >= 0.8) | (temp['marketbid'] >= 0.8), 1, 0)
    temp['ninety'] = np.where((temp['tradeprice'] >= 0.9) | (temp['marketbid'] >= 0.9), 1, 0)
    
    #Set dummies for positive trade price, bids and asks
    temp['positive_change_tradeprice'] = np.where(temp['change_in_tradeprice'] > 0, 1, 0)
    temp['positive_change_marketbid'] = np.where(temp['change_in_marketbid'] > 0, 1, 0)
    temp['positive_change_marketask'] = np.where(temp['change_in_marketask'] > 0, 1, 0)
    
    #Set dummay for positive trade price
    temp['positive_tradeprice'] = np.where(temp['tradeprice'] > 0, 1, 0)

    tempf = pd.DataFrame()
    for i in range(0, 4):
        tempfile = pd.DataFrame()
        mask = temp['security'] == int(i+1)
        tempfile = temp[mask]
        tempfile = tempfile.reset_index(drop=True)
        
        #Create dummay variables for complexity ranking within a problem
        tempfile['sec_complexity'] = np.nan
        tempfile['sec_complexity'] = tempfile['sec_complexity'].fillna(c[n+1][i])
        
        #Set dummay for security that pays off
        tempfile['payoff'] = np.nan
        tempfile['payoff'] = tempfile['payoff'].fillna(p[n+1][i])

        #Set variable that measures effort: var = [threshold of security - running maximum]/threshold] <- normalised
        tempfile['var'] = (tempfile['cummax'] / y[n+1][i]) - 1
        tempfile['var_opt'] = (tempfile['cummax'] / y0[n]) - 1
        tempfile['var'] = tempfile['var'].astype(float)
        tempfile['var_opt'] = tempfile['var_opt'].astype(float)
         
        #Set dummies for positive differences
        tempfile['positive_var'] = np.where(tempfile['var'] > 0, 1, 0)
        tempfile['negative_var'] = np.where(tempfile['var'] < 0, 1, 0)
        tempfile['negative_var_opt'] = np.where(tempfile['var_opt'] < 0, 1, 0)
        tempfile['positive_var_opt'] = np.where(tempfile['var_opt'] >= 0, 1, 0)
        
        #Set dummaies for positive trade price in next security predicting no. of moves
        if i != 0: 
            tempfile['security_positive_var'] = np.where(tempfile['cummax'] >= y[n+1][i-1], 1, 0)
        
        #Set variable for bids and asks
        if i != 3: 
            tempfile['var_bid'] = np.where(tempfile['cummax'] >= y[n+1][i+1], (tempfile['cummax'] - y[n+1][i+1])/y[n+1][i+1], 0)
            tempfile['var_ask'] = np.where(tempfile['cummax'] < y[n+1][i+1], (y[n+1][i+1] - tempfile['cummax'])/y[n+1][i+1], 0)
        
        part = np.unique(tempfile.participant_id)
        tp = pd.DataFrame()
        
        #Set variable for change in var and var_opt
        for j in range(len(part)):
            t = pd.DataFrame()
            mask = tempfile.participant_id == part[j]
            t = tempfile[mask]
            t['var_lag'] = t['var'].shift(1)
            t['var_opt_lag'] = t['var_opt'].shift(1)
            t['change_in_var'] = t['var'] - t['var_lag']
            t['change_in_var_opt'] = t['var_opt'] - t['var_opt_lag']
            if i != 3: 
                t['var_bid_lag'] = t['var_bid'].shift(1)    
                t['var_ask_lag'] = t['var_ask'].shift(1)
                t['change_in_var_bid'] = t['var_bid'] - t['var_bid_lag']
                t['change_in_var_ask'] = t['var_ask'] - t['var_ask_lag']
            tp = tp.append(t)
    
        tempf = tempf.append(tp)
    
    file = file.append(tempf)

dt = file
dt.problem = dt['problem'].astype(int)
dt.participant_id = dt['participant_id'].astype(int)
dt.security = dt['security'].astype(int)

dt.to_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-security-reg-15.csv')
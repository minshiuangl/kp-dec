#Load packages
import pandas as pd
import numpy as np

# =============================================================================
# Set Bins
# =============================================================================
timerange = np.arange(0, 605, 5)
bins = np.arange(5, 605, 5)

# =============================================================================
# Load Trading data
# =============================================================================
m = ['', 'Ant', 'Beaver', 'Camel', 'Dolphin', 'Elephant', 'Frog']
f = {}
file = {}
for nk in range(2, 7):
    file[nk] = pd.DataFrame()
    for mk in range(1, 7): 
        for k in range(0, 4):
            f[k] = [str(nk) + str(m[mk]) + 'bidask' + str(k+1)]
            file[nk] = file[nk].append(f[k])
    file[nk] = file[nk].reset_index(drop=True)
    file[nk].columns = ['name']

prob = np.sort([ int(i) for i in [1, 2, 3, 4, 5, 6] * 4])
sec = [ int(i) for i in [1, 2, 3, 4] * 6]
 
df = pd.DataFrame()
participants = {}
l = 0
tempfile = {}
for j in range(2, 7):
    tempfile[j] = pd.DataFrame()
    for i in range(len(file[j].name)):
        temp = pd.read_csv('/Users/MLEE/Desktop/KP-DEC-Python-Results/' \
                           + str(file[j].name[i]) + '.csv')
        temp = temp.drop(columns=['Unnamed: 0'])
        temp = temp.rename(columns={"security" + str(sec[i]):"tradeprice"})
        temp['tradeprice'] = np.where(temp.trade == 1, temp.tradeprice, np.nan)
        temp['security'] = sec[i]
        temp['problem'] = np.nan
        temp['problem'] = temp['problem'].fillna(int(prob[i]))
        tempfile[j] = tempfile[j].append(temp, ignore_index=True)
    tempfile[j]['session'] = np.nan
    tempfile[j]['session'] = tempfile[j]['session'].fillna(int(j-1))
    tempfile[j]['participant_id'] = np.nan 
    participants[j] = np.unique(tempfile[j].owner)
    if j == 5: 
        participants[j] = np.insert(participants[j], 13, 0)
    if j != 2:
        l += len(participants[j-1])
    for k in range(len(participants[j])):
        if j == 2: 
            tempfile[j].participant_id = np.where(tempfile[j].owner \
                    == participants[j][k], int(k), tempfile[j].participant_id)
        else: 
            tempfile[j].participant_id = np.where(tempfile[j].owner \
                    == participants[j][k], int(k + l), tempfile[j].participant_id)
    df = df.append(tempfile[j], ignore_index=True)

df.problem = df.problem.astype(int)

df['bin'] = pd.cut(df.trading_seconds, timerange, labels = bins, \
  include_lowest=True).astype(float).to_frame()

df = df.sort_values(['session', 'problem', 'security','tradetime'])
df.to_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-traded-5-raw.csv')

# =============================================================================
# Count number of bids and asks per 1 sec bin per security per session
# =============================================================================
#Complexity category
c1 = [2, 2, 2, 1]
c2 = [2, 4, 1, 1]
c3 = [3, 3, 4, 3]
c4 = [2, 2, 1, 1]
c5 = [3, 3, 4, 4]
c6 = [2, 1, 1, 1]
c = {"": '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}

dt = pd.DataFrame()
for k in range(1, 5):
    mask = df.security == int(k)
    file = df[mask]
    problems = np.unique(file.problem)
    act = pd.DataFrame()
    for o in range(len(problems)):
        tempfile = file.query('problem ==' + str(problems[o]))
        temp = pd.DataFrame({'tradetime': timerange})
        temp['problem'] = np.nan
        temp['problem'] = temp['problem'].fillna(int(problems[o]))
        session = np.unique(df.session)
        for m in range(len(session)):
            tempf = tempfile.query('session ==' + str(session[m]))
            tempf = tempf.reset_index(drop=True)
            trade = []
            tradeact = []
            bid = []
            bidact = []
            ask = []
            askact = []
            tf = pd.DataFrame()
            tempbid = pd.DataFrame()
            tempask = pd.DataFrame()
            tempprice = pd.DataFrame()
            for j in range(len(bins)):
                mask = tempfile['bin'] == bins[j]
                tf = tempfile[mask]
                if tf.empty != True:
                    mask = tf['tradeprice'].isna()
                    tempprice = tf[~mask]
                    mask = tf['bid'].isna()
                    tempbid = tf[~mask]
                    mask = tf['ask'].isna()
                    tempask = tf[~mask]
                    trade.append(tempprice['tradeprice'].mean())
                    bid.append(tempbid['bid'].mean())
                    bidact.append(tempbid['bid'].count())
                    tradeact.append(tempprice['tradeprice'].count())
                    ask.append(tempask['ask'].mean())
                    askact.append(tempask['ask'].count())
                else: 
                    trade.append(np.nan)
                    tradeact.append(np.nan)
                    bid.append(np.nan)
                    bidact.append(0)
                    ask.append(np.nan)
                    askact.append(0)
                if j == len(bins)-1:
                    trade.append(np.nan)
                    tradeact.append(0)
                    bid.append(np.nan)
                    bidact.append(0)
                    ask.append(np.nan)
                    askact.append(0)
            temp['tradeprice'] = trade
            temp['tradecount'] = tradeact
            temp['marketbid'] = bid
            temp['marketbidcount'] = bidact
            temp['marketask'] = ask
            temp['marketaskcount'] = askact
            temp['complexity'] = np.nan
            temp['complexity'] = temp['complexity'].fillna(c[o+1][k-1])
            temp['session'] = np.nan
            temp['session'] = temp['session'].fillna(session[m])
            if temp['tradeprice'].empty == True:
                temp['tradeprice'] = np.nan
            if temp['tradecount'].empty == True:
                temp['tradecount'] = np.nan
            if temp['marketbid'].empty == True:
                temp['marketbid'] = np.nan
            if temp['marketbidcount'].empty == True:
                temp['marketbidcount'] = np.nan
            if temp['marketask'].empty == True:
                temp['marketask'] = np.nan
            if temp['marketaskcount'].empty == True:
                temp['marketaskcount'] = np.nan
            
            #Change in market prices, bids and asks
            temp['tradeprice_lag'] = temp.tradeprice.shift(1)
            temp['change_in_tradeprice'] = temp['tradeprice'] - temp['tradeprice_lag']
            temp['marketbid_lag'] = temp.marketbid.shift(1)
            temp['change_in_marketbid'] = temp['marketbid'] - temp['marketbid_lag']
            temp['marketask_lag'] = temp.marketask.shift(1) 
            temp['change_in_marketask'] = temp['marketask'] - temp['marketask_lag']
                
            act = act.append(temp)
    act['security'] = np.nan
    act['security'] = act['security'].fillna(int(k))
    dt = dt.append(act, ignore_index=True)

dt.problem = dt['problem'].astype(int)
dt.security = dt['security'].astype(int)

dt.to_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-traded-5.csv')

# =============================================================================
# Count number of bids and asks per 1 sec bin per security per participant
# =============================================================================
lst1 = [19, 19, 17, 14, 19]
lst2 = [1, 2, 3, 4, 5]
session = []
for j in range(len(lst2)):
    session += [lst2[j]]*lst1[j]
 
data = pd.DataFrame()
for k in range(1, 5):
    mask = df.security == int(k)
    file = df[mask]
    act = pd.DataFrame()
    participants = np.unique(file.participant_id)
    problems = np.unique(file.problem)
    for o in range(len(problems)):
        tempf = file.query('problem ==' + str(problems[o]))
        for n in range(len(participants)):
            temp = pd.DataFrame({'tradetime': timerange})
            temp['participant_id'] = np.nan
            temp['participant_id'] = temp['participant_id'].fillna(int(participants[n]))
            temp['session'] = np.nan
            temp['session'] = temp['session'].fillna(int(session[n]))
            temp['problem'] = np.nan
            temp['problem'] = temp['problem'].fillna(int(problems[o]))
            activity = []
            tempfile = tempf.query('participant_id ==' + str(participants[n]))
            tempfile = tempfile.reset_index(drop=True)
            bid = []
            ask = []
            bidact = []
            askact = []
            tf = pd.DataFrame()
            tempbid = pd.DataFrame()
            tempask = pd.DataFrame()
            for j in range(len(bins)):
                mask = tempfile['bin'] == bins[j]
                tf = tempfile[mask]
                if tf.empty != True:
                    mask = tf['bid'].isna()
                    tempbid = tf[~mask]
                    mask = tf['ask'].isna()
                    tempask = tf[~mask]
                    bid.append(tempbid['bid'].mean())
                    bidact.append(tempbid['bid'].count())
                    ask.append(tempask['ask'].mean())
                    askact.append(tempask['ask'].count())
                else: 
                    bid.append(np.nan)
                    bidact.append(0)
                    ask.append(np.nan)
                    askact.append(0)
                if j == len(bins)-1:
                    bid.append(np.nan)
                    ask.append(np.nan)
                    bidact.append(0)
                    askact.append(0)
            temp['bid'] = bid
            temp['ask'] = ask
            temp['bidcount'] = bidact
            temp['askcount'] = askact
            temp['complexity'] = np.nan
            temp['complexity'] = temp['complexity'].fillna(c[o+1][k-1])
            act = act.append(temp)
    act['security'] = np.nan
    act['security'] = act['security'].fillna(int(k))
    data = data.append(act, ignore_index=True)

data.problem = data['problem'].astype(int)
data.participant_id = data['participant_id'].astype(int)
data.security = data['security'].astype(int)

data.to_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-security-5.csv')

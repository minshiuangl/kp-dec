#Load packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import math

#Load files
dt = pd.read_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/priceconvergence-norm-15.csv')
dt = dt.drop(columns=['Unnamed: 0'])
df = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-security-15.csv')

bidcounttotal = []
askcounttotal = []

for j in range(6):
    mask = df.problem == int(j+1)
    temp = df[mask]
    for i in range(4):
        mask = df.security == int(i+1)
        tempfile = temp[mask]
        bidcounttotal.append(tempfile['bidcount'].sum())
        askcounttotal.append(tempfile['askcount'].sum())
    
dt['bidcounttotal'] = bidcounttotal
dt['askcounttotal'] = askcounttotal

c1 = [10, 11, 9, 4]
c2 = [13, 105, 2, 2]
c3 = [16, 16, 339, 18]
c4 = [12, 12, 2, 2]
c5 = [15, 16, 41, 65]
c6 = [11, 2, 2, 2]
c = {"": '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}

p1 = [3, 4, 2, 1]
p2 = [3, 4, 1, 2]
p3 = [1, 2, 4, 3]
p4 = [3, 4, 2, 1]
p5 = [1, 2, 3, 4]
p6 = [4, 3, 2, 1]
p = {"": '', 1: p1, 2: p2, 3: p3, 4: p4, 5: p5, 6: p6}

p0 = [0, 1, 1, 0, 1, 0]

file = pd.DataFrame()
for j in range(6):
    mask = dt.problem == int(j+1)
    temp = dt[mask]
    temp['hard'] = np.nan
    temp['hard'] = temp['hard'].fillna(p0[j])
    for i in range(4):
        mask = dt.security == int(i+1)
        tempfile = temp[mask]
        tempfile['propagation'] = np.nan
        tempfile['propagation'] = tempfile['propagation'].fillna(c[j+1][i])
        tempfile['sec_complexity'] = np.nan
        tempfile['sec_complexity'] = tempfile['sec_complexity'].fillna(p[j+1][i])
        file = file.append(tempfile)

dt = file
dt['marketactivity'] = dt['bidcounttotal'] + dt['askcounttotal']
dt['normalised_marketactivity'] = dt.price_convergence / dt['marketactivity']
    
dt.to_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/priceconvergence-final-15.csv')


# =============================================================================
# Plot Graph
# =============================================================================
data = pd.read_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/priceconvergence-final-15.csv')
data = data.sort_values(by=['problem', 'security'])
data.security = data.security.astype(int)

c1 = ['limegreen', 'limegreen', 'limegreen', 'darkgreen']
c2 = ['limegreen', 'red', 'darkgreen', 'darkgreen']
c3 = ['darkorange', 'darkorange', 'darkred', 'darkorange']
c4 = ['limegreen', 'limegreen', 'darkgreen', 'darkgreen']
c5 = ['darkorange', 'darkorange', 'red', 'red']
c6 = ['limegreen', 'darkgreen', 'darkgreen', 'darkgreen']
color = {0: '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}
marker = ['o', 'x', '^', 's', 'P', 'D']

#Plot Propagation vs. Normalised price convergence
fig = plt.figure(figsize=(8,8))
marker = ['o', 'x', '^', 's', 'P', 'D']
for i in range(6):
    mask = data.problem == int(i+1)
    temp = data[mask]
    temp = temp.reset_index(drop=True)
    for j in range(len(temp.security)):
        plt.scatter(math.log(temp.propagation[j]), temp.normalised_tradetime[j], \
                    color=color[i+1][j], marker=marker[i], linestyle='-', \
                     zorder=1)
    plt.xlabel('Log(Propagation)')
    plt.ylabel('Normalised Price Convergence by trade time')
    plt.yticks(np.arange(0, 45, step=5))
    plt.title('Relationship between Instance Complexity and Price Convergence')
    
patch1 = mpatches.Patch(color='darkgreen', label='Complexity 1')
patch2 = mpatches.Patch(color='limegreen', label='Complexity 2')
patch3 = mpatches.Patch(color='darkorange', label='Complexity 3')
patch4 = mpatches.Patch(color='red', label='Complexity 4')
patch5 = mpatches.Patch(color='darkred', label='Complexity 4: Hardest')

patcha = mlines.Line2D([], [], color = 'black', linestyle='None', marker='o', label='Problem 1')
patchb = mlines.Line2D([], [], color = 'black', linestyle='None', marker='x', label='Problem 2')
patchc = mlines.Line2D([], [], color = 'black', linestyle='None', marker='^', label='Problem 3')
patchd = mlines.Line2D([], [], color = 'black', linestyle='None', marker='s', label='Problem 4')
patche = mlines.Line2D([], [], color = 'black', linestyle='None', marker='P', label='Problem 5')
patchf = mlines.Line2D([], [], color = 'black', linestyle='None', marker='D', label='Problem 6')

plt.legend(handles=[patcha, patchb, patchc, patchd, patche, patchf, \
                    patch1, patch2, patch3, patch4, patch5], \
        bbox_to_anchor=(1, 1), loc=2) 

plt.show()



# =============================================================================
# Individual Price Convergence
# =============================================================================
#Load 
data = pd.DataFrame()
dt = {}
s = sorted([1, 2, 3, 4, 5]*4)
sec = [1, 2, 3, 4]*5
for i in range(1, 7):
    dt[i] = pd.read_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/convergence-market-' \
      + str(i) + '-15.csv')
    dt[i] = dt[i].drop(columns=['Unnamed: 0'])
    dt[i].columns = ['price_convergence', 'normalised_tradetime']
    dt[i]['problem'] = np.nan
    dt[i]['problem'] = dt[i]['problem'].fillna(i)
    dt[i]['session'] = s
    dt[i]['security'] = sec
    data = data.append(dt[i])

df = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-security-15.csv')

bidcounttotal = []
askcounttotal = []

for j in range(6):
    mask = df.problem == int(j+1)
    temp = df[mask]
    for i in range(4):
        mask = df.security == int(i+1)
        tempfile = temp[mask]
        bidcounttotal.append(tempfile['bidcount'].sum())
        askcounttotal.append(tempfile['askcount'].sum())
    
data['bidcounttotal'] = bidcounttotal*5
data['askcounttotal'] = askcounttotal*5

c1 = [10, 11, 9, 4]
c2 = [13, 105, 2, 2]
c3 = [16, 16, 339, 18]
c4 = [12, 12, 2, 2]
c5 = [15, 16, 41, 65]
c6 = [11, 2, 2, 2]
c = {"": '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}

p1 = [3, 4, 2, 1]
p2 = [3, 4, 1, 2]
p3 = [1, 2, 4, 3]
p4 = [3, 4, 2, 1]
p5 = [1, 2, 3, 4]
p6 = [4, 3, 2, 1]
p = {"": '', 1: p1, 2: p2, 3: p3, 4: p4, 5: p5, 6: p6}

p0 = [0, 1, 1, 0, 1, 0]

file = pd.DataFrame()
for j in range(6):
    mask = data.problem == int(j+1)
    temp = data[mask]
    temp['hard'] = np.nan
    temp['hard'] = temp['hard'].fillna(p0[j])
    for i in range(4):
        mask = temp.security == int(i+1)
        tempfile = temp[mask]
        tempfile['propagation'] = np.nan
        tempfile['propagation'] = tempfile['propagation'].fillna(c[j+1][i])
        tempfile['sec_complexity'] = np.nan
        tempfile['sec_complexity'] = tempfile['sec_complexity'].fillna(p[j+1][i])
        file = file.append(tempfile)

data = file
data['marketactivity'] = data['bidcounttotal'] + data['askcounttotal']
data['normalised_marketactivity'] = data.price_convergence / data['marketactivity']
    
data.to_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/priceconvergence-market-15.csv')


# =============================================================================
# Plot Graph
# =============================================================================
data = pd.read_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/priceconvergence-market-15.csv')
data = data.sort_values(by=['problem', 'security'])
data.security = data.security.astype(int)
data['normalised_tradetime'] = data['normalised_tradetime'].replace(0, np.nan)

c1 = ['darkorange', 'red', 'limegreen', 'darkgreen']
c2 = ['darkorange', 'red', 'darkgreen', 'limegreen']
c3 = ['darkgreen', 'limegreen', 'darkred', 'darkorange']
c4 = ['darkorange', 'red', 'limegreen', 'darkgreen']
c5 = ['darkgreen', 'limegreen', 'darkorange', 'red']
c6 = ['red', 'darkorange', 'limegreen', 'darkgreen']
color = {0: '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}
marker = ['o', 'x', '^', 's', 'P', 'D']

#Plot Propagation vs. Normalised price convergence
fig = plt.figure(figsize=(15,15))
marker = ['o', 'x', '^', 's', 'P', 'D']

for k in range(5):
    mask = data.session == int(k+1)
    session = data[mask]
    for i in range(6):
        mask = session.problem== int(i+1)
        temp = session[mask]
        temp = temp.reset_index(drop=True)
        for j in range(len(temp.security)):
            if pd.isnull(temp.normalised_tradetime[j]) == False:
                plt.scatter(math.log(temp.propagation[j]), temp.normalised_tradetime[j], \
                            color=color[i+1][j], marker=marker[i], linestyle='-', \
                            zorder=1)
    plt.xlabel('Log(Propagation)')
    plt.ylabel('Log(ncp)')
    plt.yticks(np.arange(0,1.3, step=0.2))
    plt.title('Relationship between Instance Complexity and Price Convergence (N=115)')
        
patch1 = mpatches.Patch(color='darkgreen', label='Difficulty 1')
patch2 = mpatches.Patch(color='limegreen', label='Difficulty 2')
patch3 = mpatches.Patch(color='darkorange', label='Difficulty 3')
patch4 = mpatches.Patch(color='red', label='Difficulty 4')
patch5 = mpatches.Patch(color='darkred', label='Difficulty 4: Hardest')

patcha = mlines.Line2D([], [], color = 'black', linestyle='None', marker='o', label='Problem 1')
patchb = mlines.Line2D([], [], color = 'black', linestyle='None', marker='x', label='Problem 2')
patchc = mlines.Line2D([], [], color = 'black', linestyle='None', marker='^', label='Problem 3')
patchd = mlines.Line2D([], [], color = 'black', linestyle='None', marker='s', label='Problem 4')
patche = mlines.Line2D([], [], color = 'black', linestyle='None', marker='P', label='Problem 5')
patchf = mlines.Line2D([], [], color = 'black', linestyle='None', marker='D', label='Problem 6')

plt.legend(handles=[patcha, patchb, patchc, patchd, patche, patchf, \
                    patch1, patch2, patch3, patch4, patch5], \
        bbox_to_anchor=(1, 1), loc=2) 

plt.show()
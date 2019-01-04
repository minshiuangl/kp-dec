#Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import math

# =============================================================================
# =============================================================================
# # Compute Trading across sessions 
# =============================================================================
# =============================================================================
df = {}
file = ['', str(2) + 'KP-individual-v2', str(3) + 'KP-individual-v2', str(4) + \
        'KP-individual-v2', str(5) + 'KP-individual-v2', str(6) + 'KP-individual-v2']

for i in range(1,6):
    df[i] = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-DEC Individual/'\
      + file[i] + '.csv')

# =============================================================================
# Combine Dataframes
# =============================================================================
dt = pd.DataFrame()
for i in range(1, 6):
    dt = dt.append(df[i])

dt = dt.sort_values(by = ['participant_id', 'problem_id', 'time_into_problem'])
dt = dt.reset_index(drop=True)
dt = dt.iloc[:, -14:]

# =============================================================================
# Create 1sec bins for Knapsack values
# =============================================================================
timerange = np.arange(0, 601, 1)
bins = np.arange(1, 601, 1)
kp = pd.DataFrame({'tradetime': timerange})
dt['bin'] = pd.cut(dt.time_into_problem, timerange, labels = bins, \
  include_lowest=True).astype(float).to_frame()
dt = dt.reset_index(drop = True)
problems = np.unique(dt.problem)

for n in range(len(problems)):
    file = dt.query('problem ==' + str(problems[n]))
    file = file.reset_index(drop = True)
    if file.empty == False:
        temp = file.drop_duplicates(subset = 'cummax', keep = 'first')
        temp = temp.reset_index(drop = True)
        mktmean = []
        act = []
        for i in range(len(kp.tradetime)):
            temp_lst = []
            for j in range(len(temp['cummax'])):
                if kp.tradetime[i] == temp.bin[j]:
                    temp_lst.append(temp['cummax'][j])
                mean = np.nanmean(temp_lst)
            mktmean.append(mean)
            act.append(len(temp_lst))
        kp['problem' + str(n+1)] = mktmean
        kp['problem-act' + str(n+1)] = act
        kp['problem' + str(n+1)] = kp['problem' + str(n+1)].cummax().to_frame()
        kp['problem' + str(n+1)] = kp['problem' + str(n+1)].fillna(method = 'ffill')
        kp['problem' + str(n+1)] = kp['problem' + str(n+1)].replace(np.nan, 0)

# =============================================================================
# Plot Graphs
# =============================================================================
#Set Parameters
fig = plt.figure(figsize=(18,20))
plotrange = np.arange(0,6)

y1 = [72, 144, 164, 235]
y2 = [254, 296, 454, 494]
y3 = [871, 1000, 1160, 1251]
y4 = [288, 361, 577, 602]
y5 = [127, 203, 331, 409]
y6 = [361, 468, 489, 532]
y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y6}

y0 = [164, 254, 1160, 549, 409, 464]

c1 = ['limegreen', 'limegreen', 'limegreen', 'darkgreen']
c2 = ['limegreen', 'red', 'darkgreen', 'darkgreen']
c3 = ['darkorange', 'darkorange', 'darkred', 'darkorange']
c4 = ['limegreen', 'limegreen', 'darkgreen', 'darkgreen']
c5 = ['darkorange', 'darkorange', 'red', 'red']
c6 = ['limegreen', 'darkgreen', 'darkgreen', 'darkgreen']
color = {0: '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}

fcolor = ['honeydew', 'honeydew', 'lightcoral', 'cornsilk', 'mistyrose', 'cornsilk']
c = ['limegreen', 'limegreen', 'darkred', 'grey', 'red', 'grey']
col = ['limegreen', 'limegreen', 'darkred', 'darkorange', 'red', 'darkorange']

#Set title for graphs
title = []
for i in range(0, 6):
    temp = 'KP Trial ' + str(i+1)
    title.append(temp)

ylim = [(-5, 300), (-5, 600), (-5, 1550), (-5, 750), (-5, 500), (-5, 650)]

#Plot
for i in plotrange: 
    fig.subplots_adjust(hspace = 0.2, wspace = 0.2)
    ax = fig.add_subplot(3,2, i+1)
#    ax.plot(kp.tradetime, kp['problem' + str(i+1)], '-', color= col[i], \
#                             markersize=3, linestyle='-', label = '_nolegend_')
    ax.plot(kp.tradetime, kp['problem-act' + str(i+1)], '-', color= col[i], \
                             markersize=3, linestyle='-', label = '_nolegend_')
    ax.set_xlabel('Time into Problem (secs)')
    ax.set_ylabel('No. of Moves in the Knapsack')
#    ax.set_ylabel('Value of Knapsack')
    ax.title.set_text(title[i])
    ax.set_xlim(-5, 600)
    ax.set_ylim(0, 60)
#    ax.set_ylim(ylim[i])
    
#    for j in range(0, 4):
#        ax.axhline(y = y[i+1][j], color = color[i+1][j], linestyle='--', \
#                   linewidth=0.5, label = y[i+1][j])
#    ax.axhline(y = y0[i], color = c[i], linestyle='-', linewidth=1, \
#               label = 'Optimal Solution: ' + str(y0[i]))
#    ax.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0.25, ncol = 3)

fig.suptitle('Average individual moves in the Knapsack task of each KP trial', \
             fontsize = 16, y=0.92)

#fig.suptitle('Average individual running maximum of the knapsack value in each KP trial', \
#             fontsize = 16, y=0.92)
plt.show()

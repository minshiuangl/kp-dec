#Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# =============================================================================
# #Compute Solvability of KP Instances across sessions
# =============================================================================
# =============================================================================
#Total of 87 participants (round up to closest even number)
n = 88
# =============================================================================
# Load relevant files 
# =============================================================================
df = {}
file = ['', str(2) + 'KP-v2', str(3) + 'KP-v2', str(4) + 'KP-v2', str(5) + 'KP-v2', str(6) + 'KP-v2']

for i in range(1,6):
    df[i] = pd.read_csv('/Users/MLEE/Desktop/KP-DEC-Python-Results/'+ file[i] + '.csv')
    df[i] = df[i].drop(columns=['Unnamed: 0', 'participant_id', 'problem_id', 'problem_value'])

# =============================================================================
# Combine dataframes
# =============================================================================
dt = pd.DataFrame()
for i in range(1, 6):
    dt = dt.append(df[i])

# =============================================================================
# #Create frequency table for each problem
# =============================================================================
tab_lst = []
maxpercent = []

for i in range(1,7): 
    tab = pd.crosstab(index=dt["problem" + str(i)], columns="count")
    tab_lst.append(tab)
    
ft = {}
for i in range(0,6): 
    ft[i] = tab_lst[i].reset_index()
    ft[i]['problem' + str(i+1)] = ft[i]['problem' + str(i+1)].astype(int)
    ft[i]['problem' + str(i+1)] = ft[i]['problem' + str(i+1)].astype(str)
    ft[i]['problem'] = np.array('problem' + str(i+1))
    if i == 2: 
        ft[i]['problem' + str(i+1)] = ft[i].replace(['800'], [' ' + '800'])
    elif i == 0: 
        ft[i]['problem' + str(i+1)] = ft[i].replace(['65'], [' ' + '65'])

#summary = pd.DataFrame()
#for i in range(0,6): 
#    summary = summary.append(ft[i])
#summary.to_csv('/Users/MLEE/desktop/summary.csv')
    
stats = dt.describe().transpose()

# =============================================================================
#     #Plot Histogram for each problem 
# =============================================================================
fig = plt.figure(figsize=(18,20))

for i in range(1, 7): 
    fig.subplots_adjust(hspace = 0.2)
    ax = fig.add_subplot(3,2, i)
    axplt = ax.bar(ft[i-1]['problem' + str(i)], ft[i-1]['count'])
    ax.set_xlabel('Submitted knapsack value')
    ax.set_ylabel('No. of subjects who found the optimal solution')
    ax.title.set_text('Problem ' + str(i))
    ax.set_yticks(np.arange(0, 86, step=5))
    ax.set_ylim(0, 85)
    for rect in axplt:
        height = rect.get_height()
        percent = height / 87 * 100
        percent = str(round(percent, 2)) + '%'
        ax.text(rect.get_x() + rect.get_width()/2.0, height, '%s' % str(percent), \
                ha='center', va='bottom', fontsize=12)

fig.suptitle('Instance Solvability of the KP-DEC', fontsize = 16, y=0.92)
plt.show()

# =============================================================================
#   #Plot Box and Whiskers Plot for Summary Statistics 
# =============================================================================
#data.columns = ['Problem 1', 'Problem 2', 'Problem 3', 'Problem 4', 'Problem 5', 'Problem 6']
#data = data.reindex(columns = ['Problem 6', 'Problem 5', 'Problem 4', 'Problem 3', 'Problem 2', 'Problem 1'])
#ax = data.plot(kind = 'box', vert = False, grid = True, figsize= (10,5), sym='o')
#
#major_ticks = np.arange(0, 1250, 100)
#minor_ticks = np.arange(0, 1250, 20)
#
#ax.set_xticks(major_ticks)
#ax.set_xticks(minor_ticks, minor=True)
#
## And a corresponding grid
#ax.grid(which='both')
#
## Or if you want different settings for the grids:
#ax.grid(which='minor', alpha=0.2)
#ax.grid(which='major', alpha=0.5)
#
#ax.set_xlabel('Submitted Value')
#
#ax.title.set_text('Solvability of Knapsack Problems by Participants Across Sessions')
#
#plt.show()

#stats.to_csv('/Users/MLEE/desktop/Solvability of KP Across Sessions.csv')


#Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# =============================================================================
# Compute Solvability of each Knapsack Instances in each Session
# =============================================================================

# =============================================================================
# Load relevant files
# =============================================================================
#No. of Participants (round up to closest even number) in each session
    #19, 19, 17, 13, 19
n = ['', '', 20, 20, 18, 14, 20]

#Load csv file
df = {}
k = 2
file = ['', str(k) + 'KP', str(k) + 'KPItems', 'Itemvalues']

for i in range(1,4):
    df[i] = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/'+ file[i] + '.csv')
    
#Drop unnecessary columns in df3
df[2] = df[2].drop(columns = ['submitted_item_id', 'start_pos_x', 'start_pos_y', 'pixel_size'])

# =============================================================================
# Set Date
# =============================================================================
if k != 2: 
    date = df[1].time_started[0]
    date = date.partition(' ')[0]
    datetime.datetime.strptime(date, '%Y-%m-%d')
else: 
    date = df[1].time_started[0]
    date = date.partition(' ')[0]
    date = date.split('/')[::-1]
    date = str(20) + date[0] + '-' + str(0) + date[1] + '-' + date[2]
    datetime.datetime.strptime(date, '%Y-%m-%d')

#Remove columns: time_started, interventions_available and interventions_used
df[1] = df[1].drop(columns=['interventions_available','interventions_used', 'time_started'])

# =============================================================================
# #Match item id with item value, if item is in knapsack
# =============================================================================
myitem = []

for i in range(len(df[2].item_id)):
    for j in range(len(df[3].item_id)):
        if df[2].item_id[i] == df[3].item_id[j]:
            trial = df[3].item_value[j]*df[2].in_knapsack[i]
    myitem.append(trial)

df[2]['item_value'] = myitem

# =============================================================================
# #Determine total value for each problem submitted 
# =============================================================================
total = df[2].groupby('submitted_problem_id').sum()
total = pd.DataFrame(total.item_value)
total.reset_index(drop = True, inplace = True)

#Match total value of problem to participant
df[1]['problem_value'] = total

#Find maximum value submitted by each participant for each problem
maxproblem = df[1].groupby(['participant_id', 'problem_id']).agg({'problem_value':'max'})
mp = pd.DataFrame(maxproblem.problem_value)
mp = mp.reset_index()

a = np.array(range(0, 7))
b = np.array(range(11, 17+1))

myproblem = []

for i in range(len(mp)):
    for j in a: 
        if mp.problem_id[i] == b[j]:
            mpi = a[j] 
    myproblem.append(mpi)

mp.problem_id = myproblem

# =============================================================================
# #Create a new column for each problem
# =============================================================================
temp_lst = []

for i in range(len(mp)):
    for j in a: 
        if mp.problem_id[i] == a[j]:
            mpv = mp.problem_value[i]
    temp_lst.append(mpv)

for i in a: 
    mp['problem' + str(i)] = temp_lst
    
mp = mp.drop(columns = ['problem0'])

# =============================================================================
# #Replace cells that do not correspond to the problem column with NaN
# =============================================================================
problem = range(0, 7)

for l in range(1, 7):
    temp_lst = []
    temp = []
    for i in range(len(mp)):
        if mp.problem_id[i] != problem[l]:
            temp = mp['problem' + str(l)].replace(mp['problem' + str(l)][i], np.nan, inplace=True)
        else: 
            temp = mp['problem' + str(l)][i]
        temp_lst.append(temp)
    mp['problem' + str(l)] = temp_lst

#Drop unnecessary rows (for session 3)
mp = mp.drop(mp.index[133]) if k == 3 else mp
mp = mp.drop(mp.index[91]) if k == 5 else mp
mp = mp.drop(mp.index[90]) if k == 5 else mp
mp = mp.drop(mp.index[131]) if k == 6 else mp

# =============================================================================
# #Replace participant_id with numbers
# =============================================================================
myID = []

j = np.arange(0,26)
c = np.arange(1, 25)
x = 258 + j

for i in range(0, len(mp.participant_id)):
    for t in j:
        if mp.participant_id[i] == x[t]: 
            temp = c[t]
    myID.append(temp)
    
mp.participant_id = myID


# =============================================================================
# #Plot Graph
# =============================================================================
plt.figure(figsize=(13,8))
plt.xlabel('Participant')
plt.xticks(mp.participant_id)
plt.yticks()
plt.ylabel('Max. value of Knapsack solution submitted')

plotrange = np.arange(0,6)

maxy = [164, 254, 1160, 549, 409, 464]
color = ['darkgreen', 'orangered', 'red', 'limegreen', 'red', 'green']

for i in plotrange:
    plt.title('Solvability of Knapsack Problems by Participants ' + str(date))
    plt.scatter(mp.participant_id, mp['problem'+ str(i+1)], color = color[i], label = 'problem' + str(i+1) + ' - ' + str(maxy[i]))
    plt.axhline(y=maxy[i], color = color[i], linestyle='-', linewidth=1)
    plt.legend(bbox_to_anchor=(1, 0.8), loc=2, borderaxespad=0.25)

plt.show()


# =============================================================================
# #Create frequency table for each problem
# =============================================================================
tab_lst = []

for i in range(1,7): 
    tab = pd.crosstab(index=mp["problem" + str(i)], columns="count")
    tab_lst.append(tab)

ft = {}

for i in plotrange: 
    ft[i] = tab_lst[i].reset_index()
    ft[i]['problem' + str(i+1)] = ft[i]['problem' + str(i+1)].astype(int)
    ft[i]['problem' + str(i+1)] = ft[i]['problem' + str(i+1)].astype(str)
    if k == 2 and i == 2: 
        ft[i]['problem' + str(i+1)] = ft[i].replace(['800'], [' ' + '800'])
    elif k == 3 and i == 0: 
        ft[i]['problem' + str(i+1)] = ft[i].replace(['65'], [' ' + '65'])
    elif k == 5 and i == 0: 
        ft[i]['problem' + str(i+1)] = ft[i].replace(['65'], [' ' + '65'])
        

# =============================================================================
#     #Plot Histogram for each problem 
# =============================================================================
fig = plt.figure(figsize=(15,10))

title = ['-EASY','-HARD','-HARD','-EASY','-HARD','-EASY']

for i in range(1, 7): 
    fig.subplots_adjust(hspace = 0.3)
    ax = fig.add_subplot(2,3, i)
    ax.bar(ft[i-1]['problem' + str(i)], ft[i-1]['count'])
    ax.set_xlabel('Submitted Value')
    ax.set_ylabel('Frequency (no. of participants)')
    ax.title.set_text('Problem ' + str(i) + title[i-1])
    ax.set_yticks(np.arange(0, n[k], step=2))

fig.suptitle('Solvability of Knapsack Problems by Participants ' + str(date), fontsize = 16, y=0.95)
plt.show()


mp.to_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/' + str(k) + 'KP-v2.csv')

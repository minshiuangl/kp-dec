#Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# =============================================================================
# Load csv file for each session
# =============================================================================
#Select session
nk = 5
df = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-DEC Individual/' \
                 + str(nk) + 'KP-individual.csv')

df = df.sort_values(by = ['problem', 'submitted_item_move_id'])

participants = np.unique(df.participant_id)
problems = np.unique(df.problem)

# =============================================================================
# Delete values that are above the optimal solution
# =============================================================================
kp = pd.DataFrame()
y = [164, 254, 1160, 549, 409, 464]

for k in range(len(problems)):
    tempfile = df.query('problem ==' + str(problems[k]))
    tempfile = tempfile.sort_values(by = ['submitted_item_move_id'])
    tempfile = tempfile.reset_index(drop = True)
    index = tempfile.loc[tempfile['problem_value'] > y[k]].index.values.tolist()
    if index != []:
        for i in range(len(index)):
            tempfile.loc[index[i], 'problem_value'] = tempfile.problem_value[index[i]-1]
    elif index == []: 
        tempfile = tempfile
    kp = kp.append(tempfile)

df = kp

# =============================================================================
# Combine multiple submissions from each participants
# =============================================================================
myTime = []
kp = pd.DataFrame()

for k in range(len(participants)):
    tempfile = df.query('participant_id ==' + str(participants[k]))
    tempfile = tempfile.reset_index(drop = True)
    unique = np.unique(tempfile.problem)
    time = []
    temp = pd.DataFrame()
    for j in range(len(unique)):
        tempprob = tempfile.query('problem ==' + str(unique[j]))
        tempprob = tempprob.reset_index(drop = True)
        
        #find start time of trading period
        if nk == 2: 
            starttime = datetime.datetime.strptime(tempprob.time_started[0], '%H:%M')
        else: 
            starttime = datetime.datetime.strptime(tempprob.time_started[0], '%H:%M:%S')

        #set trading time 
        myTime = []
        for l in range(len(tempprob.time_started)):
            if nk == 2:
                t = datetime.datetime.strptime(tempprob.time_started[l], \
                                               '%H:%M') - starttime
            else: 
                t = datetime.datetime.strptime(tempprob.time_started[l], \
                                               '%H:%M:%S') - starttime
            myTime.append(t)
        tempprob['starttime'] = myTime
        
        #Convert trading time to seconds
        tempprob['starttime'] = tempprob['starttime'].dt.total_seconds() 
        myTime = []
        
        #add seconds together
        for l in range(len(tempprob.time_started)):
            t = tempprob.time_into_problem[l] + tempprob.starttime[l]
            myTime.append(t)
        tempprob['time_into_problem'] = myTime
        temp = temp.append(tempprob)
    kp = kp.append(temp)

kp = kp.sort_values(by = ['participant_id', 'problem', 'problem_id', \
                          'submitted_item_move_id'])
kp = kp.reset_index(drop=True)

# =============================================================================
# Find running maximum of problem value
# =============================================================================
cummax = pd.DataFrame(kp.groupby(['problem','participant_id', \
                                  'problem_id'])['problem_value'].cummax())
kp['cummax'] = cummax.problem_value

#Save file
kp.to_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-DEC Individual/' \
          + str(nk) + 'KP-individual-v2.csv')

# =============================================================================
# Count number of moves per 15 secs bins per problem
# =============================================================================
timerange = np.arange(0, 615, 15)
bins = np.arange(15, 615, 15)
kpa = pd.DataFrame({'tradetime': timerange})
kp['bin'] = pd.cut(kp.time_into_problem, timerange, labels = bins, \
  include_lowest=True).astype(float).to_frame()
kpa = kpa.reset_index(drop = True)

for n in range(len(problems)):
    activity = []
    tempfile = kp.query('problem ==' + str(problems[n]))
    tempfile = tempfile.reset_index(drop=True)
    for j in range(len(bins)):
        temp_lst = []
        for i in range(len(tempfile.problem)):
            if tempfile.bin[i] == bins[j]:
                temp_lst.append(tempfile['cummax'][i])
        activity.append(len(temp_lst))
        if j == len(bins)-1:
            activity.append(0)
    kpa['moves' + str(n+1)] = activity
    
# =============================================================================
# Plot Graphs for Summary KP moves
# =============================================================================
#Set Parameters
fig = plt.figure(figsize=(20,10)) 

c1 = ['limegreen', 'limegreen', 'limegreen', 'darkgreen']
c2 = ['limegreen', 'red', 'darkgreen', 'darkgreen']
c3 = ['darkorange', 'darkorange', 'darkred', 'darkorange']
c4 = ['limegreen', 'limegreen', 'darkgreen', 'darkgreen']
c5 = ['darkorange', 'darkorange', 'red', 'red']
c6 = ['limegreen', 'darkgreen', 'darkgreen', 'darkgreen']
color = {0: '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}

c = ['limegreen', 'limegreen', 'darkred', 'grey', 'red', 'grey']
col = ['limegreen', 'limegreen', 'darkred', 'darkorange', 'red', 'darkorange']

l1 = ['Security 72', 'Security 144', 'Security 164', 'Security 235']
l2 = ['Security 254', 'Security 296', 'Security 454', 'Security 494']
l3 = ['Security 871', 'Security 1000', 'Security 1160', 'Security 1251']
l4 = ['Security 288', 'Security 361', 'Security 577', 'Security 602']
l5 = ['Security 127', 'Security 203', 'Security 331', 'Security 409']
l6 = ['Security 361', 'Security 468', 'Security 489', 'Security 532']
label = {"": '', 1: l1, 2: l2, 3: l3, 4: l4, 5: l5, 6: l6}

y0 = [164, 254, 1160, 549, 409, 464]

y1 = [72, 144, 164, 235]
y2 = [254, 296, 454, 494]
y3 = [871, 1000, 1160, 1251]
y4 = [288, 361, 577, 602]
y5 = [127, 203, 331, 409]
y6 = [361, 468, 489, 532]
y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y6}

ylim = [(-5, 300), (-5, 600), (-5, 1550), (-5, 750), (-5, 500), (-5, 650)]

unique = np.unique(df.problem)

#Set graph title
title = []
for i in range(0, len(unique)):
    temp = 'Problem ' + str(i+1)
    title.append(temp)
    
#Extending cumulative maximum until the end of session
last = kp['time_into_problem'].last_valid_index()
last = pd.DataFrame(kp.loc[last]).transpose()
last['problem_value'] = 0
last['time_into_problem'] = 600

#Plot
for k in range(0, len(unique)):
    temp = kp.loc[lambda kp: kp['problem'] == unique[k], :]
    ax = fig.add_subplot(2,3, k+1)
    fig.subplots_adjust(hspace = 0.3, wspace = 0.2)
    for j in range(0, len(participants)):
        tempfile = temp.loc[lambda tempfile: tempfile['participant_id'] == participants[j], :]
        tempfile = tempfile.sort_values(['time_into_problem'])
        tempfile = tempfile.append(last)
        tempfile = tempfile.reset_index(drop = True)
        if tempfile.empty == False:
            cummax = tempfile['problem_value'].cummax().to_frame()
            ax.step(tempfile.time_into_problem, cummax.problem_value, 'o', color= col[k], \
                    linestyle = ':', label = '_nolegend_', markersize=2, where = 'post')

for k in range(1, 7): 
    ax = fig.add_subplot(2,3, k)
    ax.set_xlabel('Time into Problem (secs)')
    ax.set_ylabel('Value of Problem')
    ax.title.set_text(title[k-1])
    ax.set_xlim(-5, 600)
    ax.set_ylim(ylim[k-1])
    for i in range(0, 4):
        ax.axhline(y = y[k][i], color = color[k][i], linestyle='--', \
                   linewidth=0.5, label = y[k][i])
    ax.axhline(y = y0[k-1], color = c[k-1], linestyle='-', linewidth=1, \
               label = 'Optimal Solution: ' + str(y0[k-1]))
    ax.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0.25, ncol = 3)
    
fig.suptitle('Individual Knapsack Moves -Session ' + str(nk), fontsize = 16, y=0.95)
plt.show()

# =============================================================================
# =============================================================================
# # For Individual Participant KP Data per problem
# =============================================================================
# =============================================================================
# =============================================================================
# Count number of moves per 15 secs bins per participant
# =============================================================================
m = ['Ant', 'Beaver', 'Camel', 'Dolphin', 'Elephant', 'Frog']
e = ['-EASY', '-HARD', '-HARD', '-EASY', '-HARD', '-EASY']
for mk in range(0, 6): 
    file = kp.loc[lambda kp: kp['problem'] == problems[mk], :]
    kpa = pd.DataFrame({'tradetime': timerange})
    
    for n in range(len(participants)):
        activity = []
        tempfile = file.loc[lambda file: file['participant_id'] == participants[n], :]
        tempfile = tempfile.reset_index(drop=True)
        for j in range(len(bins)):
            temp_lst = []
            for i in range(len(tempfile.problem)):
                if tempfile.bin[i] == bins[j]:
                    temp_lst.append(tempfile['cummax'][i])
            activity.append(len(temp_lst))
            if j == len(bins)-1:
                activity.append(0)
        kpa['moves' + str(n+1)] = activity
        for k in range(len(kpa['moves' + str(n+1)])):
            if kpa['moves' + str(n+1)][k] == []:
                kpa['moves' + str(n+1)][k] = np.nan
    
    # =============================================================================
    # Plot Graphs for Individual KP moves by participant
    # =============================================================================
    #Set Parameters
    ylim = [(-5, 300), (-5, 600), (-5, 1300), (-5, 750), (-5, 500), (-5, 650)]
        
    fig = plt.figure(figsize=(25,20))
    plotrange = np.arange(len(participants))
    
    #Plot
    for k in plotrange: 
        ax = fig.add_subplot(5, 4, k+1)
        par = ax.twinx()
        fig.subplots_adjust(hspace = 0.4, wspace = 0.4)
        tempfile = file.loc[lambda file: file['participant_id'] == participants[k], :]
        tempfile = tempfile.sort_values(['time_into_problem'])
        tempfile = tempfile.reset_index(drop = True)
        tempfile = tempfile.append(last)
        par.bar(kpa.tradetime, kpa['moves'+str(k+1)], width=15, alpha = 0.3, color = 'blue')
        if tempfile.empty == False:
            cummax = tempfile['problem_value'].cummax().to_frame()
            ax.step(tempfile.time_into_problem, cummax.problem_value, 'o', color= col[mk], \
                    linestyle = ':', label = '_nolegend_', markersize=2, where = 'post')
    #    par.step(kpa.tradetime, kpa['moves'+str(k+1)], where = 'post')
        ax.set_xlabel('Time into Problem (secs)')
        ax.set_ylabel('Value of Problem')
        par.set_xlabel('Time into Problem (secs)')
        par.set_ylabel('No. of Moves per 15 secs')
        ax.title.set_text('Participant ' + str(k+1))
        ax.set_xlim(-5, 600)
        ax.set_ylim(ylim[mk])
        par.set_xlim(-5, 600)
        par.set_ylim(0, 40)
        for i in range(0, 4):
            ax.axhline(y = y[mk+1][i], color = color[mk+1][i], \
                       linestyle='--', linewidth=0.5, label = y[mk+1][i])
        ax.axhline(y = y0[mk], color = c[mk], linestyle='-', linewidth=1, \
                   label = 'Optimal Solution: ' + str(y0[mk]))
        if k == 7:
            ax.legend(bbox_to_anchor=(1, 0.7), loc=2, borderaxespad=0.25)
        
    fig.suptitle('Individual Knapsack Moves -Session ' + str(nk) \
                 + ' -' + str(m[mk]) + str(e[mk]), fontsize = 16, y=0.92)
    plt.show()

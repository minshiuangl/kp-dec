#Load packages
import pandas as pd
import numpy as np

# =============================================================================
# Load relevant files 
# =============================================================================
#Choose session
nk = 6

df = {}
file = ['', str(nk) + 'KP', str(nk) + 'KPItems', 'ItemMove' + str(nk)]

for i in range(1,4):
    df[i] = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/'+ file[i] + '.csv')

df[1] = df[1].drop(columns=['interventions_available', 'interventions_used'])
df[2] = df[2].drop(columns=['start_pos_x', 'start_pos_y', 'pixel_size'])
df[3] = df[3].drop(columns=['pos_x', 'pos_y'])

# =============================================================================
# Find missing items (i.e., items with no submitted_item_move_id)
# =============================================================================
uniitemid2 = np.unique(df[2].submitted_item_id)
uniitemid3 = np.unique(df[3].submitted_item_id)
unmatcheditem = np.setdiff1d(uniitemid2, uniitemid3)

# =============================================================================
# Find problem_id of correpsonding missing items
# =============================================================================
problemid = []
itemid = []
inkp = []
for i in range(len(unmatcheditem)):
    for j in range(len(df[2].submitted_item_id)):
        if unmatcheditem[i] == df[2].submitted_item_id[j]:
            problemid.append(df[2].submitted_problem_id[j])
            inkp.append(df[2].in_knapsack[j])
            itemid.append(df[2].submitted_item_id[j])
  
# =============================================================================
# Create new file          
# =============================================================================
unique = pd.DataFrame()
unique['submitted_problem_id'] = problemid
unique['in_knapsack'] = inkp
unique['submitted_item_id'] = itemid

# =============================================================================
# Match participant_id to problem_id
# =============================================================================
participantid = []
for i in range(len(unique.submitted_problem_id)):
    for j in range(len(df[1].submitted_problem_id)):
        if unique.submitted_problem_id[i] == df[1].submitted_problem_id[j]:
            participantid.append(df[1].participant_id[j])
            

unique['participant_id'] = participantid

# =============================================================================
# Sort and save file
# =============================================================================
unique = unique.sort_values(by=['submitted_item_id'])
unique = unique.reindex(columns= ['participant_id', 'submitted_problem_id', 'submitted_item_id', 'in_knapsack'])
unique = unique.reset_index(drop=True)

uni = unique.query('in_knapsack == 1')
        

unique.to_csv('/Users/MLEE/Desktop/' + str(nk) + 'missing.csv')
uni.to_csv('/Users/MLEE/Desktop/' + str(nk) + 'missing_kp.csv')


#Load packages
import pandas as pd
import numpy as np

# =============================================================================
# Set bins
# =============================================================================
timerange = np.arange(0, 605, 5)
bins = np.arange(5, 605, 5)

for nk in range(2, 7):
    # =============================================================================
    # Load csv file for each session
    # =============================================================================
    df = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-DEC Individual/' \
                     + str(nk) + 'KP-individual-v2.csv')
    df = df.sort_values(by = ['problem', 'submitted_item_move_id'])
    
    participants = np.unique(df.participant_id)
    problems = np.unique(df.problem)
    
    # =============================================================================
    # Count number of moves per 15 sec bin per problem per participant
    # =============================================================================
    df['bin'] = pd.cut(df.time_into_problem, timerange, labels = bins, \
      include_lowest=True).astype(float).to_frame()
    act = pd.DataFrame()
    
    for k in range(0, 6): 
        kpa = pd.DataFrame({'tradetime': timerange})
        kpa['problem'] = np.nan
        kpa['problem'] = kpa['problem'].fillna(int(k+1))
        kpa = kpa.reset_index(drop = True)
        file = df.loc[lambda df: df['problem'] == problems[k], :]
        for n in range(len(participants)):
            kpa['participant_id'] = np.nan
            kpa['participant_id'] = kpa['participant_id'].fillna(int(participants[n]))
            activity = []
            cmax = []
            tempfile = file.loc[lambda file: file['participant_id'] == participants[n], :]
            tempfile = tempfile.reset_index(drop=True)
            for j in range(len(bins)):
                temp_lst = []
                for i in range(len(tempfile.problem)):
                    if tempfile.bin[i] == bins[j]:
                        temp_lst.append(tempfile['cummax'][i])
                cmax.append(np.nanmean(temp_lst))
                activity.append(len(temp_lst))
                if j == len(bins)-1:
                    activity.append(0)
                    cmax.append(np.nan)
            kpa['moves'] = activity
            kpa['cummax'] = cmax
            if kpa['moves'].empty == True:
                kpa['moves'] = np.nan
            if kpa['cummax'].empty == True:
                kpa['cummax'] = np.nan
            kpa['cummax'] = kpa['cummax'].fillna(method = 'ffill')
            kpa['cummax'] = kpa['cummax'].replace(np.nan, 0)
            act = act.append(kpa)
    act['session'] = np.nan
    act['session'] = act['session'].fillna(nk-1)
    act.to_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/' + str(nk) + 'KP-individual-moves-5.csv')
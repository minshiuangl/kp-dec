#Load packages
import pandas as pd
import numpy as np

for nk in range(2, 7):
    # =============================================================================
    # Load csv file, for each session
    # =============================================================================
    df = {}
    file = ['', 'ItemMove' + str(nk), str(nk) + 'KPItems', 'Itemvalues', str(nk) + 'KP']
    
    for i in range(1,5):
        df[i] = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-DEC Individual/'\
          + file[i] + '.csv')
        
    #Remove irrelevant columns
    df[1] = df[1].drop(columns = ['pos_x', 'pos_y'])
    df[2] = df[2].drop(columns = ['start_pos_x', 'start_pos_y', 'pixel_size'])
    df[4] = df[4].drop(columns=['interventions_available','interventions_used'])

    # =============================================================================
    # Match item id to item value
    # =============================================================================
    myitem = []
    
    for i in range(len(df[2].item_id)):
        for j in range(len(df[3].item_id)):
            if df[2].item_id[i] == df[3].item_id[j]:
                temp = df[3].item_value[j] 
        myitem.append(temp)
    
    df[2]['item_value'] = myitem
    
    # =============================================================================
    # Match item value to submitted item_id
    # =============================================================================
    myitem = []
    
    for i in range(len(df[1].submitted_item_id)):
        for j in range(len(df[2].submitted_item_id)):
            if df[1].submitted_item_id[i] == df[2].submitted_item_id[j]:
                temp = df[2].item_value[j] 
        myitem.append(temp)
    
    df[1]['item_value'] = myitem
    
    # =============================================================================
    # Match individual items to problem id
    # =============================================================================
    myID = []
    
    for i in range(len(df[1].submitted_item_id)):
        for j in range(len(df[2].submitted_problem_id)):
            if df[1].submitted_item_id[i] == df[2].submitted_item_id[j]:
                temp = df[2].submitted_problem_id[j]
        myID.append(temp)
    
    df[1]['problem_id'] = myID
    
    # =============================================================================
    # Match problem id to participant id
    # =============================================================================
    #Check start time (for multiple submissions)
    df[4].time_started = df[4].time_started.str.partition(' ')[2]
    myID = []
    myProb = []
    myTime = []
    
    for i in range(len(df[1].submitted_item_id)):
        for j in range(len(df[4].participant_id)):
            if df[1].problem_id[i] == df[4].submitted_problem_id[j]:
                temp = df[4].participant_id[j]
                tempprob = df[4].problem_id[j]
                temptime = df[4].time_started[j]
        myID.append(temp)
        myProb.append(tempprob)
        myTime.append(temptime)
    
    df[1]['participant_id'] = myID
    df[1]['problem'] = myProb
    df[1]['time_started'] = myTime
    
    #Sort Dataframe by time
    df[1] = df[1].sort_values(by = ['problem_id', 'time_into_problem'])
    df[1] = df[1].reset_index(drop = True)
    
    problemid = np.unique(df[1].problem)
    
    if len(problemid) != 6: 
        df[1] = df[1][df[1]["problem"] != problemid[0]]
        df[1] = df[1].reset_index(drop = True)
        problemid = problemid[1:]
        
    # =============================================================================
    # Calculate Movements in KP problem over time for each individual
    # =============================================================================    
    dt = {}
    kp = pd.DataFrame()
    #Replace 0 with -1 for items that have been taken out
    problems = np.unique(df[1].problem_id)
    
    for k in range(0, len(problems)):
        tempfile = df[1].query('problem_id ==' + str(problems[k]))
        tempfile = tempfile.sort_values(by = ['submitted_item_move_id'])
        tempfile = tempfile.reset_index(drop = True)
        items = np.unique(tempfile.submitted_item_id)
        dt[k] = pd.DataFrame()
        tempitem = {}
        index = []
        for l in range(0, len(items)):
            tempitem[l] = tempfile.query('submitted_item_id ==' + str(items[l]))
            tempitem[l] = tempitem[l].sort_values(by = ['submitted_item_move_id'])
            tempitem[l] = tempitem[l].reset_index(drop = True)
            index = tempitem[l].loc[tempitem[l]['in_knapsack'] == 1].index.values.tolist()
            if index != []:
                index = list(map(lambda x: x + 1, index))
                for i in range(0, len(index)):
                    tempitem[l].loc[index[i], 'in_knapsack'] = -1
            elif index == []: 
                tempitem[l] = tempitem[l]
            dt[k] = dt[k].append(tempitem[l])
        kp = kp.append(dt[k])
    
    kp = kp.dropna(subset=['problem_id'])
    kp = kp.sort_values(by = ['problem_id', 'submitted_item_move_id'])
    kp = kp.reset_index(drop = True)
    
    # =============================================================================
    # Calculate problem value over time
    # =============================================================================
    totalvalue = [kp.item_value[0] * kp.in_knapsack[0]]
    total = kp.item_value[0] * kp.in_knapsack[0]
    
    for i in range(1, len(kp)):
        if kp.problem_id[i] != kp.problem_id[i-1]:
            total = []
            total = kp.item_value[i] * kp.in_knapsack[i]
            totalvalue.append(total)
        else: 
            total += kp.item_value[i] * kp.in_knapsack[i]
            if total < 0:
               total = totalvalue[i-1]
            totalvalue.append(total)
    
    kp['problem_value'] = totalvalue
    
    kp.to_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-DEC Individual/' \
              + str(nk) + 'KP-individual.csv')
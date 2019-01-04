#Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import integrate
import matplotlib.lines as mlines

# =============================================================================
# Choose Problem Instance
# =============================================================================
m = ['', 'Ant', 'Beaver', 'Camel', 'Dolphin', 'Elephant', 'Frog']
e = ['', '-EASY', '-HARD', '-HARD', '-EASY', '-HARD', '-EASY']

for mk in range(1, 7):  
    # =============================================================================
    # =============================================================================
    # #Load files for trading data across sessions 
    # =============================================================================
    # =============================================================================
    df = {}
    file = ['', str(2) + str(m[mk]) + '-adjusted', str(3) + str(m[mk]) \
            + '-adjusted', str(4) + str(m[mk]) + '-adjusted', str(5) + str(m[mk]) \
            + '-adjusted', str(6) + str(m[mk]) + '-adjusted']
    
    for i in range(1,6):
        df[i] = pd.read_csv('/Users/MLEE/Desktop/KP-DEC-Python-Results/'+ file[i] + '.csv')
        df[i] = df[i].drop(columns=['Unnamed: 0'])
    
    # =============================================================================
    # Combine Dataframes
    # =============================================================================
    dt = pd.DataFrame()
    for i in range(1, 6):
        dt = dt.append(df[i])
    
    dt = dt.sort_values(['tradetime'])
    dt = dt.reset_index(drop=True)
    
    # =============================================================================
    # Plot Graph
    # =============================================================================
    #Set Parameters
#    plt.figure(figsize=(9,6))
#    plt.xlabel('Trading Time (seconds)')
#    plt.ylabel('Price (cents)')
#    plotrange = np.arange(0,4)
    
    c1 = ['limegreen', 'limegreen', 'limegreen', 'darkgreen']
    c2 = ['limegreen', 'red', 'darkgreen', 'darkgreen']
    c3 = ['darkorange', 'darkorange', 'darkred', 'darkorange']
    c4 = ['limegreen', 'limegreen', 'darkgreen', 'darkgreen']
    c5 = ['darkorange', 'darkorange', 'red', 'red']
    c6 = ['limegreen', 'darkgreen', 'darkgreen', 'darkgreen']
    color = {0: '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}
    
    m1 = ['o', 'x', '^', 'o']
    m2 = ['o', 'o', 'o', 'x']
    m3 = ['o', 'x', 'o', 'o']
    m4 = ['o', 'x', 'o', 'o']
    m5 = ['o', 'x', 'o', 'x']
    m6 = ['o', 'o', 'x', '^']
    marker = {0: '', 1: m1, 2: m2, 3: m3, 4: m4, 5: m5, 6: m6}
    
    l1 = ['Security 1 \n Threshold:72  Payoff:100', \
          'Security 2 \n Threshold:144  Payoff:100', \
          'Security 3 \n Threshold:164  Payoff:100', \
          'Security 4 \n Threshold:235  Payoff:0']
    l2 = ['Security 1 \n Threshold:254  Payoff:100', \
          'Security 2 \n Threshold:296  Payoff:0', \
          'Security 3 \n Threshold:454  Payoff:0', \
          'Security 4 \n Threshold:494  Payoff:0']
    l3 = ['Security 1 \n Threshold:871  Payoff:100', \
          'Security 2 \n Threshold:1000  Payoff:100', \
          'Security 3 \n Threshold:1160  Payoff:100', \
          'Security 4 \n Threshold:1251  Payoff:0']
    l4 = ['Security 1 \n Threshold:288  Payoff:100', \
          'Security 2 \n Threshold:361  Payoff:100', \
          'Security 3 \n Threshold:577  Payoff:0', \
          'Security 4 \n Threshold:602  Payoff:0']
    l5 = ['Security 1 \n Threshold:127  Payoff:100', \
          'Security 2 \n Threshold:203  Payoff:100', \
          'Security 3 \n Threshold:331  Payoff:100', \
          'Security 4 \n Threshold:409  Payoff:100']
    l6 = ['Security 1 \n Threshold:361  Payoff:100', \
          'Security 2 \n Threshold:468  Payoff:0', \
          'Security 3 \n Threshold:489  Payoff:0', \
          'Security 4 \n Threshold:532  Payoff:0']
    label = {"": '', 1: l1, 2: l2, 3: l3, 4: l4, 5: l5, 6: l6}
        
    y1 = [100.1, 100.1, 100.1, -0.1]
    y2 = [100.1, -0.5, -0.1, -0.1]
    y3 = [100.1, 100.1, 100.5, -0.1]
    y4 = [100.1, 100.1, -0.1, -0.1]
    y5 = [100.1, 100.5, 100.5, 100.5]
    y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y2}
    
    y0 = [164, 254, 1160, 549, 409, 464]
    
#    #Plot
#    for i in plotrange:
#        plt.title(str(m[mk]) + str(e[mk]) + '-All Sessions')
#        plt.plot(dt.trading_seconds, dt['security' + str(i+1)], color= color[mk][i], \
#                                        markersize=5, label = label[mk][i], \
#                                        marker=marker[mk][i], linestyle='')
#        plt.axhline(y = y[mk][i], color = color[mk][i], linestyle='-', linewidth=1.5)
#        plt.legend(bbox_to_anchor=(1, 0.7), loc=2, borderaxespad=0.25, \
#                   title="Securities and Payoffs")
#    
#    #Set legend and x axis of graph
#    plt.xlim(0, 600)
#    plt.show()
    
    # =============================================================================
    # =============================================================================
    # # Determine average price at every 15/30 secs and create confidence interval at +/- 1 STD
    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Create 30secs bins to calculate average price
    # =============================================================================
    timerange = np.arange(0, 630, 30)
    bins = np.arange(30, 630, 30)
    df = pd.DataFrame()
    df['tradetime'] = timerange
    securities = ['security1', 'security2', 'security3', 'security4']
    
    dt['bin'] = pd.cut(dt.trading_seconds, timerange, labels = bins, \
      include_lowest=True).astype(float).to_frame()
    dt = dt.reset_index(drop = True)
    
    for n in range(4):
        mktmean = []
        mktstd = []
        for j in range(len(bins)):
            temp = []
            for i in range(len(dt.bin)):
                if dt.bin[i] == bins[j]:
                    temp.append(dt[securities[n]][i])
                else: 
                    temp.append(np.nan)
                mean = np.nanmean(temp)
                z = np.count_nonzero(temp)
                if z != []:
                    std = np.nanstd(temp, ddof=1)/math.sqrt(z)
            mktmean.append(mean)
            mktstd.append(std)
            if j == len(bins)-1:
                mktmean.append(mean)
                mktstd.append(std)
        df[securities[n]] = mktmean
        df[securities[n] + '-std'] = mktstd
        
    
    #Forward fill nan values until last valid value for graph  
    for n in range(4):
        temp = df[securities[n]].last_valid_index()
        if temp != len(df[securities[n]]):
            df[securities[n]] = df[securities[n]].fillna(method='ffill')[:temp+1]
        else:
            df[securities[n]] = df[securities[n]].fillna(method='ffill')
    
    # =============================================================================
    # Plot Graphs
    # =============================================================================
    #Set Parameters
    fig = plt.figure(figsize=(15,10))
    plotrange = np.arange(0,4)
    
    y1 = [100, 100, 100, 0]
    y2 = [100, 0, 0, 0]
    y3 = [100, 100, 100, 0]
    y4 = [100, 100, 0, 0]
    y5 = [100, 100, 100, 100]
    y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y2}
    
    fc1 = ['honeydew', 'honeydew', 'honeydew', 'palegreen']
    fc2 = ['honeydew', 'mistyrose', 'palegreen', 'palegreen']
    fc3 = ['cornsilk', 'cornsilk', 'lightcoral', 'cornsilk']
    fc4 = ['honeydew', 'honeydew', 'palegreen', 'palegreen']
    fc5 = ['cornsilk', 'cornsilk', 'mistyrose', 'mistyrose']
    fc6 = ['honeydew', 'palegreen', 'palegreen', 'palegreen']
    fcolor = {0: '', 1: fc1, 2: fc2, 3: fc3, 4: fc4, 5: fc5, 6: fc6}
    
    #Plot
    for i in plotrange: 
        yerr = df['security' + str(i+1) + '-std'].fillna(0)
        fig.subplots_adjust(hspace = 0.3)
        ax = fig.add_subplot(2,2, i+1)
        ax.plot(dt.trading_seconds, dt['security' + str(i+1)], 'o', \
                                       color= color[mk][i], markersize=5, \
                                       label = label[mk][i], linestyle='')
        ax.plot(df.tradetime, df['security' + str(i+1)], color= color[mk][i], \
                                 linestyle='-', label = label[mk][i])
        ax.errorbar(df.tradetime, df['security' + str(i+1)], yerr = yerr, \
                                     color= color[mk][i], linestyle='-', linewidth=1)
        ax.set_xlabel('Trading Time (seconds)')
        ax.set_ylabel('Price (cents)')
        ax.title.set_text(label[mk][i])
        ax.axhline(y = y[mk][i], color = color[mk][i], linestyle='-', linewidth=1.5)
        ax.set_xlim(0, 600)
        ax.set_ylim(-5, 105)
        ax.fill_between(df.tradetime, df['security' + str(i+1)] - yerr, \
                                         df['security' + str(i+1)] + yerr, \
                                         facecolor=fcolor[mk][i])
        if i == 1: 
            patcha = mlines.Line2D([], [], color = 'black', linestyle='None', marker='o', label='Trade')
            patchb = mlines.Line2D([], [], color = 'black', linestyle='-', \
                           label='30 sec Avg. \n Trendline')
            ax.legend(handles=[patcha, patchb], ncol=2, \
               bbox_to_anchor=(1.015, 1.3), loc=1) 
    
    fig.suptitle('KP Trial ' + str(mk) + '\n Optimal Solution:' + \
                 str(y0[mk-1]), fontsize = 16, y=0.97)
    
    plt.show()
    
    # =============================================================================
    # Calculate price convergence of each problem using integration
        #If payoff = 100: calculate area above the curve
        #If payoff = 0: calculate area under the curve
    # =============================================================================
    integrals = []
    normintegrals = []
    y1 = [100, 100, 100, 0]
    y2 = [100, 0, 0, 0]
    y3 = [100, 100, 100, 0]
    y4 = [100, 100, 0, 0]
    y5 = [100, 100, 100, 100]
    y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y2}
    df.tradetime = df.tradetime / 60
    
    for i in range(1, 5):
        maxindex = df['security' + str(i)].last_valid_index()
        minindex = df['security' + str(i)].first_valid_index() 
        tempfile = df.loc[:maxindex, :]
        if minindex != 0: 
            tempfile = tempfile.replace(tempfile['security' + str(i)][0], 50)
            tempfile[:minindex] = tempfile.fillna(method = 'ffill')
            tempfile = tempfile.dropna(subset=['security' + str(i)])
        else: 
            tempfile = tempfile.dropna(subset=['security' + str(i)])
        if y[mk][i-1] == 100: 
            integral = integrate.simps(tempfile['security' + str(i)], tempfile.tradetime)
            brange = np.ones(len(tempfile['security' + str(i)]))*100
            bound = integrate.simps(brange, tempfile.tradetime)
            integral = bound - integral
        else: 
            integral = integrate.simps(tempfile['security' + str(i)], tempfile.tradetime)
        
        normintegral = integral / tempfile['tradetime'][maxindex]
        
        integrals.append(integral)
        normintegrals.append(normintegral)
    
    #Save price convergence as new file    
    if mk == 1:
        marketpc = {}
    marketpc[mk] = pd.DataFrame(integrals, columns = ['price_convergence'])
    marketpc[mk]['normalised_tradetime'] = normintegrals
    marketpc[mk]['problem'] = int(mk)
    s = np.arange(1, 5)
    marketpc[mk]['security'] = s
    
    if mk == 6: 
        mktpc = pd.DataFrame()
        for k in range(1, 7):
            mktpc = mktpc.append(marketpc[k])
        mktpc.to_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/priceconvergence-norm-30.csv')
    
    df.tradetime = df.tradetime * 60
    
    # =============================================================================
    # =============================================================================
    # # Bid-Ask-Spread
    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Load files across session to combine dataframe for bid-ask spread
    # =============================================================================
    f = {}
    for k in range(1, 5):
        f[k] = ['', str(2) + str(m[mk]) + 'bidask' + str(k), str(3) + str(m[mk]) \
         + 'bidask' + str(k), str(4) + str(m[mk]) + 'bidask' + str(k), str(5) \
         + str(m[mk]) + 'bidask' + str(k), str(6) + str(m[mk]) + 'bidask' + str(k)]
    
    security = {}
    for k in range(1, 5):
        security[k] = pd.DataFrame()
        temp = []
        for i in range(1,6):
            temp = pd.read_csv('/Users/MLEE/Desktop/KP-DEC-Python-Results/'+ f[k][i] + '.csv')
            temp = temp.drop(columns=['Unnamed: 0'])
            security[k] = security[k].append(temp)
        security[k] = security[k].sort_values(['tradetime'])
        security[k] = security[k].reset_index(drop=True)
    
    # =============================================================================
    # Create 30secs bins to calculate average bid
    # =============================================================================
    bidask = {}
    
    for k in range(1, 5):
        security[k]['bin'] = pd.cut(security[k].trading_seconds, timerange, \
                labels = bins, include_lowest=True).astype(float).to_frame()
        security[k] = security[k].reset_index(drop = True)
        bidask[k] = pd.DataFrame()
        bidask[k]['tradetime'] = timerange
        mktmean1 = []
        mktstd1 = []
        mktmean2 = []
        mktstd2 = []
        for j in range(len(bins)):
            temp1 = []
            temp2 = []
            for i in range(len(security[k].bin)):
                if security[k].bin[i] == bins[j]:
                    temp1.append(security[k].bid[i])
                    temp2.append(security[k].ask[i])
                else: 
                    temp1.append(np.nan)
                    temp2.append(np.nan)
                mean1 = np.nanmean(temp1)
                z1 = np.count_nonzero(temp1)
                mean2 = np.nanmean(temp2)
                z2 = np.count_nonzero(temp2)
                if z1 != []:
                    std1 = np.nanstd(temp1, ddof=1)/math.sqrt(z1)
                if z2 != []:
                    std2 = np.nanstd(temp2, ddof=1)/math.sqrt(z2)
            mktmean1.append(mean1)
            mktstd1.append(std1)
            mktmean2.append(mean2)
            mktstd2.append(std2)
            if j == len(bins)-1:
                mktmean1.append(mean1)
                mktstd1.append(std1)
                mktmean2.append(mean2)
                mktstd2.append(std2)
        bidask[k]['bid'] = mktmean1
        bidask[k]['bid-std'] = mktstd1
        bidask[k]['ask'] = mktmean2
        bidask[k]['ask-std'] = mktstd2
        
    # =============================================================================
    # Plot Graph
    # =============================================================================
    #Plot
    plotrange = np.arange(0,4)
    fig = plt.figure(figsize=(15,10))
    
    for i in plotrange: 
        fig.subplots_adjust(hspace = 0.3)
        ax = fig.add_subplot(2,2, i+1)
        ax.axhline(y = y[mk][i], color = color[mk][i], linestyle='-', linewidth=1)
        ax.plot(bidask[i+1].tradetime, bidask[i+1].bid, '|', markersize=9, \
                linestyle = '-.', color= 'blue', label = '_nolegend_', \
                drawstyle='steps-post', linewidth=1)
        ax.plot(bidask[i+1].tradetime, bidask[i+1].ask, '|', markersize=9, \
                linestyle = ':', color= 'red', label = '_nolegend_', \
                drawstyle='steps-post', linewidth=1)
        ax.set_xlabel('Trading Time')
        ax.set_ylabel('Price (cents)')
        ax.set_xlim(0, 600)
        ax.set_ylim(-5, 105)
        ax.title.set_text(label[mk][i])
     
    fig.suptitle('Bid-Ask Spread \n' + str(m[mk]) + str(e[mk]), fontsize = 16, y=0.95)
    plt.show()

#Load packages
import pandas as pd
import numpy as np
import math
from scipy import integrate

# =============================================================================
# =============================================================================
# # Compute Trading Results of each Session
# =============================================================================
# =============================================================================
#Choose Instance
m = ['', 'Ant', 'Beaver', 'Camel', 'Dolphin', 'Elephant', 'Frog']
e = ['', '-EASY', '-HARD', '-HARD', '-EASY', '-HARD', '-EASY']

for mk in range(1, 7):
    for nk in range(2, 7):
        #Load csv file
        df = pd.read_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/' + str(nk) + str(m[mk]) + '-adjusted.csv')
        df = df.drop(columns=['Unnamed: 0'])
        
        # =============================================================================
        # Integration
        # =============================================================================
        timerange = np.arange(0, 615, 15)
        bins = np.arange(15, 615, 15)
        pcm = pd.DataFrame()
        pcm['tradetime'] = timerange
        securities = ['security1', 'security2', 'security3', 'security4']
        
        df['bin'] = pd.cut(df.trading_seconds, timerange, labels = bins, include_lowest=True).astype(float).to_frame()
        df = df.reset_index(drop = True)
        
        for n in range(4):
            mktmean = []
            mktstd = []
            for j in range(len(bins)):
                temp = []
                for i in range(len(df.bin)):
                    if df.bin[i] == bins[j]:
                        temp.append(df[securities[n]][i])
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
            pcm[securities[n]] = mktmean
            pcm[securities[n] + '-std'] = mktstd
        
        # =============================================================================
        # Calculate price convergence of each market using integration 
        # =============================================================================
        integrals = []
        normintegrals = []
        y1 = [100, 100, 100, 0]
        y2 = [100, 0, 0, 0]
        y3 = [100, 100, 100, 0]
        y4 = [100, 100, 0, 0]
        y5 = [100, 100, 100, 100]
        y = {"": '', 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y2}
        pcm.tradetime = pcm.tradetime / 60
        
        for i in range(1, 5):
            maxindex = pcm['security' + str(i)].last_valid_index()
            minindex = pcm['security' + str(i)].first_valid_index()
            maxtime = df['security' + str(i)].last_valid_index()
            tempfile = pcm.loc[:maxindex, :]
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
            
            if maxtime == None:
                normintegral = 0
            else:
                normintegral = integral / df['trading_seconds'][maxtime]
            
            integrals.append(integral)
            normintegrals.append(normintegral)
            
        if nk == 2:
            marketpc = {}
        marketpc[nk] = pd.DataFrame(integrals, columns = ['Problem' + str(mk)])
        marketpc[nk]['normalised_tradetime'] = normintegrals
        
        if nk == 6: 
            mktpc = pd.DataFrame()
            for k in range(2, 7):
                mktpc = mktpc.append(marketpc[k])
            mktpc.to_csv('/Users/MLEE/desktop/KP-DEC-Python-Results/convergence-market-' + str(mk) + '-15.csv')
        
        pcm.tradetime = pcm.tradetime * 60
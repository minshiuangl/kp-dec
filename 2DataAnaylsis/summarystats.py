#Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dt = pd.read_csv('/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python/KP-security-reg-15.csv')

moves = []
avgmoves =[]
sdmoves = []
bid = []
avgbid = []
sdbid = []
ask = []
avgask = []
sdask = []
trade = []
avgtrade = []
sdtrade=[]
problem = pd.DataFrame()
problem['KP Trial'] = np.arange(1,7)
for i in range(6):
    mask = dt.problem== int(i+1)
    temp = dt[mask]
    moves.append(np.sum(temp.moves))
    avgmoves.append(np.sum(temp.moves)/87)
    sdmoves.append(np.std(temp.moves, ddof=1))
    bid.append(np.sum(temp.bidcount))
    avgbid.append(np.sum(temp.bidcount)/87)
    sdbid.append(np.std(temp.bidcount, ddof=1))
    ask.append(np.sum(temp.askcount))
    avgask.append(np.sum(temp.askcount)/87)
    sdask.append(np.std(temp.askcount, ddof=1))
    trade.append(np.sum(temp.tradecount)/41)
    avgtrade.append(np.sum(temp.tradecount)/87/41)
    sdtrade.append(np.std(temp.tradecount, ddof=1))

problem['No. of moves in the Knapsack task Total'] = moves
problem['Avg. moves'] = avgmoves
problem['sd. moves'] = sdmoves
problem['No. of market bid orders Total'] = bid
problem['Avg. bid'] = avgbid
problem['sd. bid'] = sdbid
problem['No. of market ask orders Total'] = ask
problem['Avg. ask'] = avgask
problem['sd. ask'] = sdask
problem['No. of market traded orders Total'] = trade
problem['Avg. traded'] = avgtrade
problem['sd. traded'] = sdtrade

problem.to_csv('/Users/MLEE/Desktop/kptrial.csv')

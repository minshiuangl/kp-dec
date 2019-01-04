#Load packages
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import math

#Load files
dt = pd.read_csv('/Users/MLEE/Desktop/logcp.csv')
mask = dt.security != 5
dt = dt[mask]

# =============================================================================
# Plot Graph
# =============================================================================
c1 = ['limegreen', 'limegreen', 'limegreen', 'darkgreen']
c2 = ['limegreen', 'red', 'darkgreen', 'darkgreen']
c3 = ['darkorange', 'darkorange', 'darkred', 'darkorange']
c4 = ['limegreen', 'limegreen', 'darkgreen', 'darkgreen']
c5 = ['darkorange', 'darkorange', 'red', 'red']
c6 = ['limegreen', 'darkgreen', 'darkgreen', 'darkgreen']
color = {0: '', 1: c1, 2: c2, 3: c3, 4: c4, 5: c5, 6: c6}
marker = ['o', 'x', '^', 's', 'P', 'D']

#Plot Propagation vs. Log(c\p)
fig = plt.figure(figsize=(8,5))
for i in range(6):
    mask = dt.problem == int(i+1)
    temp = dt[mask]
    temp = temp.reset_index(drop=True)
    plt.axvline(x=0, color='lightgrey', linestyle='--', alpha=0.2)
    for j in range(len(temp.security)):
        plt.scatter(temp.log[j], math.log(temp.prop[j]), \
                    color=color[i+1][j], marker=marker[i], linestyle='-', \
                     zorder=1)
    plt.xlabel('log(c\p)')
    plt.ylabel('log(propagation)')
    plt.xlim(-0.8, 0.4)
    plt.title('Log(c\p) vs. Propagation of each KP-DEC Instance')

patch1 = mpatches.Patch(color='darkgreen', label='Complexity 1')
patch2 = mpatches.Patch(color='limegreen', label='Complexity 2')
patch3 = mpatches.Patch(color='darkorange', label='Complexity 3')
patch4 = mpatches.Patch(color='red', label='Complexity 4')
patch5 = mpatches.Patch(color='darkred', label='Complexity 4: Hardest')

patcha = mlines.Line2D([], [], color = 'black', linestyle='None', marker='o', label='Problem 1')
patchb = mlines.Line2D([], [], color = 'black', linestyle='None', marker='x', label='Problem 2')
patchc = mlines.Line2D([], [], color = 'black', linestyle='None', marker='^', label='Problem 3')
patchd = mlines.Line2D([], [], color = 'black', linestyle='None', marker='s', label='Problem 4')
patche = mlines.Line2D([], [], color = 'black', linestyle='None', marker='P', label='Problem 5')
patchf = mlines.Line2D([], [], color = 'black', linestyle='None', marker='D', label='Problem 6')

plt.legend(handles=[patcha, patchb, patchc, patchd, patche, patchf, \
                    patch1, patch2, patch3, patch4, patch5], \
        bbox_to_anchor=(1, 1), loc=2) 
      
plt.show()

#Plot Normalised Price Convergence vs. Log(c\p)
fig = plt.figure(figsize=(8,5))
for i in range(6):
    mask = dt.problem == int(i+1)
    temp = dt[mask]
    temp = temp.reset_index(drop=True)
    plt.axvline(x=0, color='lightgrey', linestyle='--', alpha=0.2)
    for j in range(len(temp.security)):
        plt.scatter(temp.log[j], temp.priceconvergence[j], \
                    color=color[i+1][j], marker=marker[i], linestyle='-', \
                     zorder=1)
    plt.xlabel('log(c\p)')
    plt.ylabel('Normalised Price Convergence by trade time')
    plt.xlim(-0.8, 0.4)
    plt.ylim(0, 40)
    plt.title('Log(c\p) vs. Normalised Price Convergence of each KP-DEC Instance')

patch1 = mpatches.Patch(color='darkgreen', label='Complexity 1')
patch2 = mpatches.Patch(color='limegreen', label='Complexity 2')
patch3 = mpatches.Patch(color='darkorange', label='Complexity 3')
patch4 = mpatches.Patch(color='red', label='Complexity 4')
patch5 = mpatches.Patch(color='darkred', label='Complexity 4: Hardest')

patcha = mlines.Line2D([], [], color = 'black', linestyle='None', marker='o', label='Problem 1')
patchb = mlines.Line2D([], [], color = 'black', linestyle='None', marker='x', label='Problem 2')
patchc = mlines.Line2D([], [], color = 'black', linestyle='None', marker='^', label='Problem 3')
patchd = mlines.Line2D([], [], color = 'black', linestyle='None', marker='s', label='Problem 4')
patche = mlines.Line2D([], [], color = 'black', linestyle='None', marker='P', label='Problem 5')
patchf = mlines.Line2D([], [], color = 'black', linestyle='None', marker='D', label='Problem 6')

plt.legend(handles=[patcha, patchb, patchc, patchd, patche, patchf, \
                    patch1, patch2, patch3, patch4, patch5], \
        bbox_to_anchor=(1, 1), loc=2) 
      
plt.show()

#Plot Normalised Capacity and Normalised Profit
fig = plt.figure(figsize=(8,8))
for i in range(6):
    mask = dt.problem == int(i+1)
    temp = dt[mask]
    temp = temp.reset_index(drop=True)
    for j in range(len(temp.security)):
        plt.scatter(temp.c[j], temp.p[j], \
                    color=color[i+1][j], marker=marker[i], linestyle='-', \
                     zorder=1)
    plt.xlabel('Normalised capacity (c)')
    plt.ylabel('Normalised profit (p)')
    plt.xlim(0, 1.1)
    plt.xlim(0, 1)
    plt.title('Normalised Capacity and Normalised Profit of each KP-DEC Instance')

patch1 = mpatches.Patch(color='darkgreen', label='Complexity 1')
patch2 = mpatches.Patch(color='limegreen', label='Complexity 2')
patch3 = mpatches.Patch(color='darkorange', label='Complexity 3')
patch4 = mpatches.Patch(color='red', label='Complexity 4')
patch5 = mpatches.Patch(color='darkred', label='Complexity 4: Hardest')

patcha = mlines.Line2D([], [], color = 'black', linestyle='None', marker='o', label='Problem 1')
patchb = mlines.Line2D([], [], color = 'black', linestyle='None', marker='x', label='Problem 2')
patchc = mlines.Line2D([], [], color = 'black', linestyle='None', marker='^', label='Problem 3')
patchd = mlines.Line2D([], [], color = 'black', linestyle='None', marker='s', label='Problem 4')
patche = mlines.Line2D([], [], color = 'black', linestyle='None', marker='P', label='Problem 5')
patchf = mlines.Line2D([], [], color = 'black', linestyle='None', marker='D', label='Problem 6')

plt.legend(handles=[patcha, patchb, patchc, patchd, patche, patchf, \
                    patch1, patch2, patch3, patch4, patch5], \
        bbox_to_anchor=(1, 1), loc=2) 
       
plt.show()


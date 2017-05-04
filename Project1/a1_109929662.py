import numpy as np
import scipy.stats as ss
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.stats import gaussian_kde
import sys

# For adjusting the bin width of 4 figures 
numBin = 800
numBin2 = 20
numBin3 = 15
numBin4 = 8
nr300 = 0
nr3100 = 0
nr5000 = 0
r300 = 0
r3100 = 0
r5000 = 0

myFile = pd.read_csv(sys.argv[1],low_memory = False)
# To filter out state total rows
filter = myFile.COUNTYCODE != 0  # filter out state total rows
myFile = myFile[filter]
col = myFile.columns
# Headers with 'Value'
myHeaders = []    
for i in range(len(col)):
	if 'Value' in col[i]:
		myHeaders.append(col[i])
print('(1) COLUMN HEADERS: \n' + '\n'.join(myHeaders))

# Counties and ranked counties
numCounty = 0
rCounty = 0
ind = myFile.index
for i in range(len(ind)):
	numCounty += 1
	if myFile.loc[ind[i],'County that was not ranked'] != 1:
		rCounty += 1
print('\n(2) TOTAL COUNTIES IN FILE:' + str(numCounty))

print('\n(3) TOTAL RANKED COUNTIES:' + str(rCounty))

pop = myFile['2011 population estimate Value']
lpp = []
pp = []
for i in range(len(pop)):
	if filter[i]:
		# Convert strings like '1,264' to int
		number = int(pop[i].replace(',',''))
		pp.append(number)
		lpp.append(math.log(number))
# Population data and log population data
popu = pd.Series(pp)
log_pop = pd.Series(lpp)

popHist = popu.hist(bins = numBin)
popHist.plot()
plt.title('Hist of Population')
plt.xlabel('population')
plt.ylabel('number of counties')
plt.savefig('a1_4_histpop.png')
plt.clf()
print('\n(4) HISTOGRAM OF POPULATION: wrote a1_4_histpop.png')

logHist = log_pop.hist(bins = numBin2)
logHist.plot()
plt.title('Hist of Log Population')
plt.xlabel('Log(population)')
plt.ylabel('number of counties')
plt.savefig('a1_5_histlog.png')
plt.clf()
print('\n(5) HISTOGRAM OF LOG POPULATION: wrote a1_5_histlog.png')

rList = []
nrList = []
# Indices of ranked counties and not ranked counties
rankInd = myFile['County that was not ranked'] != 1
nrankInd = myFile['County that was not ranked'] == 1
rlpp = myFile['2011 population estimate Value'][rankInd]
nrlpp = myFile['2011 population estimate Value'][nrankInd]
# Count on ranked and not ranked population, respectively
for i in range(len(rlpp)):
	if filter[i] and rankInd[i]:
		thisNum = math.log(int(rlpp[i].replace(',','')))
		rList.append(thisNum)
		if thisNum < 1000:
			r300 += 1
		if thisNum > 3000 and thisNum < 4000:
			r3100 += 1
		if thisNum > 4000 and thisNum < 5000:
			r5000 += 1
		
for i in range(len(nrlpp)):
	if filter[i] and nrankInd[i]:
		thisNum = math.log(int(nrlpp[i].replace(',','')))
		nrList.append(thisNum)
		if thisNum < 1000:
			nr300 += 1
		if thisNum > 3000 and thisNum < 4000:
			nr3100 += 1
		if thisNum > 4000 and thisNum < 5000:
			nr5000 += 1

# Use gaussian kernel for KDE
rDensity = gaussian_kde(rList)
nrDensity = gaussian_kde(nrList)
x1 = np.linspace(1,15,5000)
x2 = np.linspace(1,15,1000)
rDensity.covariance_factor = lambda : .7
nrDensity.covariance_factor = lambda : .7
rDensity._compute_covariance()
nrDensity._compute_covariance()
plt.plot(x1,rDensity(x1),label = 'ranked')
plt.plot(x2,nrDensity(x2),label = 'not ranked')
plt.title = ('KDE of Ranked and Not Ranked Counties')
plt.xlabel = ('log(population)')
plt.ylabel = ('probability density')
plt.legend(loc='upper right')
plt.savefig('a1_6_KDE.png')
plt.clf()
print('\n(6) KERNEL DENSITY ESTIMATES: wrote a1_6_KDE.png')
p1 = (r300/(0.0001 + nr300))*(len(rList)/len(nrList))
p2 = (r3100/(0.0001 + nr3100))*(len(rList)/len(nrList))
p3 = (r5000/(0.0001 + nr5000))*(len(rList)/len(nrList))
p1 = p1/(p1 + 1)
p2 = p2/(p2 + 1)
p3 = p3/(p3 + 1)
print('\n(7) PROBABILITY RANKED GIVEN POP: the samples at population less than 5000 are too few, and KDE from previous step shows 0 at these population point. I do not think there is a precise way to measure it.')

# Column index containing 'Value'
indCol = []
for i in range(len(col)):
	if filter[i]:
		if 'Value' in col[i]:
			indCol.append(i)

print('\n(8) LIST MEAN AND STD_DEV PER COLUMN:')
for i in indCol:
	temp = []
	for j in range(len(ind)):
		if filter[j]:
			if type(myFile.iloc[j,i]) == str:
				number = float(myFile.iloc[j,i].replace(',',''))
			else:
				number = myFile.iloc[j,i]
			if number > 0:
				temp.append(number)
	print(col[i] + ': mean = ' + str(np.mean(temp)) + '    std = ' + str(np.std(temp)) )














import numpy as np
from lifelines import KaplanMeierFitter

def writeArrayToFile(varname,arrayToWrite):
	filepath = 'log'+varname+'.txt'
	with open(filepath,'w'):
		pass
		f = open(filepath, 'a+')
		for data in arrayToWrite:
			f.write(str(data)+'\n')
		f.close()

# Create lifetimes, but censor all lifetimes after time 12
censor_after = 12
actual_lifetimes = np.random.exponential(10, size=20)

observed_lifetimes = np.minimum(actual_lifetimes, censor_after*np.ones(20) )
C = (actual_lifetimes < censor_after) #boolean array
tst = np.array([1,0,1,0,0,0])
tst = tst.astype(bool)
print(tst)

## Write variables to files for debugging
# varn = 'actual_lifetimes'
# writeArrayToFile(varn,actual_lifetimes)
# varn = 'observed_lifetimes'
# writeArrayToFile(varn,observed_lifetimes)
# varn = 'event_observed'
# writeArrayToFile(varn,C)


kmf = KaplanMeierFitter(1)
print(observed_lifetimes)
print(C)
kmf.fit(observed_lifetimes, event_observed=C)
print (kmf)
# fitter methods have an internal plotting method.
# plot the curve with the confidence intervals
#kmf.plot()

import pylab
pylab.show()
# pylab.savefig('foo.svg', format="svg", bbox_inches='tight')
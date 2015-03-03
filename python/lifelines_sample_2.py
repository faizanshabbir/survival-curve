import numpy as np

# Create lifetimes, but censor all lifetimes after time 12
censor_after = 12
actual_lifetimes = np.random.exponential(10, size=20)
print (actual_lifetimes)
print ()
observed_lifetimes = np.minimum( actual_lifetimes, censor_after*np.ones(20) )
print (observed_lifetimes)
C = (actual_lifetimes < censor_after) #boolean array

from lifelines import KaplanMeierFitter

kmf = KaplanMeierFitter(1)
kmf.fit(observed_lifetimes, event_observed=C)
print (kmf)
# fitter methods have an internal plotting method.
# plot the curve with the confidence intervals
kmf.plot()

import pylab
pylab.show()
# pylab.savefig('foo.svg', format="svg", bbox_inches='tight')
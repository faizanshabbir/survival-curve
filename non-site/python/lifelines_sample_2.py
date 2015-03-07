import numpy as np

# Create lifetimes, but censor all lifetimes after time 12
censor_after = 12
actual_lifetimes = np.random.exponential(10, size=20)
# print ("actual_lifetimes", actual_lifetimes)
# print()
observed_lifetimes = np.minimum( actual_lifetimes, censor_after*np.ones(20) )
# print ("observed_lifetimes", observed_lifetimes)
C = (actual_lifetimes < censor_after) #boolean array

from lifelines import KaplanMeierFitter

kmf = KaplanMeierFitter(1)
kmf.fit(observed_lifetimes, event_observed=C)
# fitter methods have an internal plotting method.
# plot the curve with the confidence intervals
# kmf.plot()

# # Get data from kmf
# l = dir(kmf)
# d = kmf.__dict__

from pprint import pprint
# print("--dir--")
# pprint(l)
# print("--dict--")
# pprint(d, indent=2)
# print("--custom--")
# timeline = getattr(kmf, "timeline")
# print ("timeline")
# pprint(timeline)
# print("timeline_2", timeline[2])
# confidence_interval = getattr(kmf, "confidence_interval_")
# print ("confidence_interval", confidence_interval)
# event_observed = getattr(kmf, "event_observed")
# print ("event_observed", event_observed)
# event_table = getattr(kmf, "event_table")
# print ("event_table", event_table)
survival_function_ = getattr(kmf, "survival_function_")
estimate = getattr(survival_function_, "KM-estimate")
print ("estimate", estimate)
print ("--")
for x in estimate:
	print (x)
# import pylab
# pylab.show()
# pylab.savefig('foo.svg', format="svg", bbox_inches='tight')
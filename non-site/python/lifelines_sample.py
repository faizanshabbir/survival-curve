import numpy as np
import re

# Create lifetimes, but censor all lifetimes after time 12
censor_after = 12
actual_lifetimes = np.random.exponential(10, size=20)
observed_lifetimes = np.minimum( actual_lifetimes, censor_after*np.ones(20) )
C = (actual_lifetimes < censor_after) #boolean array

from lifelines import KaplanMeierFitter

kmf = KaplanMeierFitter()
kmf.fit(observed_lifetimes, event_observed=C)
# for attr, value in kmf.__dict__.iteritems():
#         print attr + "---", value
# print "-----------"
sf = getattr(kmf, "survival_function_")
# print "sf:", sf, "\n"
json_string = sf.to_json();
regex = re.compile(r'(\{\s*"KM_estimate":\s*)\{(.*)\}(\})')
print re.sub(r'(\{\s*"KM_estimate":\s*)\{(.*)\}(\})', "\1[\2]\3", json_string)
# for attr, value in sf.__dict__.iteritems():
        # print attr + "---", value
# kmf_e = getattr(kmf, "_KaplanMeierFitter__estimate")
# print
# print "kmf_e:", kmf_e
# for attr, value in kmf_e.__dict__.iteritems():
	# print attr + "---", value
# timeline = getattr(sf, "timeline")
# print timeline
# print (kmf)
# fitter methods have an internal plotting method.
# plot the curve with the confidence intervals
# kmf.plot()

# import pylab
# pylab.show()
# pylab.savefig('foo.svg', format="svg", bbox_inches='tight')
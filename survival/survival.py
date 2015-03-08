import numpy as np
from lifelines import KaplanMeierFitter

def random_data:
	# Create lifetimes, but censor all lifetimes after time 12
	censor_after = 12
	actual_lifetimes = np.random.exponential(10, size=20)
	observed_lifetimes = np.minimum( actual_lifetimes, censor_after*np.ones(20) )
	C = (actual_lifetimes < censor_after) #boolean array

	from lifelines import KaplanMeierFitter

	kmf = KaplanMeierFitter()
	kmf.fit(observed_lifetimes, event_observed=C)
	return True
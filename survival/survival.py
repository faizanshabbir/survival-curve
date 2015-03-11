import numpy as np
from lifelines import KaplanMeierFitter
import re

def random_data():
	# Create lifetimes, but censor all lifetimes after time 12
	censor_after = 12
	actual_lifetimes = np.random.exponential(10, size=20)
	observed_lifetimes = np.minimum( actual_lifetimes, censor_after*np.ones(20) )
	C = (actual_lifetimes < censor_after) #boolean array

	from lifelines import KaplanMeierFitter

	kmf = KaplanMeierFitter()
	kmf.fit(observed_lifetimes, event_observed=C)
	sf = getattr(kmf, "survival_function_")
	return survival_data_to_json(sf)

def survival_data_to_json(data):
	json_string = data.to_json(orient="split");
	# regex = re.compile(r'(\{\s*"KM_estimate":\s*)\{(.*)\}(\})')
	# return re.sub(regex, r"\1[\2]\3", json_string)
	return json_string

def generate_curve(data):
	time1 = data['time1']
	data1 = data['data1']
	time2 = data['time2']
	data2 = data['data2']

	return random_data()

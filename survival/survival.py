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
	dataSets = data['dataSets']
	time_1 = dataSets[0]['time']
	data_1 = dataSets[0]['data']

	#convert from string to numeric arrays for sorting
	time_1 = np.array(map(float,time_1))
	data_1 = np.array(map(int,data_1))
	#data_1 = [data_1 for (time_1,data_1) in sorted (zip(time_1,data_1))]
	time_1 = np.sort(time_1)
	perm = time_1.argsort()
	data_1 = data_1[perm]

	#convert death array into boolean array required for pipelines
	data_1 = data_1.astype(bool)

	kmf = KaplanMeierFitter()
	kmf.fit(time_1,event_observed=data_1)  
	
	#sf = gettatr(kmf, "survival_function_") #GETTING ERROR BUT IDK WHY
	sf = kmf.survival_function_
	return survival_data_to_json(sf)

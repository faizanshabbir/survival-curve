import numpy as np
from lifelines import KaplanMeierFitter
import re
import json

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
	return json_string

def dataset_to_lifelines(dataset):
	print dataset['type']
	if dataset['type'] == 1:
		time = dataset['time']
		data = dataset['data']

		#convert from string to numeric arrays for sorting
		time = np.array(map(float,time))
		data = np.array(map(int,data))

		time = np.sort(time)
		perm = time.argsort()
		data = data[perm]

		#convert death array into boolean array required for pipelines
		data = data.astype(bool)
	else:
		time = dataset['data']
		time = np.array(map(float,time))
		time = np.sort(time)
		currDataLen = len(np.atleast_1d(time))

		experimentLength = int(dataset['experimentLength'])
		numSamples = int(dataset['samplesInGroup'])
		diff = numSamples - currDataLen

		arrToAppend = np.ones(diff)
		arrToAppend = arrToAppend*int(experimentLength)
		time = np.concatenate((time,arrToAppend), axis = 1)

		data = np.ones(currDataLen)
		livingAppend = np.ones(diff)
		data = np.concatenate((data,livingAppend), axis = 1)
	return data, time

def generate_curve(data):
	dataSets = data['dataSets']
	results = list()

	for dataset in dataSets:
		print "Dataset", dataset
		data, time = dataset_to_lifelines(dataset)
		kmf = KaplanMeierFitter()
		kmf.fit(time,event_observed=data)  
		sf = kmf.survival_function_
		jsonData = survival_data_to_json(sf)
		print jsonData
		results.append(jsonData)

	return json.dumps(results)

function saveSvgAsFile() {
	var canvasElement = document.createElement('canvas');
	canvasElement.setAttribute('id', 'canvas');
	document.body.appendChild(canvasElement);
	canvg('canvas', $("#chart svg")[0].innerHTML);
	var img = canvasElement.toDataURL("image/png");
	document.write('<img src="' + img + '"/>');
}

function serverJsonToPlottable(results) {
	// console.debug("serverJsonToPlottable", results);
	
	var plottableData = {};
	plottableData.xs = {};
	plottableData.columns = [];
	plottableData.types = {};
	
	//XXX: Result should always be an array, this is temp
	//If result is an object instead of array, no need to loop
	if (typeof results == "object") {
		singleResultToPlottable(plottableData, results, 0);
	} else {
		var datasets = results.map(function(result) {
			return JSON.parse(result);
		});
		datasets.forEach(function(dataset, index) {
			singleResultToPlottable(plottableData, dataset, index);
		});
	}

	plotSurvival(plottableData);
}

function singleResultToPlottable(plottableData, dataset, index) {
	//Get Data
	var x = dataset.index;
	var y = flattenSingleValueArrays(dataset.data);
	//Create Names
	var xName = "x" + index;
	var yName = "data" + index;
	//Add X axis mapping
	plottableData.xs[yName] = xName;
	//Add x and y columns
	var xcolumn = [xName].concat(x);
	var ycolumn = [yName].concat(y);
	plottableData.columns.push(xcolumn);
	plottableData.columns.push(ycolumn);
	//Add types
	plottableData.types[yName] = "step";
}

function flattenSingleValueArrays(singleValueArrays) {
	return singleValueArrays.map(function(singleValueArray) {
		return singleValueArray[0];
	});
}

function plotSurvival(plottableData) {
	// console.debug("Plottable json", plottableData);
	var c3args = {
	    data: {
	        xs: plottableData.xs,
	        columns: plottableData.columns,
	        //Line curve is broken in Chrome, but step chart works
	        types: plottableData.types
	    },
	    axis: {
	    	x: {
	    		tick: {
	    			//TODO: Get x ticks as input
	    			values: calculateXTicks(12)
	    		}
	    	},
	    	y: {
	    		min: 0,
	    		max: 1,
	    		padding: { top: 0, bottom: 0}
	    	}
	    }
	};

	// console.debug("c3args", c3args);
	var chart = c3.generate(c3args);
}

function calculateXTicks(lengthOfExprimentInDays) {
	var ticks = [];
	for (var i=1; i<= lengthOfExprimentInDays; i++) {
		ticks.push(i);
	}
	return ticks;
}

function getRandomData() {
	// console.debug("getRandomData");
	$.ajax({
		type: "GET",
		url: "/random_data",
		success: serverJsonToPlottable
	});
}

//Input_data html functions below
function getFormData($form) {
	var unindexed_array = $form.serializeArray();
	var indexed_array = {};

	$.map(unindexed_array, function(n, i){
		indexed_array[n['name']] = n['value'];
	});
	return indexed_array;
}

/**
 * Serializes jQuery form object into required json 
 * object and submits form. JSON format is:
 *
 * {
		numberOfGroups: n,
		samplesInGroup: n,
		lengthOfExprimentInDays: n,
		dataSets: [
			{
				data: [n1, n2, ...],
				time: [t1, t2, ...]
			},
			{
				data: [n1, n2, ...],
				time: [t1, t2, ...]
			}
		]
	}
 * @param  {jQuery Object} formObj form jQuery object
 */
function submitForm(formObj) {
	// console.debug("submitForm", formObj);
	var data = {};
	//Integer inputs
	var integerInputs = ['numberOfGroups', 'samplesInGroup', 'lengthOfExprimentInDays'];
	integerInputs.forEach(function(inputName) {
		var input = getInput(inputName);
		var name = input.attr('name');
		var value = input.val();
		data[name] = value;
	});
	console.log(data);
	//Data sets
	var dataSets = [];
	for (var i=1; i <= data.numberOfGroups; i++) {
		var dataSet = {};
		var dataSeries = getInput("data" + i);
		var timeSeries = getInput("time" + i);
		dataSet["data"] = dataSeries.val().split(",");
		dataSet["time"] = timeSeries.val().split(",");
		console.log(dataSeries.val().split(","));
		dataSets.push(dataSet);
	}
	data["dataSets"] = dataSets;
	console.log(data);
	 
	$.ajax({
        method: "POST",
        url: "/generate_curve",
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: "json",
        success: function(data) {
        	console.debug("Post complete", data);
        	serverJsonToPlottable(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
        	alert(textStatus + errorThrown);
        }
    });
}

function getInput(inputName) {
	return $('form :input[name="' + inputName + '"]');
}

function submitData() {
	var form = $("form");
	var jsonFormattedData = getFormData(form);
	
	var time1 = document.getElementById('time1').value;
	var data1 = document.getElementById('data1').value;
	var time2 = document.getElementById('time2').value;
	var data2 = document.getElementById('data2').value;
	time1 = time1.split(",");
	console.log(time1);
	data1 = data1.split(",");
	time2 = time2.split(",");
	data2 = data2.split(",");

	var data = {};
	var dataSets = [];
	var dataSet = {};
	dataSet["time"] = time1;
	dataSet["data"] = data1;
	dataSets.push(dataSet);

	dataSet = {};
	dataSet["time"] = time2;
	dataSet["data"] = data2;
	dataSets.push(dataSet);

	data["dataSets"] = dataSets;
	
	// console.log(data);
	// console.log(JSON.stringify(data));
	//return jsonFormattedData;
	$.ajax({
        type: "POST",
        url: "/generate_curve",
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: "json",
        success: serverJsonToPlottable,
        failure: function(errMsg){alert(errMsg);
        }
    });
}
function serverJsonToPlottable(json) {
	console.debug("serverJsonToPlottable", json);
	var x = json.index;
	var y = json.data.map(function (singleArray) {
		return singleArray[0];
	});
	plotSurvival({
		x: x,
		data1: y
	});
}

function plotSurvival(json) {
	console.debug("Plottable json", json);
	var c3args = {
	    data: {
	        x: 'x',
	        columns: [
	            ['x'].concat(json.x),
	            ['data1'].concat(json.data1)
	        ],
	        //Line curve is broken in Chrome, but step chart works
	        types: {
	        	data1: "step"
	        }
	    }
	};

	console.debug("c3args", c3args);
	var chart = c3.generate(c3args);
}

function getRandomData() {
	console.debug("getRandomData");
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
	console.debug("submitForm", formObj);
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
		console.log(dataSeries.val().split(","))
		dataSets.push(dataSet);
	}
	data["dataSets"] = dataSets;
	console.log(data);
	console.log(JSON.stringify(data));
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
	
	console.log(data);
	console.log(JSON.stringify(data));
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
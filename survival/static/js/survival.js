// This example was created using Protovis & jQuery
// Base64 provided by http://www.webtoolkit.info/
function encode_as_img_and_link(){
 // Add some critical information
 $("svg").attr({ version: '1.1' , xmlns:"http://www.w3.org/2000/svg"});
 
 var svg = $("#chart-canvas").html();
 var b64 = Base64.encode(svg);
 
 // Works in recent Webkit(Chrome)
 $("body").append($("<img src='data:image/svg+xml;base64,\n"+b64+"' alt='file.svg'/>"));
 
 // Works in Firefox 3.6 and Webit and possibly any browser which supports the data-uri
 $("body").append($("<a href-lang='image/svg+xml' href='data:image/svg+xml;base64,\n"+b64+"' title='file.svg'>Download</a>"));
}

(function(){
 
  // var button_id = "download"
 
  // // include this code in your page
  // // you must have jQuery installed
  // // you must have a link element with an id of "download"
  // // this is limited to only one chart on the page (the first)
  // function encode_as_link(){
  //   // Add some critical information
  //   $("svg").attr({ version: '1.1' , xmlns:"http://www.w3.org/2000/svg"});
 
  //   var svg      = $("svg").parent().html(),
  //       b64      = window.btoa(svg),
  //       download = $("#download"),
  //       html     = download.html();
 
  //   download.replaceWith(
  //     $("<a id='"+button_id+"' href-lang='image/svg+xml' href='data:image/svg+xml;base64,\n"+b64+"'></a>").html(html));
  // }
 
  // $(function(){
  //   $("div").delegate("#"+button_id, "mouseover", encode_as_link);
  // });
 
})();

function fillSampleData() {
	var inputNames = {
		"numberOfGroups": 2,
		"lengthOfExprimentInDays": 100,
		"name1": "Group Uno",
		"samplesInGroup": 10,
		"type2_data1": "30,35,35,35,50,55,60,70,70,70",
		"name2": "Group Dos",
		"type2_data2": "60,75,79,85,85,85,90"
	};

	for (var inputName in inputNames) {
		$('input[name="' + inputName + '"]').val(inputNames[inputName]);
	}
}

function animateCurveDraw() {
	console.debug("animateCurveDraw");
	var formBox = $('.form-box');
	var curveBox = $('.curve-box');

	formBox.addClass('active');
	curveBox.addClass('active');

	submitForm($('#input-form1'));
}

function displayGraph() {
	$('#curve svg').css('overflow', 'visible');

	$('.curve-box').fadeIn(500);
}

function saveSvgAsFile() {
	var canvasElement = document.createElement('canvas');
	canvasElement.setAttribute('id', 'canvas');
	document.body.appendChild(canvasElement);
	canvg('canvas', $("#chart svg")[0].innerHTML);
	var img = canvasElement.toDataURL("image/png");
	document.write('<img src="' + img + '"/>');
}

function serverJsonToPlottable(results, data) {
	// console.debug("serverJsonToPlottable", results);
	
	var plottableData = {};
	plottableData.xs = {};
	plottableData.columns = [];
	plottableData.types = {};
	plottableData.lengthOfExprimentInDays = data.lengthOfExprimentInDays;
	
	//XXX: Result should always be an array, this is temp
	//If result is an object instead of array, no need to loop
	if (!$.isArray(results)) {
		singleResultToPlottable(plottableData, results, 0);
	} else {
		var datasets = results.map(function(result) {
			return JSON.parse(result);
		});
		datasets.forEach(function(dataset, index) {
			singleResultToPlottable(plottableData, data, dataset, index);
		});
	}

	plotSurvival(plottableData);
}

function singleResultToPlottable(plottableData, data, dataset, index) {
	//Get Data
	var x = dataset.index;
	var y = flattenSingleValueArrays(dataset.data);
	//Create Names
	var xName = "x" + index;
	var yName = data["name" + (index + 1)] || "data" + index;
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
		bindto: '#curve',
		size: {
			height: 400,
			width: 600
		},
	    data: {
	        xs: plottableData.xs,
	        columns: plottableData.columns,
	        //Line curve is broken in Chrome, but step chart works
	        types: plottableData.types
	    },
	    axis: {
	    	x: {
    			max: parseInt(plottableData.lengthOfExprimentInDays, 10),
    			//max: Math.ceil(parseInt(plottableData.lengthOfExprimentInDays, 10)/10)*10,
    			min: 0,
	    		tick: {
	    			//TODO: Get x ticks as input
	    			values: calculateXTicks(plottableData.lengthOfExprimentInDays),
	    			//culling: {
	    			//	max: 10
	    			//}
	    		}
	    	},
	    	y: {
	    		min: 0,
	    		max: 1,
	    		padding: { top: 0, bottom: 0, left: 50}
	    	}
	    },
	    grid: {
	        x: {
	            show: true
	        },
	        y: {
	            show: true
	        }
    	},
	    tooltip: {
		    show: false // Default true
		},

		regions: [
        {start:-10, end:parseInt(plottableData.lengthOfExprimentInDays, 10)+10, class: 'entire-chart' },
        ]


	};

	// console.debug("c3args", c3args);
	var chart = c3.generate(c3args);

	displayGraph();
}

function round(value, decimals) {
    return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}

function calculateXTicks(lengthOfExprimentInDays) {
	var ticks = [];
	var numTicks = 10;
	var threshRound = 250;
	var incrementNum = lengthOfExprimentInDays / numTicks;
	var testnum = Math.ceil(lengthOfExprimentInDays/10)*10
	var incrementNum = testnum / numTicks;
	var currTick = 0;
	ticks.push(currTick)
	for (var i=0; i<= numTicks; i++) {
		currTick = currTick + incrementNum;
		if(lengthOfExprimentInDays>threshRound)
			ticks.push(round(currTick,0));
		else
			ticks.push(round(currTick,1));
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
	var integerInputs = ['numberOfGroups', 'samplesInGroup', 'samplesInGroup', 'lengthOfExprimentInDays', 'name1', 'name2'];
	integerInputs.forEach(function(inputName) {
		var input = getInput(inputName);
		var value = input.val();
		data[inputName] = value;
	});
	console.log(data);
	//Data sets
	var dataSets = [];
	for (var i=1; i <= data.numberOfGroups; i++) {
		var dataSet = {};
		var dataSeries = getInput("type2_data" + i);
		var numSamples = getInput("samplesInGroup");
		var exprLength = getInput("lengthOfExprimentInDays");
		dataSet["data"] = dataSeries.val().split(",");
		dataSet["samplesInGroup"] = numSamples.val();
		dataSet["experimentLength"] = exprLength.val();
		dataSet["type"] = 2;
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
        success: function(results) {
        	console.debug("Post complete", results);
        	serverJsonToPlottable(results, data);
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
	dataSet["type"] = 1;
	dataSets.push(dataSet);

	dataSet = {};
	dataSet["time"] = time2;
	dataSet["data"] = data2;
	dataSet["type"] = 1;
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
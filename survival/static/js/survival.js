function serverJsonToPlottable(json) {
	console.debug("serverJsonToPlottable");
	var km_estimate = json["KM_estimate"];
	var estimate = [];
	for (var key in km_estimate) {
		var value = km_estimate[key];
		console.log("key", key, "value", value);
		estimate.push({key: value});
	}
	//Just to be safe, sort array
	// estimate.sort(function (a, b) {
	// 	//TODO
	// });
	console.log(estimate);
}

function getRandomData() {
	console.debug("getRandomData");
	$.ajax({
		type: "GET",
		url: "/random_data",
		success: serverJsonToPlottable
	});
}
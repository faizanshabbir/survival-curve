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

//Input_data html functions below
function getFormData($form) {
	var unindexed_array = $form.serializeArray();
	var indexed_array = {};

	$.map(unindexed_array, function(n, i){
		indexed_array[n['name']] = n['value'];
	});
	return indexed_array;
}

function submitData() {
	var form = $("form");
	jsonFormattedData = getFormData(form);
	console.log(jsonFormattedData);
	console.log(JSON.stringify(jsonFormattedData));

/*
	//MODIFY AJAX METHOD FOR POSTING WITH CSRF TOKEN
	$.ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*//*.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
	});
	//END AJAX METHOD
*/
	//return jsonFormattedData;
	$.ajax({
        type: "POST",
        url: "/generate_curve",
        data: JSON.stringify(jsonFormattedData),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){console.log(data);},
        failure: function(errMsg){alert(errMsg);
        }
    });

}
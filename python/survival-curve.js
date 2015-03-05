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

	return jsonFormattedData;

	$.ajax({
        type: "POST",
        url: "/",
        data: jsonFormattedData,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        /*success: function(data){alert(data);},
        failure: function(errMsg) {
            alert(errMsg);
        }*/
    });
}
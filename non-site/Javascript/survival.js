function test() {
	var chart = c3.generate({
	    data: {
	        x: 'x',
	        columns: [
	            ['x', 0, 0, 61, 61, 69, 69, 76, 76, 90, 90, 96, 96, 98, 98, 105, 105, 110, 110, 122, 122, 133, 133, 159, 159, 175, 175, 181, 181, 245, 245, 322, 322],
	            ['data1', 1, 1, 1, 0.95, 0.95, 0.9, 0.9, 0.85, 0.85, 0.75, 0.75, 0.7, 0.7, 0.55, 0.55, 0.45, 0.45, 0.4, 0.4, 0.35, 0.35, 0.25, 0.25, 0.2, 0.2, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05, 0],
	        ]
	        //Line curve is broken in Chrome, but step chart works
	    }
	});
}
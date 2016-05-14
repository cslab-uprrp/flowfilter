function updateViz(response, totalFlows){
	if(totalFlows == 0){
		document.getElementById('vizDate').innerHTML = "<h1>" + totalFlows + "</h1>"
	}
	else{
		if(typeof(response) == "string")
			var flows = JSON.parse(response).flows;
		else
			var flows = response;

		initTable(flows, totalFlows)

		document.getElementById('vizDate').innerHTML = "<h1>" + totalFlows + "</h1>"
		$('#vizDiv').removeClass('hidden');
	}
}
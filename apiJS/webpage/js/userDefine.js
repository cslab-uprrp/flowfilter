function updateViz(response){
	var response = response;
	// var obj = JSON.parse(response);
	// var flows = response.split("Response")[1]
	console.log(response);
	// var obj = JSON.parse(response).flows;
	// var obj1 = JSON.parse(obj[0])
	// var obj = JSON.parse(flows);
	// document.getElementById('vizDate').innerHTML =  flows + '\n <object width="1000" height="607" data="../ForceDirected/visForceDirected.html"></object>';
	// document.getElementById('vizDate').innerHTML = flows
	// console.log(response)
	console.log('babalisio');
	// console.log(flows)
	// console.log(JSON.parse(flows).flows);
	// console.log('duration: ' + obj[0].duration);
	// console.log('stime: ' + obj[0].stime);
}


// function updateViz(response){
// 	var response = response.substr(response.indexOf("\n")).trim();;
// 	// var respArray = response.split("\n")
// 	var flows = response.substr(0,response.indexOf("\n")).trim();
// 	response = response.substr(response.indexOf("\n")).trim();
// 	var viz = response.substr(response.indexOf("\n")).trim();
// 	// document.getElementById('vizDate').innerHTML =  flows + '\n <object width="1000" height="607" data="../ForceDirected/visForceDirected.html"></object>';
// 	document.getElementById('vizDate').innerHTML =  flows + '\n <object width="1000" height="607" data="'+viz+'"></object>';
// 	console.log('baba');
// 	// var str = response.substr(response.indexOf("\n")).trim();
// 	// str = str(str.substr(0, str.indexOf("\n")));
// 	console.log(viz);
// }
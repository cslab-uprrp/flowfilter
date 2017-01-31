var fillHours = function(){
	var startSelect = document.getElementById('selectstarttime');
	var endSelect = document.getElementById('selectendtime');

	for (var i = 1; i < 24; i++) {

		var option = document.createElement("option");
		var option1 = document.createElement("option");

		if (i < 10) {
			option.value = '0' + i;	
			option.text = '0' + i;

			option1.value = '0' + i;	
			option1.text = '0' + i;
		}
		else{
			option.value = i;	
			option.text = i;

			option1.value = i;	
			option1.text = i;
		}
		
		startSelect.add(option)
		endSelect.add(option1)	
	}
}

function showInput(option){
	if (option.value == "Other") {
		$('#inputEntries').removeClass('hidden');
	}
	else{
		$('#inputEntries').addClass('hidden');
	}
}

fillHours()
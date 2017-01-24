var records_per_page = 10;

    
function changePage(page)
{
    var table = document.getElementById("flowsTable");
    var flowsTableBody = document.createElement('tbody');
    var oldTbody = document.getElementById("flowsTableBody");
    flowsTableBody.setAttribute('id', 'flowsTableBody');
    oldTbody.parentNode.replaceChild(flowsTableBody, oldTbody);

    // Validate page
    if (page < 1) page = 1;
    if (page > numPages()) page = numPages();

    for(var i = 0; i < objJson.length; i++){

        if(i == objJson.length)
            break;

        var tr = document.createElement("tr");
        var tdSip = document.createElement("td");
        var tdDip = document.createElement("td");
        var tdSPort = document.createElement("td");
        var tdDPort = document.createElement("td");
        var tdBytes = document.createElement("td");
        var tdPackets = document.createElement("td");


        tdSip.appendChild(document.createTextNode(objJson[i].sip));
        tdDip.appendChild(document.createTextNode(objJson[i].dip));
        tdSPort.appendChild(document.createTextNode(objJson[i].sport));
        tdDPort.appendChild(document.createTextNode(objJson[i].dport));
        tdBytes.appendChild(document.createTextNode(objJson[i].bytes));
        tdPackets.appendChild(document.createTextNode(objJson[i].packets));

        tr.appendChild(tdSip);
        tr.appendChild(tdDip);
        tr.appendChild(tdSPort);
        tr.appendChild(tdDPort);
        tr.appendChild(tdBytes);
        tr.appendChild(tdPackets);

        flowsTableBody.appendChild(tr)
    }

    table.appendChild(flowsTableBody);
}

function changeEntries(entries){

    $('#loading').removeClass('hidden');
    $('#vizDiv').addClass('hidden');

    records_per_page = entries;
    var dropDownButton = document.getElementById("dropDownButton");
    dropDownButton.innerHTML = entries + ' <span class="caret"></span>';
    current_page = 1;
    changePage(1);
    validateNextPrev(1);

    getEntries = {
        first: (current_page-1) * records_per_page,
        last: current_page * records_per_page,
        currentPage: current_page,
        path: $("#filePathI").val(),
        vis: $("#selectVis").val()
    }

    var theForm = document.forms['myForm'];
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'entries';
    input.value = JSON.stringify(getEntries)
    theForm.appendChild(input);
    document.myForm.submit()
}


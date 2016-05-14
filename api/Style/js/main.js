function numPages(){
    return Math.ceil(amountOfEntries / records_per_page);
}

function validateNextPrev(page){
    if(page == 1){
        $("#prevButtonLi").addClass('disabled');
    }
    else{
        $("#prevButtonLi").removeClass('disabled');
    }

    if (page == numPages()) {
        $("#nextButtonLi").addClass('disabled');
    } 
    else {
        $("#nextButtonLi").removeClass('disabled');
    }

    var currentPage = document.getElementById("currentPage");
    currentPage.innerHTML = page;

    var amountOfEntriesDiv = document.getElementById("amountOfEntries");
    amountOfEntriesDiv.innerHTML = amountOfEntries;

    document.getElementById("numPages").innerHTML = numPages();

    var firstEntry = 0;
    var lastEntry = 0;



    if(amountOfEntries == 0){
        document.getElementById("firstEntry").innerHTML = firstEntry;
        document.getElementById("lastEntry").innerHTML = lastEntry;
    }
    else{
        firstEntry = ((page-1) * records_per_page) + 1;
        lastEntry = firstEntry + (records_per_page - 1);
        document.getElementById("firstEntry").innerHTML = firstEntry;
        document.getElementById("lastEntry").innerHTML = lastEntry;
    }

}

function nextEntries()
{   
    if (current_page < numPages()){

        $('#loading').removeClass('hidden');
        $('#vizDiv').addClass('hidden');

        current_page++;

        getEntries = {
            first: (current_page-1) * records_per_page,
            last: current_page * records_per_page,
            currentPage: current_page,
            path: $("#filePathI").val()
        }

        validateNextPrev(current_page);

        var theForm = document.forms['myForm'];
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'entries';
        input.value = JSON.stringify(getEntries)
        theForm.appendChild(input);
        document.myForm.submit()
    }
}
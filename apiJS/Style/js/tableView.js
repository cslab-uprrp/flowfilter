function initTable(objJson, amountOfEntries, records_per_page){
    var scope = angular.element(document.getElementById("MainDiv")).scope();
    setTimeout(function(){
        scope.$apply(function(){
            scope.initTable(objJson, amountOfEntries);
        })
    }, 1);
}
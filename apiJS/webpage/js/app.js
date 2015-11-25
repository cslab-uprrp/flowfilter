var app = angular.module('QuerySelector', ['ngSanitize']);


// This directive will let me use ng-show when parcing html using angular
app.directive('ngHtmlCompile', function($compile) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            scope.$watch(attrs.ngHtmlCompile, function(newValue, oldValue) {
                element.html(newValue);
                $compile(element.contents())(scope);
            });
        }
    }
});

app.controller('QuerySelectorCtrl', ['$scope', '$http', '$window',  function($scope, $http, $window) {
    $scope.disableButton = true

    $scope.selectedFilTemp = []
    $scope.selectedFilters = []

    $scope.start_date = new Date()
    $scope.end_date = new Date()

    $scope.data = {
     singleSelect: null,
     multipleSelect: [],
     option1: 'option-1',
    };

    $scope.response = ''


    $scope.FiltersDict = {
        "logic_input_output": 'and',
        "midLogic_input_output": 'and',
        //"logic_input" : 'or',
        "neg_input": '',
        "input" : "Input interface",
        "input-val": "",
        "input-e": false,
        // "logic_output": 'or',
        "neg_output": '',
        "output": "Output interface",
        "output-val": "",
        "output-e": false,
        // "logic_srcAS" : 'or',
        "logic_srcAS_dstAS": 'and',
        "midLogic_srcAS_dstAS": 'and',
        "neg_srcAS": '',
        "srcAS":"Source AS",
        "srcAS-val": "",
        "srcAS-e": false,
        // "logic_dstAS" : 'or',
        "neg_dstAS": '',
        "dstAS":"Destination AS",
        "dstAS-val": "",
        "dstAS-e": false,
        // "logic_sip" : 'or',
        "logic_sip_dip": 'and',
        "midLogic_sip_dip": 'and',
        "neg_sip": '',
        "sip":"Source IP",
        "sip-val": "",
        "sip-e": false,
        // "logic_dip" : 'or',
        "neg_dip": '',
        "dip":"Destination IP",
        "dip-val": "",
        "dip-e": false,
        // "logic_sport" : 'or',
        "logic_sport_dport": 'and',
        "midLogic_sport_dport": 'and',
        "neg_sport": '',
        "sport":"Source Port",
        "sport-val": "",
        "sport-e": false, 
        // "logic_dport" : 'or',
        "neg_dport": '',
        "dport":"Destination Port",
        "dport-val": "",
        "dport-e": false,
        
        "logic_bytes": "and",
        "bytes-e": false,
        "bytes-val": "",
        "bytes-op": ">",
        
        "logic_packets": "and",
        "packets-e": false,
        "packets-val": "",
        "packets-op": ">"
    }

    $scope.template = ' \
    <div class="row"> \
        <div class="col-md-1"> \
            <div ng-show = "checkIfLogic(\'name1\', \'name2\')"> \
                <div class="btn-group" data-toggle="buttons"> \
                      <label class="btn btn-primary" ng-click="updateLogic(\'name1\', \'name2\', \'or\')"> \
                        <input type="radio" name="options" id="option1" autocomplete="off" checked> or \
                      </label> \
                      <label class="btn btn-primary active" ng-click="updateLogic(\'name1\', \'name2\', \'and\')"> \
                        <input type="radio" name="options" id="option2" autocomplete="off"> and \
                      </label> \
                </div> \
            </div> \
        </div> \
        <div class="col-md-1"> \
                <div class="btn-group" data-toggle="buttons"> \
                    <label class="btn btn-danger" ng-click="updateNeg(\'name1\')"> \
                        <input type="checkbox"/> NOT \
                    </label> \
                </div> \
        </div> \
        \
        <div class="col-md-4" ng-show="FiltersDict[\'name1-e\']" class="ng-hide"> \
            <ul> \
                <li class="pull-left"> \
                    <button ng-click="removeFilter(\'name1\', \'name2\')" type="button" class="btn btn-danger" aria-label="Left Align"> \
                            <span class="glyphicon glyphicon-remove" aria-hidden="true"></span> \
                    </button> \
            </li> \
            <li class="pull-left"> \
                    <p> \
                        <label id="filterValue"> \
                            value1: \
                        </label> \
                        <input type="text" ng-model="FiltersDict[\'name1-val\']"> \
                    </p> \
                </li> \
            </ul> \
        </div> \
    \
        <div class="col-md-2" ng-show = "FiltersDict[\'name1-e\'] && FiltersDict[\'name2-e\']"> \
            <div> \
                <div class="btn-group" data-toggle="buttons" > \
                  <label class="btn btn-primary" ng-click="updateMidLogic(\'name1\', \'name2\', \'or\')"> \
                    <input type="radio" name="options" id="option1" autocomplete="off" checked> or \
                  </label> \
                  <label class="btn btn-primary active" ng-click="updateMidLogic(\'name1\',\'name2\', \'and\')"> \
                    <input type="radio" name="options" id="option2" autocomplete="off"> and \
                  </label> \
                </div>   \
                  <div class="btn-group" data-toggle="buttons"> \
                    <label class="btn btn-danger" ng-click="updateNeg(\'name2\')"> \
                        <input type="checkbox"> NOT \
                    </label>             \
                  </div>     \
            </div> \
        </div> \
        \
        <div class="col-md-4" ng-show="FiltersDict[\'name2-e\']" class="ng-hide"> \
            <ul>  \
                <li class="pull-left"> \
                    <button ng-click="removeFilter(\'name2\', \'name1\')" type="button" class="btn btn-danger" aria-label="Left Align"> \
                            <span class="glyphicon glyphicon-remove" aria-hidden="true"></span> \
                    </button> \
                </li> \
                <li class="pull-left"> \
                    <p> \
                        <label id="filterValue">\
                            value2:\
                        </label>\
                        <input type="text" ng-model="FiltersDict[\'name2-val\']">\
                    </p> \
                </li> \
            </ul> \
        </div> \
    </div>'

    $scope.templateOp = ' \
        <div class="row"> \
                <div class="col-md-1"> \
                    <div ng-show = "checkIfLogic(\'name1\', \'name2\')"> \
                        <div class="btn-group" data-toggle="buttons"> \
                              <label class="btn btn-primary" ng-click="updateLogic(\'name1\', \'name2\', \'or\')"> \
                                <input type="radio" name="options" id="option1" autocomplete="off" checked> or \
                              </label> \
                              <label class="btn btn-primary active" ng-click="updateLogic(\'name1\', \'name2\', \'and\')"> \
                                <input type="radio" name="options" id="option2" autocomplete="off"> and \
                              </label> \
                        </div> \
                    </div> \
                </div> \
                <div class="col-md-1"> \
                \
                </div> \
                <div class="col-md-3" ng-show="FiltersDict[\'name1-e\']" class="ng-hide" style="width: 20%; padding: 0%;"> \
                    <ul> \
                        <li class="pull-left"> \
                            <button ng-click="removeFilter(\'name1\', \'name2\')" type="button" class="btn btn-danger" aria-label="LeftAlign"> \
                                    <span class="glyphicon glyphicon-remove" aria-hidden="true"></span> \
                            </button> \
                    </li> \
                    <li class="pull-left"> \
                            <p> \
                                <label id="filterValue"> \
                                    value1: \
                                </label> \
                            </p> \
                        </li> \
                    </ul> \
                </div> \
                <div class="col-md-3" style="margin-left: -6%;width: 20%; padding: 0%;">\
                        <div class="btn-group" data-toggle="buttons"> \
                              <label class="btn btn-primary" ng-click="updateOp(\'name1\', \'<\')"> \
                                <input type="radio" name="options" id="option1" autocomplete="off" checked> &lt;\
                              </label> \
                              <label class="btn btn-primary" ng-click="updateOp(\'name1\', \'>\')"> \
                                <input type="radio" name="options" id="option2" autocomplete="off"> &gt;\
                              </label> \
                              <label class="btn btn-primary active" ng-click="updateOp(\'name1\', \'=\')"> \
                                <input type="radio" name="options" id="option1" autocomplete="off" checked> =\
                              </label> \
                              <label class="btn btn-primary" ng-click="updateOp(\'name1\', \'<=\')"> \
                                <input type="radio" name="options" id="option2" autocomplete="off"> &le;\
                              </label> \
                              <label class="btn btn-primary" ng-click="updateOp(\'name1\', \'>=\')"> \
                                <input type="radio" name="options" id="option2" autocomplete="off"> &ge;\
                              </label> \
                        </div> \
                </div>\
                <div class="col-md-2">\
                    <ul>\
                        <li class="pull-left"> \
                                <p> \
                                    <input type="text" ng-model="FiltersDict[\'name1-val\']"> \
                                </p> \
                        </li> \
                    </ul>\
                </div>\
        </div>\
            '

    $scope.buttonDep = function(){
        // if($scope.start_date != "" && $scope.end_date != "" && $scope.selectedFilTemp.length != 0){
        if($scope.selectedFilters.length != 0){
            $scope.disableButton = false
        }
        else{
            $scope.disableButton = true   
        }
    }

    //function to update the logic of a filter in the Filters dictionary
    $scope.updateLogic = function(filter1,filter2, logic){
        filter_logic ='logic_' + filter1 + '_' + filter2
        $scope.FiltersDict[filter_logic] = logic

        //this loop will change the filter logic in the selectedFilters dictionary
        for(item in $scope.selectedFilters){
            if($scope.selectedFilters[item].name == filter1 || $scope.selectedFilters[item].name == filter2){
                $scope.selectedFilters[item].logic_filter = logic
            }
        }
    }

    //function to update the operator of a filter in the Filters dictionary
    $scope.updateOp = function(filter, op){
        filter_op = filter + '-op'
        $scope.FiltersDict[filter_op] = op

        for(item in $scope.selectedFilters){
            if($scope.selectedFilters[item].name == filter){
                $scope.selectedFilters[item].operator = op
            }
        }
    }

    //mid logic is the logic that goes between the two filters (filter1 OR/AND filter2)
    $scope.updateMidLogic = function(filter1, filter2, logic){
        mid_logic ='midLogic_' + filter1 + '_' + filter2
        $scope.FiltersDict[mid_logic] = logic

        //this loop will change the mid filter logic in the selectedFilters dictionary
        for(item in $scope.selectedFilters){
            if($scope.selectedFilters[item].name == filter1 || $scope.selectedFilters[item].name == filter2){
                $scope.selectedFilters[item].midLogic_filter = logic
            }
        }
    }

    //function to update the negation of a filter in the Filters dictionary
    $scope.updateNeg = function(filter){
        neg_filter = 'neg_' + filter

        if($scope.FiltersDict[neg_filter] == ''){
            $scope.FiltersDict[neg_filter] = 'not'
        }
        else{
            $scope.FiltersDict[neg_filter] = ''
        }

        for(item in $scope.selectedFilters){
            if($scope.selectedFilters[item].name == filter){
                $scope.selectedFilters[item].neg_filter = $scope.FiltersDict[neg_filter]
            }
        }
    }

    $scope.addFilterOp = function(filterName, filterValue){
        if($scope.isSelected(filterName) == -1){   
            logic = 'logic_' + filterName      

            $scope.selectedFilters.push(
                {
                    logic_filter: $scope.FiltersDict[logic],
                    name: filterName,
                    value: $scope.FiltersDict[filterName+"-val"]
                }
            )

            $scope.changeTemplateOp(filterName, filterValue) 
            
            $scope.data.singleSelect = filterValue
            $scope.FiltersDict[filterName + "-e"] = true
        }    
        $scope.buttonDep()
    }


    $scope.addFilter = function(filterName, filterValue, secondFilter, inverted){
        if($scope.isSelected(filterName) == -1){            
            if(inverted){
                logic = 'logic_' + secondFilter + '_' + filterName
                midLogic = 'midLogic_' + secondFilter + '_' + filterName
            }
            else{
                logic = 'logic_' + filterName + '_' + secondFilter
                midLogic = 'midLogic_' + filterName + '_' + secondFilter
            }

            $scope.selectedFilters.push(
                {
                    logic_filter: $scope.FiltersDict[logic],
                    midLogic_filter: $scope.FiltersDict[midLogic],
                    name: filterName,
                    neg_filter: $scope.FiltersDict['neg_' + filterName],
                    value: $scope.FiltersDict[filterName+"-val"]
                }
            )

            $scope.changeTemplate(filterName, secondFilter, filterValue) 
            
            $scope.data.singleSelect = filterValue
            $scope.FiltersDict[filterName + "-e"] = true
        }     
        $scope.buttonDep()
    }

    //Since I am using a template to create the filters selectin in the webpage, I have to go trought the template and change the
    //different temporal names to the names of the filters that were selected and this function will help me with that
    $scope.changeTemplate = function(filter1, filter2, filter1Val){
        //This if will prevent of adding the two filters twice... because I am adding both in the first time and just hidding
        //the one that was not selected and then unhiding it when is selected.
        if(!($scope.FiltersDict[filter1 + "-e"] || $scope.FiltersDict[filter2 + "-e"])){
            $scope.newTemplate = $scope.template
            
            while($scope.newTemplate.search("name1") >= 0){
                $scope.newTemplate = $scope.newTemplate.replace('name1', filter1)
                $scope.newTemplate = $scope.newTemplate.replace('name2', filter2)
            }

            $scope.newTemplate = $scope.newTemplate.replace('value1', filter1Val)
            $scope.newTemplate = $scope.newTemplate.replace('value2', $scope.FiltersDict[filter2])
    
            $scope.selectedFilTemp.push({'name': filter1, 'template': $scope.newTemplate})
        }
    }

    $scope.changeTemplateOp = function(filter, filterVal){
        $scope.newTemplateOp = $scope.templateOp

        while($scope.newTemplateOp.search("name1") >= 0){
                $scope.newTemplateOp = $scope.newTemplateOp.replace('name1', filter)
        }

        $scope.newTemplateOp = $scope.newTemplateOp.replace('value1', filterVal)
        $scope.selectedFilTemp.push({'name': filter, 'template': $scope.newTemplateOp})
    }

    //helper function to verify if a filter is selected
    $scope.isSelected = function(filterName){
        for (var i = 0; i < $scope.selectedFilters.length; i++) {
            if($scope.selectedFilters[i].name == filterName){
                return i
            }
        };
        return -1;
    }

    $scope.removeFilter = function(filter1, filter2){
        //Pos of the filter in the selectedFilters list
        var filterPos = $scope.isSelected(filter1)

        //Disabling the filter, so it does not appear in the webpage (ng-show = false)
        $scope.FiltersDict[filter1 + "-e"] = false

        //removing the filter from the selected filters
        $scope.selectedFilters.splice(filterPos, 1);
        
        //Here if one of the two pair filters is enable we can't remove the template, because the template contains both filters
        //We are just going to remove the template when both filters are false (ng-show=false), otherwise we can't remove the template
        if(!($scope.FiltersDict[filter1 + "-e"] || $scope.FiltersDict[filter2 + "-e"])){
            for(var i = 0; i < $scope.selectedFilTemp.length; i++){
                var filterName = $scope.selectedFilTemp[i].name
                if(filterName == filter1 || filterName == filter2){
                    $scope.selectedFilTemp.splice(i, 1)
                }
            }
        }

        $scope.buttonDep()
    }

    //With this function we are verifying if the filter needs the first logic, because if the filter is in the first position of 
    //the selection list, then it does not need the first logic
    $scope.checkIfLogic = function(filter1, filter2){
        var firstFilter = ''
        if($scope.selectedFilTemp.length >= 2){
            firstFilter = $scope.selectedFilTemp[0].name
            if(firstFilter == filter1 || firstFilter == filter2){
                return false
            }
            else if($scope.isSelected(filter1) >= 0 || $scope.isSelected(filter2) >= 0){
                return true
            }
            else{
                return false
            }
        }
        // if($scope.selectedFilters.length >= 2){
        //     firstFilter = $scope.selectedFilters[0].name
        //     if($scope.selectedFilters[0].name == filter1 || $scope.selectedFilters[0].name == filter2){
        //         return false
        //     }
        //     else if($scope.isSelected(filter1) >= 0 || $scope.isSelected(filter2) >= 0){
        //         return true
        //     }
        //     else{
        //         return false
        //     }
        // }
        else{
            return false
        }
    }

    $scope.updateSelectedFilters = function(){
        for (var i = 0; i < $scope.selectedFilters.length; i++) {
            var filterName = $scope.selectedFilters[i].name
            $scope.selectedFilters[i].value = $scope.FiltersDict[filterName+"-val"]
        }
    }

    $scope.getResults = function(){
        $scope.updateSelectedFilters()
        finalData = {data: $scope.selectedFilters}
        // console.log(finalData)
        console.log($scope.selectedFilters)
        startDate = $scope.start_date.getFullYear() + "/" + ($scope.start_date.getMonth()+1) + "/" + $scope.start_date.getDate(),
        endDate = $scope.end_date.getFullYear() + "/" + ($scope.end_date.getMonth()+1) + "/" + $scope.end_date.getDate()
        console.log("start: " + startDate)
        console.log("end: " + endDate)
        $http({
            method: 'GET',
            // url: 'http://lagrange.ccom.uprrp.edu/~jdelacruz/webflows/gui/processData.cgi',
            // url: 'http://wolverine.ccom.uprrp.edu/~jdelacruz/netFlows/processData.cgi',
            url: 'http://wolverine.ccom.uprrp.edu/~jdelacruz/netFlows/api/prueba.cgi',
            params: {
                data:   finalData,
                        start: $scope.start_date.getFullYear() + "/" + ($scope.start_date.getMonth()+1) + "/" + $scope.start_date.getDate(),
                        end: $scope.end_date.getFullYear() + "/" + ($scope.end_date.getMonth()+1) + "/" + $scope.end_date.getDate()
            }
        }).success(function(response) {
            // console.log(response)
            updateViz(response)
            // $window.location.href = 'justTest.cgi';
            // this callback will be called asynchronously
            // when the response is available
          }). 
            error(function(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
          });
    }
}]);
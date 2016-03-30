#!/usr/bin/python
import cgi, cgitb
from silk import *
import json
import os
import time
from webflow import *
from ian import *
from TreeMap import *

print """Content-length:1000000000;"""
print """Content-type:text/html\r\n\r\n"""
print

def receiveData(form):
	data = form.getvalue("data")
	data = json.loads(data)
	startDate = str(data['start'])
	endDate = str(data['end'])
	filteredData = data['filteredData']
	path = data['path']
	data = data['data']

	return data, startDate, endDate, filteredData, path

form = cgi.FieldStorage()

# f = open("temp.txt", "wb")

if(form.has_key("data")):
	printFilterPage()

	# print """<script> $('#pleaseWaitDialog').modal('show'); </script>"""
	
	data, startDate, endDate, useFilteredData, pathOfFilteredData = receiveData(form)

	flows, filePath = processData(data, startDate, endDate, useFilteredData, pathOfFilteredData)
	fl = json.loads(toJson(flows))
	fl = fl['flows']
	print fl is str
	print """<h3> Flows: """+str(len(flows))+"""</h3>"""
	print """ <script type="text/javascript"> 
	var current_page = 1; 
	var records_per_page = 10; """
	# print "var objJson = %s"%(str(toJson(flows)))
	print "var objJson = []"#%s"%(str(fl))
	print """ 
    function prevPage()
    {
        if (current_page > 1) {
            current_page--;
            changePage(current_page);
        }
    }

    function nextPage()
    {
        if (current_page < numPages()) {
            current_page++;
            changePage(current_page);
        }
    }
        
    function changePage(page)
    {
        var btn_next = document.getElementById("btn_next");
        var btn_prev = document.getElementById("btn_prev");
        // var listing_table = document.getElementById("listingTable");
        var page_span = document.getElementById("page");

        var table = document.getElementById("flowsTable");
        var flowsTableBody = document.createElement('tbody');
        var oldTbody = document.getElementById("flowsTableBody");
        flowsTableBody.setAttribute('id', 'flowsTableBody');
        oldTbody.parentNode.replaceChild(flowsTableBody, oldTbody);

        // Validate page
        if (page < 1) page = 1;
        if (page > numPages()) page = numPages();
        page_span.innerHTML = page;

        // listing_table.innerHTML = "";

        document.getElementById("firstEntryInTable").innerHTML = ((page-1) * records_per_page)+1
        // $("firstEntryInTable").html((page-1) * records_per_page);
        var i = 0;
        for (i = (page-1) * records_per_page; i < (page * records_per_page); i++) {

            if(i == objJson.length)
                break;

            var tr = document.createElement("tr");
            var tdSip = document.createElement("td");
            var tdDip = document.createElement("td");
            var tdBytes = document.createElement("td");
            tdSip.appendChild(document.createTextNode(objJson[i].sip));
            tdDip.appendChild(document.createTextNode(objJson[i].dip));
            tdBytes.appendChild(document.createTextNode(objJson[i].dport));

            tr.appendChild(tdSip);
            tr.appendChild(tdDip);
            tr.appendChild(tdBytes);

            flowsTableBody.appendChild(tr)

            // listing_table.innerHTML += objJson[i].dip + "<br>";
            if(page == numPages()){
                // btn_next.style.visibility = "hidden";
                $("#li_next").addClass('disabled');
            }
        }
        document.getElementById("lastEntryInTable").innerHTML = i;
        // $("lastEntryInTable").html(i);
        // oldTbody.parentNode.replaceChild(flowsTableBody, oldTbody);
        table.appendChild(flowsTableBody);

        page_span.innerHTML = page;

        if (page == 1) {
            // btn_prev.style.visibility = "hidden";
            $("#li_prev").addClass('disabled');
        } else {
            // btn_prev.style.visibility = "visible";
            $("#li_prev").removeClass('disabled');
        }

        if (page == numPages()) {
            // btn_next.style.visibility = "hidden";
            $("#li_next").addClass('disabled');
        } else {
            // btn_next.style.visibility = "visible";
            $("#li_next").removeClass('disabled');
        }
    }

    function numPages()
    {
        return Math.ceil(objJson.length / records_per_page);
    }

    function changeEntries(entries){
        records_per_page = entries;
        var dropDownButton = document.getElementById("dropDownButton");
        dropDownButton.innerHTML = entries + ' <span class="caret"></span>';
        current_page = 1;
        changePage(1);
    }

	</script>
		<section>
			<div class="row>
				<div class="md-col-6"> Hola Papa 
					<div class="dropdown">
						Show
					    <button id="dropDownButton"class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">10
					    <span class="caret"></span></button>
					    <ul class="dropdown-menu">
					      <li><a href="#" onclick="changeEntries(10);">10</a></li>
					      <li><a href="#" onclick="changeEntries(25);">25</a></li>
					      <li><a href="#" onclick="changeEntries(50);">50</a></li>
					      <li><a href="#" onclick="changeEntries(100);">100</a></li>
					    </ul>
					    entries
					  </div>
					</div>
				</div>
				<div class="col-md-6" style="text-align: right; padding-top: 1.5%;">
					Page: <span id="page"></span>
				</div>
			</div>

			<!-- <label>
				Show 
				<select class="form-control input-sm" aria-controls="example" name="example_length">
					<option value="10">10</option>
					<option value="25">25</option>
					<option value="50">50</option>
					<option value="100">100</option>
				</select> 
				entries
			</label>

			 -->



			<table id = "flowsTable" class = "table table-striped table-hover table-condensed table-bordered">
			   <!-- <caption>Striped Table Layout</caption> -->
			   
			   <thead>
			      <tr>
			         <th>Source IP</th>
			         <th>Destination IP</th>
			         <th>Bytes</th>
			      </tr>
			   </thead>
			   
			   <tbody id ="flowsTableBody">
			      <tr>
			         <td>Tanmay</td>
			         <td>Bangalore</td>
			         <td>560001</td>
			      </tr>
			      
			      <tr>
			         <td>Sachin</td>
			         <td>Mumbai</td>
			         <td>400003</td>
			      </tr>
			      
			      <tr>
			         <td>Uma</td>
			         <td>Pune</td>
			         <td>411027</td>
			      </tr>
			   </tbody>
			   
			</table>
			<div class="row" style="margin-top: -1%;">
				<div id="showingEntriesDiv" class="col-md-6">
					Showing <span id="firstEntryInTable"></span> to <span id="lastEntryInTable"></span> of <span id="amountOfEntries"></span> entries.
				</div>
				<div class="col-md-6" style="text-align:right;">
					<ul id = "pagination" class="pagination">
					    <li id="li_prev">
					      <a href="#flowsTableSec" onclick="prevPage()" id="btn_prev">
					        <span aria-hidden="true">&laquo;</span>
					        Prev
					      </a>
					    </li>
					    <li id="li_next">
					    	<a href="#flowsTableSec" onclick="nextPage()" id="btn_next">Next
					        <span aria-hidden="true">&raquo;</span>
					      </a>
					    </li>
					</ul>
				</div>
			</div>
		</section>
	"""

	# graph = TreeMap(flows)
	# graph = ForceDirected(flows)

	# print len(flows)

	# pages = len(flows)/50
	# pagesRem = int(50*(len(flows)/50.0 - pages))


	# print """ <ul class="pagination"> """

	# for i in range(pages):
	# 	print """ <li><a href="#">%d</a></li> """%(i+1)

	# if pagesRem:
	# 	print """ <li><a href="#">%d</a></li> """%(pages + 1)
	# # for j in range()

	# print """ </ul> """
	# print """
	# 	  <ul class="pagination">
	# 	    <li><a href="#">1</a></li>
	# 	    <li><a href="#">2</a></li>
	# 	    <li><a href="#">3</a></li>
	# 	    <li><a href="#">4</a></li>
	# 	    <li><a href="#">5</a></li>
	# 	  </ul>
	# """

	# print '<br/>'
	# for fl in flows:
		# print '<br/>'
		# print fl.sip
		# print fl.sport

	# print 'blaba'
	# time.sleep(3)
	# print """<script> $('#pleaseWaitDialog').modal('hide'); </script>"""

else:
	printFilterPage()
	print "There is no filter..."

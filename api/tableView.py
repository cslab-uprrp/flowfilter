setFilePath = """<script> $("#filePathI").val("%s"); </script>"""

setTableValues = """
	<script>
		var current_page = %s;
		var records_per_page = %s;
		var flows = '%s';
		var objJson = JSON.parse(flows).flows;
		var amountOfEntries = %s;
	</script>
"""

sectionTableTag = """
<div id = "vizDiv" class="container">
		<section id="flowsTableSec">
			<div class="row">
				<div class="col-md-6" style="text-align: left; margin-bottom: 1%;">
				  <div class="dropdown">
				  	Show
				    <button id="dropDownButton"class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown">10
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


			<table id = "flowsTable" class = "table table-striped table-hover table-condensed table-bordered">
			   <thead>
			      <tr>
			         <th>Source IP</th>
			         <th>Destination IP</th>
			         <th>Source Port</th>
			         <th>Destination Port</th>
			         <th>Bytes</th>
			         <th>Packets</th>
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


			</section>
</div>
"""

initTableScript = """
	<script>
		changePage(current_page);
		var dropDownButton = document.getElementById("dropDownButton");
    	dropDownButton.innerHTML = records_per_page + ' <span class="caret"></span>';
    	validateNextPrev(current_page);
	</script>
"""
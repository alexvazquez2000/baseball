<?php
include 'config.php';
include 'templates/header.php';
?>

<h1><?= htmlspecialchars($PAGE_TITLE) ?></h1>
<form method="post">
  <input type="hidden" name="id" value="<?= $parent->id ?>">
  <div class="mb-3">
    <label for="name" class="form-label">Name</label>
    <input type="text" name="name" class="form-control" value="<?= htmlspecialchars($parent->name) ?>" required />
  </div>
  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" name="email" class="form-control" value="<?= htmlspecialchars($parent->email) ?>" />
  </div>
  <div class="mb-3">
    <label for="phone" class="form-label">Phone</label>
    <input type="text" name="phone" class="form-control" value="<?= htmlspecialchars($parent->phone) ?>" />
  </div>
  <button type="submit" class="btn btn-primary">Save</button>
  <a href="list_parents.php" class="btn btn-secondary">Cancel</a>
</form>


<h2>List players (children)</h2>
<table id="players" class="table table-striped">
  <thead>
    <tr>
      <th>Name</th>
      <th>DOB</th>
      <th>Jersey Number</th>
      <th>Edit</th>
    </tr>
  </thead>
  <tbody id="childrenTableBody">
<?php
  if (!empty($players)) {
    foreach ($players as $player) {
		#TODO: html escape
      echo "<tr><td>{$player->name}</td>\n<td>{$player->date_of_birth}</td>\n";
      echo "<td>{$player->jersey_number}</td>\n";
      echo "<td><a href=\"edit_player.php?id={$player->id}\" class=\"btn btn-sm btn-primary\">Edit</a></td>\n</tr>\n";
    }
  } else {
    echo "<tr><td colspan=\"4\">No players found.</td></tr>\n";
  }
?>
  </tbody>
</table>

<form action="">
  <label for="fname">Name:</label>
  <input type="text" id="fname" name="fname" onkeyup="showHint(this.value)" placeholder="Search for names..">
</form>
<p><span id="txtHint"></span></p>
TODO: these are not yet being saved
<a href="list_parents.php">Back</a>

<script>
//track new children
var childrenPlayers = [ ];

function addPlayer(id, childName, childDOB, jersey) {
	
	if (!childrenPlayers.includes(id)) {
		childrenPlayers.push(id);
		console.log("Added " + id + " new array= " + childrenPlayers);
		const tableBody = document.getElementById('childrenTableBody');
		const row = document.createElement('tr');
		row.id = "child" +  id;
		const cell1 = document.createElement('td');
		const cell2 = document.createElement('td');
		const cell3 = document.createElement('td');
		const cell4 = document.createElement('td');
		
		cell1.textContent = childName;
		cell2.textContent = childDOB;
		cell3.textContent = jersey;
		
		let rmButton = document.createElement('button');
		rmButton.textContent = 'X';
		rmButton.onclick = function() { removePlayer(id); };
		cell4.appendChild(rmButton);
		
		row.appendChild(cell1);
		row.appendChild(cell2);
		row.appendChild(cell3);
		row.appendChild(cell4);
		tableBody.appendChild(row);
		
	} else {
		console.log("Skipped adding id= " + id );
	}
	//clear the table results after a button is pushed
	const hint = document.getElementById('txtHint');
	hint.textContent="";
	//maybe also delete the elementid=fname ?
}

function removePlayer(p) {
	// Check if the item exists and filter it out
	if (childrenPlayers.includes(p)) {
		//The filter() method creates a new array with all elements that pass the test implemented 
		childrenPlayers = childrenPlayers.filter(item => item !== p);
		rowToRemove = document.getElementById("child" + p);
		rowToRemove.remove();
	}
	console.log("Deleted " + p + " new array= " + childrenPlayers);
	//clear the table results after a button is pushed
	const hint = document.getElementById('txtHint');
	hint.textContent="";
	//maybe also delete the elementid=fname ?
}

//TODO:  this is not yet saving the added rows
//TODO: need to allow to delete an existing row

function showHint(str) {
  if (str.length == 0) {
    document.getElementById("txtHint").innerHTML = "";
    return;
  } else {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onload = function() {
        const myObj = JSON.parse(this.responseText);
        let text = "<table border='1'>"
        for (let x in myObj) {
          var id = parseInt(myObj[x].id);
          text += "<tr><td>" + myObj[x].name + "</td><td>" + myObj[x].date_of_birth  + "</td>"
            + "<td>&nbsp; #" + myObj[x].jersey_number + "</td>";
          if (childrenPlayers.includes(id)) {
            //danger make it red,  info=light blue
            text += "<td><button onclick=\"removePlayer(" + id +")\" class=\"btn btn-sm btn-danger\">Delete</button></td>";
          } else {
        	  text += "<td><button onclick=\"addPlayer(" + id + ",'" + myObj[x].name  + "','"
        	  	+ myObj[x].date_of_birth + "','" + myObj[x].jersey_number + "')\" class=\"btn btn-sm btn-info\">Add</button></td>";
          }
          text += "</tr>";
        }
        text += "</table>"
        document.getElementById("txtHint").innerHTML = text;
      }
    xmlhttp.open("POST",  "gethints.php", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("playerNameStartsWith=" + str);
  }
}
</script>
<?php include 'templates/footer.php'; ?>

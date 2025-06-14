<?php
include 'config.php';
include 'templates/header.php';
?>

<h1>Players</h1>
<br>
<a href="add_player.php" class="btn btn-success mb-2">Add Player</a>
<br>
<input type="text" id="search" onkeyup="filterByName()" placeholder="Search for names..">
<table class="table table-striped" id="filteredTable">
  <thead>
    <tr>
      <th onclick="sortTable(0)">Name</th>
      <th onclick="sortTable(1)">DOB</th>
      <th onclick="sortTable(2)">Jersey Number</th>
      <th>Edit</th>
    </tr>
  </thead>
  <tbody>
<?php
  if (!empty($players)) {
    foreach ($players as $player) {
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

<?php include 'templates/footer.php'; ?>

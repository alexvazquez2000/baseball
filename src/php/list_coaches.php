<?php include 'config.php'; ?>
<?php include 'templates/header.php'; ?>

<h1>Coaches</h1>
<br>
<a href="add_coach.php" class="btn btn-success mb-2">Add Coach</a>
<br>
<input type="text" id="search" onkeyup="filterByName()" placeholder="Search for names..">
<table class="table table-striped" id="filteredTable">
  <thead>
    <tr>
      <th onclick="sortTable(0)">Name</th>
      <th onclick="sortTable(1)">Email</th>
      <th onclick="sortTable(2)">Phone</th>
      <th>Edit</th>
    </tr>
  </thead>
  <tbody>
  <?php
    if (!empty($coaches)) {
      foreach ($coaches as $coach) {
        echo "<tr><td>{$coach->name}</td>\n";
        echo "<td>{$coach->email}</td>\n";
        echo "<td>{$coach->phone}</td>\n";
        echo "<td><a href=\"edit_coach.php?id={$coach->id}\" class=\"btn btn-sm btn-primary\">Edit</a></td>\n</tr>\n";
      }
    } else {
      echo "<tr><td colspan=\"4\">No coaches found.</td></tr>\n";
    }
  ?>
  </tbody>
</table>

<?php include 'templates/footer.php'; ?>

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
        echo "<tr>";
        echo "<td><img src=\"uploads/{$coach->photo}\" width=\"80\"></td>";
        echo "<td>{$coach->name}</td>\n";
        echo "<td>{$coach->email}</td>\n";
        echo "<td><a href=\"tel:{$coach->phone}\">{$coach->phone}</a></td>\n";
        echo "<td><a href=\"edit_coach.php?id={$coach->id}\" class=\"btn btn-sm btn-primary\">Edit</a></td>";
        echo "<td><a href=\"delete.php?id={$coach->id}\" class=\"btn btn-sm\" onclick=\"return confirm('Are you sure?')\">Delete</a></td>";
        echo "\n</tr>\n";
      }
    } else {
      echo "<tr><td colspan=\"4\">No coaches found.</td></tr>\n";
    }
  ?>
  </tbody>
</table>

<?php include 'templates/footer.php'; ?>

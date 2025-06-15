<?php include 'config.php'; ?>
<?php include 'templates/header.php';
?>

<h1>Parents</h1>
<br>
<a href="add_parent.php" class="btn btn-success mb-2">Add Parent</a>
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
    if (!empty($parents)) {
      foreach ($parents as $parent) {
        echo "<tr><td>{$parent->name}</td>\n";
        echo "<td>{$parent->email}</td>\n";
        echo "<td><a href=\"tel:{$parent->phone}\">{$parent->phone}</a></td>\n";
        echo "<td><a href=\"edit_parent.php?id={$parent->id}\" class=\"btn btn-sm btn-primary\">Edit</a></td>\n</tr>\n";
      }
    } else {
      echo "<tr><td colspan=\"4\">No parents found.</td></tr>\n";
    }
  ?>
  </tbody>
</table>

<?php include 'templates/footer.php'; ?>
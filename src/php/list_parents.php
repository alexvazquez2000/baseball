<?php include 'config.php'; ?>
<?php include 'templates/header.php'; ?>
<h1>Parents</h1>
<ul>
</ul>
<h2>Parents</h2>
<a href="add_parent.php" class="btn btn-success mb-2">Add Parent</a>

<table class="table table-striped">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Phone</th>
      <th>Edit</th>
    </tr>
  </thead>
  <tbody>
  <?php
    if (!empty($parents)) {
      foreach ($parents as $parent) {
        echo "<tr><td>{$parent->name}</td>\n";
        echo "<td>{$parent->email}</td>\n";
        echo "<td>{$parent->phone}</td>\n";
        echo "<td><a href=\"edit_parent.php?id={$parent->id}\" class=\"btn btn-sm btn-primary\">Edit</a></td>\n</tr>\n";
      }
    } else {
      echo "<tr><td colspan=\"4\">No parents found.</td></tr>\n";
    }
  ?>
  </tbody>
</table>

<?php include 'templates/footer.php'; ?>
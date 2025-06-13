<?php include 'config.php'; ?>
<?php include 'templates/header.php'; ?>
<h1>Coaches</h1>

<a href="add_coach.php" class="btn btn-success mb-2">Add Coach</a>

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
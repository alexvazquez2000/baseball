<?php
include 'config.php';
include 'templates/header.php';
?>

<h2>Edit Parent</h2>
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
<table class="table table-striped">
  <thead>
    <tr>
      <th>Name</th>
      <th>DOB</th>
      <th>Jersey Number</th>
      <th>Edit</th>
    </tr>
  </thead>
  <tbody>
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

<a href="list_parents.php">Back</a>

<?php include 'templates/footer.php'; ?>

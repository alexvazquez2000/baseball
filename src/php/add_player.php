<?php
include 'config.php';
include 'templates/header.php';
?>

<h2>Add Player</h2>
<form method="post">
  <div class="mb-3">
    <label for="name" class="form-label">Name</label>
    <input type="text" name="name" class="form-control" required />
  </div>
  <div class="mb-3">
    <label for="date_of_birth" class="form-label">Date of Birth</label>
    <input type="date" name="date_of_birth" class="form-control" required />
  </div>
  <div class="mb-3">
    <label for="jersey_number" class="form-label">Jersey Number</label>
    <input type="number" name="jersey_number" class="form-control" required />
  </div>
  <button type="submit" class="btn btn-primary">Add Player</button>
  <a href="list_players.php" class="btn btn-secondary">Cancel</a>
</form>

<?php include 'templates/footer.php'; ?>

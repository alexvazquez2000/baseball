<?php
include 'config.php';
include 'templates/header.php';
?>
<h2>Edit Player</h2>
<form method="post">
  <input type="hidden" name="id" value="<?= $player->id ?>">
  <div class="mb-3">
    <label for="name" class="form-label">Name</label>
    <input type="text" name="name" class="form-control" value="<?= htmlspecialchars($player->name) ?>" required />
  </div>
  <div class="mb-3">
    <label for="date_of_birth" class="form-label">Date of Birth</label>
    <input type="date" name="date_of_birth" class="form-control" value="<?= htmlspecialchars($player->date_of_birth) ?>" required />
  </div>
  <div class="mb-3">
    <label for="jersey_number" class="form-label">Jersey Number</label>
    <input type="number" name="jersey_number" class="form-control" value="<?= htmlspecialchars($player->jersey_number) ?>" required />
  </div>
  <button type="submit" class="btn btn-primary">Save</button>
  <a href="list_players.php" class="btn btn-secondary">Cancel</a>
</form>


<?php include 'templates/footer.php'; ?>

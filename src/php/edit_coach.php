<?php
include 'config.php';
include 'templates/header.php';
?>

<h2>Edit Coach</h2>
<form method="post">
	<input type="hidden" name="id" value="<?= $coach->id ?>">
  <div class="mb-3">
    <label for="name" class="form-label">Name</label>
    <input type="text" name="name" class="form-control" value="<?= $coach->name ?>" required />
  </div>
  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" name="email" class="form-control" value="<?= $coach->email ?>" />
  </div>
  <div class="mb-3">
    <label for="phone" class="form-label">Phone</label>
    <input type="text" name="phone" class="form-control" value="<?= $coach->phone ?>" />
  </div>
  <button type="submit" class="btn btn-primary">Save</button>
  <a href="list_coaches.php" class="btn btn-secondary">Cancel</a>
</form>

<h2>(TODO: add teams)</h2>

<?php include 'templates/footer.php'; ?>

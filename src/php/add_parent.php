<?php
include 'config.php';
include 'templates/header.php';
?>

<h2>Add Parent</h2>
<form method="post">
  <div class="mb-3">
    <label for="name" class="form-label">Name</label>
    <input type="text" name="name" class="form-control" required />
  </div>
  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" name="email" class="form-control" />
  </div>
  <div class="mb-3">
    <label for="phone" class="form-label">Phone</label>
    <input type="text" name="phone" class="form-control" />
  </div>
  <button type="submit" class="btn btn-primary">Add Parent</button>
  <a href="list_parents.php" class="btn btn-secondary">Cancel</a>
</form>

<?php include 'templates/footer.php'; ?>

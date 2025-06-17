<?php
include 'config.php';
include 'templates/header.php';
?>

<h2><?= htmlspecialchars($PAGE_TITLE) ?></h2>
<form method="post">
	<input type="hidden" name="id" value="<?= $coach->id ?>">
  <div class="mb-3">
    <label for="name" class="form-label">Name</label>
    <input type="text" name="name" class="form-control" value="<?= htmlspecialchars($coach->name) ?>" required />
  </div>
  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" name="email" class="form-control" value="<?= htmlspecialchars($coach->email) ?>" />
  </div>
  <div class="mb-3">
    <label for="phone" class="form-label">Phone</label>
    <input type="text" name="phone" class="form-control" value="<?= htmlspecialchars($coach->phone) ?>" />
  </div>
  
  <div>
    <video id="video" width="200" autoplay style="display: none;"></video>
    <canvas id="canvas" style="display: none;"></canvas>

    <button type="button" id="captureBtn">Start Camera / Take Photo</button><br>

    <!-- Fallback upload -->
    <div id="fallback-upload" style="margin-top: 10px;">
        <label>If camera is unavailable, upload a photo:</label><br>
        <input type="file" id="fileUpload" accept="image/*">
    </div>

    <input type="hidden" name="photo_filename" id="photo_filename" value="<?= $coach->photo ?>">
    <br>
    <img id="preview" src="uploads/<?= $coach->photo ?>" width="100" style="<?= $coach->photo ? '' : 'display:none;' ?>">
  </div>
  
  <button type="submit" class="btn btn-primary">Save</button>
  <a href="list_coaches.php" class="btn btn-secondary">Cancel</a>
</form>

<h2>(TODO: add teams)</h2>


<script src="js/photo_capture.js"></script>

<?php include 'templates/footer.php'; ?>

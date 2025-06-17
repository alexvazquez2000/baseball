<?php
include 'config.php';
include 'templates/header.php';
?>
<h2>Add Coach</h2>
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

  <div>
    <video id="video" width="200" autoplay style="display: none;"></video>
    <canvas id="canvas" style="display: none;"></canvas>

    <button type="button" id="captureBtn">Start Camera / Take Photo</button><br>

    <!-- Fallback upload -->
    <div id="fallback-upload" style="margin-top: 10px;">
        <label>If camera is unavailable, upload a photo:</label><br>
        <input type="file" id="fileUpload" accept="image/*">
    </div>

    <input type="hidden" name="photo_filename" id="photo_filename" value="">
    <br>
    <img id="preview" src="" width="100" style="display:none;">
  </div>

  <button type="submit" class="btn btn-primary">Add Coach</button>
  <a href="{{ url_for('list_coaches') }}" class="btn btn-secondary">Cancel</a>
</form>

<script src="js/photo_capture.js"></script>

<?php include 'templates/footer.php'; ?>

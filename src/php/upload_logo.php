<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["logo"])) {
    $target_dir = "uploads/";
    $target_file = $target_dir . basename($_FILES["logo"]["name"]);
    if (move_uploaded_file($_FILES["logo"]["tmp_name"], $target_file)) {
        echo "Logo uploaded: " . basename($_FILES["logo"]["name"]);
    } else {
        echo "Upload failed.";
    }
}
?>
<form method="post" enctype="multipart/form-data">
    Select logo to upload (PNG/GIF):
    <input type="file" name="logo"><br>
    <input type="submit" value="Upload Logo">
</form>

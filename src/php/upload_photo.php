<?php
$filename = uniqid() . '.jpg';
#handle both camera blobs and file uploads
move_uploaded_file($_FILES['photo']['tmp_name'], "uploads/$filename");
echo $filename;

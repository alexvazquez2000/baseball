<?php
$filename = uniqid() . '.jpg';
file_put_contents("uploads/$filename", file_get_contents($_FILES['photo']['tmp_name']));
echo $filename;

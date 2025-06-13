<?php include 'config.php'; ?>
<?php include 'templates/header.php'; ?>
<h1>Parents</h1>
<ul>
<?php
$stmt = $pdo->query("SELECT * FROM parents");
while ($row = $stmt->fetch()) {
    echo "<li>{$row['name']} - <a href='edit_parent.php?id={$row['id']}'>Edit</a></li>\n";
}
?>
</ul>
<?php include 'templates/footer.php'; ?>
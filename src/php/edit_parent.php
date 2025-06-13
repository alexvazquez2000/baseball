<?php
include 'config.php';
include 'templates/header.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $stmt = $pdo->prepare("UPDATE parents SET name=?, email=?, phone=? WHERE id=?");
    $stmt->execute([$_POST['name'], $_POST['email'], $_POST['phone'], $_POST['id']]);
}
$parent = $pdo->prepare("SELECT * FROM parents WHERE id=?");
$parent->execute([$_GET['id']]);
$data = $parent->fetch();
$players = $pdo->query("SELECT * FROM players")->fetchAll();
$linked = $pdo->prepare("SELECT players_id FROM players_parents WHERE parents_id=?");
$linked->execute([$_GET['id']]);
$linked_ids = array_column($linked->fetchAll(), 'players_id');

if (isset($_POST['link'])) {
    $pdo->prepare("DELETE FROM players_parents WHERE parents_id=?")->execute([$_GET['id']]);
    if (!empty($_POST['players'])) {
        foreach ($_POST['players'] as $pid) {
            $pdo->prepare("INSERT INTO players_parents (parents_id, players_id) VALUES (?, ?)")->execute([$_GET['id'], $pid]);
        }
    }
}
?>
<form method="post">
    <input type="hidden" name="id" value="<?= $data['id'] ?>">
    Name: <input type="text" name="name" value="<?= $data['name'] ?>"><br>
    Email: <input type="email" name="email" value="<?= $data['email'] ?>"><br>
    Phone: <input type="text" name="phone" value="<?= $data['phone'] ?>"><br>
    <input type="submit" value="Save">
</form>

<h3>Link Children</h3>
<form method="post">
    <?php foreach ($players as $p): ?>
        <input type="checkbox" name="players[]" value="<?= $p['id'] ?>" <?= in_array($p['id'], $linked_ids) ? 'checked' : '' ?>> <?= $p['name'] ?><br>
    <?php endforeach; ?>
    <input type="submit" name="link" value="Update Children">
</form>
<a href="list_parents.php">Back</a>

<?php include 'templates/footer.php'; ?>

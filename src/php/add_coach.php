<?php include 'config.php';
include 'templates/header.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $stmt = $pdo->prepare("INSERT INTO coaches (name, email, phone) VALUES (?, ?, ?)");
    $stmt->execute([$_POST['name'], $_POST['email'], $_POST['phone']]);
    header("Location: edit_teams.php");
}
?>
<form method="post">
    Name: <input type="text" name="name"><br>
    Email: <input type="email" name="email"><br>
    Phone: <input type="text" name="phone"><br>
    <input type="submit" value="Add Coach">
</form>

<?php include 'templates/footer.php'; ?>

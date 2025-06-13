<?php include 'config.php';
include 'templates/header.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $stmt = $pdo->prepare("INSERT INTO parents (name, email, phone) VALUES (?, ?, ?)");
    $stmt->execute([$_POST['name'], $_POST['email'], $_POST['phone']]);
    header("Location: list_parents.php");
}
?>
<form method="post">
    Name: <input type="text" name="name"><br>
    Email: <input type="email" name="email"><br>
    Phone: <input type="text" name="phone"><br>
    <input type="submit" value="Add Parent">
</form>

<?php include 'templates/footer.php'; ?>
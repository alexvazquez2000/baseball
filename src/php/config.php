<?php
include 'settings.php';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Could not connect to the database: " . $e->getMessage());
}

spl_autoload_register(function ($className) {
    $classFile = __DIR__ . '/app/' . $className . '.php';
    if (file_exists($classFile)) {
        require_once $classFile;
    }
});

echo "\n'{$_SERVER["SCRIPT_NAME"]}'";
switch ($_SERVER["SCRIPT_NAME"]) {
		case "/about.php":
			$CURRENT_PAGE = "About"; 
			$PAGE_TITLE = "About Us";
			break;
		case "/baseball/add_player.php":
			$CURRENT_PAGE = "Add Player";
			$PAGE_TITLE = "Add Player";
			if ($_SERVER["REQUEST_METHOD"] == "POST") {
				$stmt = $pdo->prepare("INSERT INTO players (name, date_of_birth, jersey_number) VALUES (?, ?, ?)");
				$stmt->execute([$_POST['name'], $_POST['date_of_birth'], $_POST['jersey_number']]);
				header("Location: list_players.php");
			}
			break;
		case "/baseball/list_players.php":
			$CURRENT_PAGE = "Players";
			$PAGE_TITLE = "Players";
			$stmt = $pdo->query("SELECT * FROM players");
			$players = $stmt->fetchAll(PDO::FETCH_CLASS, "Player");
			break;
		case "/baseball/edit_player.php":
			$CURRENT_PAGE = "Edit Player";
			$PAGE_TITLE = "Edit Player";
			if ($_SERVER["REQUEST_METHOD"] == "POST") {
				$stmt = $pdo->prepare("UPDATE players SET name=?, date_of_birth=?, jersey_number=? WHERE id=?");
				$stmt->execute([$_POST['name'], $_POST['date_of_birth'], $_POST['jersey_number'], $_POST['id']]);
				header("Location: list_players.php");
				exit();
			}
			$stmt = $pdo->prepare("SELECT * FROM players WHERE id=?");
			$stmt->setFetchMode(PDO::FETCH_CLASS, "Player");
			$stmt->execute([$_GET['id']]);
			$player = $stmt->fetch();
			break;
		default:
			$CURRENT_PAGE = "Index";
			$PAGE_TITLE = "Welcome to my homepage!";
	}


?>
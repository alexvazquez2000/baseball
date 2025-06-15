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

switch ($_SERVER["SCRIPT_NAME"]) {

		###################################################################
		#  Players
		###################################################################
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

		###################################################################
		#  Parents
		###################################################################
		case "/baseball/add_parent.php":
			$CURRENT_PAGE = "Add Parent";
			$PAGE_TITLE = "Add Parent";
			if ($_SERVER["REQUEST_METHOD"] == "POST") {
				$stmt = $pdo->prepare("INSERT INTO parents (name, email, phone) VALUES (?, ?, ?)");
				$stmt->execute([$_POST['name'], $_POST['email'], $_POST['phone']]);
				header("Location: list_parents.php");
			}
			break;
		case "/baseball/list_parents.php":
			$CURRENT_PAGE = "Parents";
			$PAGE_TITLE = "Parents";
			$stmt = $pdo->query("SELECT * FROM parents");
			$parents = $stmt->fetchAll(PDO::FETCH_CLASS, "PParent");
			break;
		case "/baseball/edit_parent.php":
			$CURRENT_PAGE = "Edit Parent";
			$PAGE_TITLE = "Edit Parent";
			if ($_SERVER["REQUEST_METHOD"] == "POST") {
				$stmt = $pdo->prepare("UPDATE parents SET name=?, email=?, phone=? WHERE id=?");
				$stmt->execute([$_POST['name'], $_POST['email'], $_POST['phone'], $_POST['id']]);
				header("Location: list_parents.php");
				exit();
			}
			$stmt = $pdo->prepare("SELECT * FROM parents WHERE id=?");
			$stmt->setFetchMode(PDO::FETCH_CLASS, "PParent");
			$stmt->execute([$_GET['id']]);
			$parent = $stmt->fetch();
			
			$stmt = $pdo->prepare("SELECT p.id, p.name, p.date_of_birth, p.jersey_number FROM players as p LEFT JOIN players_parents ON players_parents.players_id=p.id WHERE players_parents.parents_id=?");
			#$stmt->setFetchMode(PDO::FETCH_CLASS, "Player");
			$stmt->execute([$_GET['id']]);
			$players = $stmt->fetchAll(PDO::FETCH_CLASS, "Player");
			break;


		###################################################################
		#  Coaches
		###################################################################
		case "/baseball/add_coach.php":
			$CURRENT_PAGE = "Add Coach";
			$PAGE_TITLE = "Add Coach";
			if ($_SERVER["REQUEST_METHOD"] == "POST") {
				$stmt = $pdo->prepare("INSERT INTO coaches (name, email, phone) VALUES (?, ?, ?)");
				$stmt->execute([$_POST['name'], $_POST['email'], $_POST['phone']]);
				header("Location: list_coaches.php");
			}
			break;
		case "/baseball/list_coaches.php":
			$CURRENT_PAGE = "Coaches";
			$PAGE_TITLE = "Coaches";
			$stmt = $pdo->query("SELECT * FROM coaches");
			$coaches = $stmt->fetchAll(PDO::FETCH_CLASS, "Coach");
			break;
		case "/baseball/edit_coach.php":
			$CURRENT_PAGE = "Edit Coach";
			$PAGE_TITLE = "Edit Coach";
			if ($_SERVER["REQUEST_METHOD"] == "POST") {
				$stmt = $pdo->prepare("UPDATE coaches SET name=?, email=?, phone=? WHERE id=?");
				$stmt->execute([$_POST['name'], $_POST['email'], $_POST['phone'], $_POST['id']]);
				header("Location: list_coaches.php");
				exit();
			}
			$stmt = $pdo->prepare("SELECT * FROM coaches WHERE id=?");
			$stmt->setFetchMode(PDO::FETCH_CLASS, "Coach");
			$stmt->execute([$_GET['id']]);
			$coach = $stmt->fetch();
			#$stmt = $pdo->prepare("SELECT p.id, p.name, p.date_of_birth, p.jersey_number FROM players as p LEFT JOIN players_parents ON players_parents.players_id=p.id WHERE players_parents.parents_id=?");
			#$stmt->setFetchMode(PDO::FETCH_CLASS, "Player");
			#$stmt->execute([$_GET['id']]);
			#$teams = $stmt->fetchAll(PDO::FETCH_CLASS, "Team");
			break;

		###################################################################
		#  Parents
		###################################################################

		case "/baseball/list_teams.php":
			$CURRENT_PAGE = "Teams";
			$PAGE_TITLE = "Teams";
			$season = $_GET['season'] ?? "2025-Spring";
			$stmt = $pdo->prepare("SELECT * FROM teams WHERE season=?");
			$stmt->execute([$season]);
			$teams = $stmt->fetchAll(PDO::FETCH_CLASS, "Team");
			break;

			case "/baseball/index.php":
				break;

		default:
			$CURRENT_PAGE = "Index";
			$PAGE_TITLE = "Welcome to my homepage!";
			header("Location: index.php");
	}

	// Always ensure to close prepared statements and database connections when done.
	$stmt = null;
	// we closed the connection
	$pdo = null;

?>

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

    # ##################################################################
    # Players
    # ##################################################################
    case "/baseball/add_player.php":
        $CURRENT_PAGE = "Add Player";
        #Title is the H1 at top of the page
        $PAGE_TITLE = "Add Player";
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $stmt = $pdo->prepare("INSERT INTO players (name, date_of_birth, jersey_number) VALUES (?, ?, ?)");
            $stmt->execute([
                $_POST['name'],
                $_POST['date_of_birth'],
                $_POST['jersey_number']
            ]);
            header("Location: list_players.php");
        }
        break;
    case "/baseball/list_players.php":
        $CURRENT_PAGE = "Players";
        #Title is the H1 at top of the page
        $PAGE_TITLE = "Players";
        $stmt = $pdo->query("SELECT * FROM players");
        $players = $stmt->fetchAll(PDO::FETCH_CLASS, "Player");
        break;
    case "/baseball/edit_player.php":
        $CURRENT_PAGE = "Edit Player";
        #Title is the H1 at top of the page
        $PAGE_TITLE = "Edit Player";
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $stmt = $pdo->prepare("UPDATE players SET name=?, date_of_birth=?, jersey_number=? WHERE id=?");
            $stmt->execute([
                $_POST['name'],
                $_POST['date_of_birth'],
                $_POST['jersey_number'],
                $_POST['id']
            ]);
            header("Location: list_players.php");
            exit();
        }
        $stmt = $pdo->prepare("SELECT * FROM players WHERE id=?");
        $stmt->setFetchMode(PDO::FETCH_CLASS, "Player");
        $stmt->execute([
            $_GET['id']
        ]);
        $player = $stmt->fetch();
        break;

    # ##################################################################
    # Parents
    # ##################################################################
    case "/baseball/list_parents.php":
        $CURRENT_PAGE = "Parents";
        #Title is the H1 at top of the page
        $PAGE_TITLE = "Parents";
        $stmt = $pdo->query("SELECT * FROM parents");
        $parents = $stmt->fetchAll(PDO::FETCH_CLASS, "PParent");
        break;
    case "/baseball/edit_parent.php":
        $id = $_GET['id'] ?? '';
        $first_name = $last_name = $phone = $email = $photo = '';
        if ($id) {
            $CURRENT_PAGE = "Edit Parent";
            #Title is the H1 at top of the page
            $PAGE_TITLE = "Edit Parent";
            $stmt = $pdo->prepare("SELECT * FROM parents WHERE id=?");
            $stmt->setFetchMode(PDO::FETCH_CLASS, "PParent");
            $stmt->execute([  $id ]);
            $parent = $stmt->fetch();
            //also find the children/players
            $stmt = $pdo->prepare("SELECT p.id, p.name, p.date_of_birth, p.jersey_number FROM players as p LEFT JOIN players_parents ON players_parents.players_id=p.id WHERE players_parents.parents_id=?");
            # $stmt->setFetchMode(PDO::FETCH_CLASS, "Player");
            $stmt->execute([ $id ]);
            $players = $stmt->fetchAll(PDO::FETCH_CLASS, "Player");
        } else {
            $CURRENT_PAGE = "Add Parent";
            #Title is the H1 at top of the page
            $PAGE_TITLE = "Add Parent";
            $parent = new PParent();
            $parent->id = "";
        }
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $id = $_POST['id'];
            $name = $_POST['name'];
            $phone = $_POST['phone'];
            $email = $_POST['email'];
            if ($id) {
                $stmt = $pdo->prepare("UPDATE parents SET name=?, email=?, phone=? WHERE id=?");
                $stmt->execute([
                    $name,
                    $email,
                    $phone,
                    $id
                ]);
                header("Location: list_parents.php");
            } else {
                $stmt = $pdo->prepare("INSERT INTO parents (name, email, phone) VALUES (?, ?, ?)");
                $stmt->execute([
                    $name,
                    $email,
                    $phone
                ]);
                header("Location: list_parents.php");
            }
        }
        break;

    # ##################################################################
    # Coaches
    # ##################################################################
    case "/baseball/list_coaches.php":
        $CURRENT_PAGE = "Coaches";
        #Title is the H1 at top of the page
        $PAGE_TITLE = "Coaches";
        $stmt = $pdo->query("SELECT * FROM coaches");
        $coaches = $stmt->fetchAll(PDO::FETCH_CLASS, "Coach");
        break;
    case "/baseball/edit_coach.php":
        $id = $_GET['id'] ?? '';
        $first_name = $last_name = $phone = $email = $photo = '';
        if ($id) {
            $CURRENT_PAGE = "Edit Coach";
            #Title is the H1 at top of the page
            $PAGE_TITLE = "Edit Coach";
            $stmt = $pdo->prepare("SELECT * FROM coaches WHERE id=?");
            $stmt->setFetchMode(PDO::FETCH_CLASS, "Coach");
            $stmt->execute([ $id ]);
            $coach = $stmt->fetch();
        } else {
            $CURRENT_PAGE = "Add Coach";
            #Title is the H1 at top of the page
            $PAGE_TITLE = "Add Coach";
            $coach = new Coach();
            $coach->id = "";
        }
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $id = $_POST['id'];
            $name = $_POST['name'];
            $phone = $_POST['phone'];
            $email = $_POST['email'];
            $photo = $_POST['photo_filename'] ?? '';
            if ($id) {
                $stmt = $pdo->prepare("UPDATE coaches SET name=?, email=?, phone=?, photo=? WHERE id=?");
                $stmt->execute([
                    $name,
                    $email,
                    $phone,
                    $photo,
                    $id
                ]);
                header("Location: list_coaches.php");
            } else {
                $photo = $_POST['photo_filename'] ?? '';
                $stmt = $pdo->prepare("INSERT INTO coaches (name, email, phone, photo) VALUES (?, ?, ?, ?)");
                $stmt->execute([
                    $name,
                    $email,
                    $phone,
                    $photo
                ]);
                header("Location: list_coaches.php");
            }
        }
        # $stmt = $pdo->prepare("SELECT p.id, p.name, p.date_of_birth, p.jersey_number FROM players as p LEFT JOIN players_parents ON players_parents.players_id=p.id WHERE players_parents.parents_id=?");
        # $stmt->setFetchMode(PDO::FETCH_CLASS, "Player");
        # $stmt->execute([$_GET['id']]);
        # $teams = $stmt->fetchAll(PDO::FETCH_CLASS, "Team");
        break;
    case "/baseball/delete_coach.php":
        $CURRENT_PAGE = "Delete Coach";
        $PAGE_TITLE = "Delete Coach";
        if ($_SERVER["REQUEST_METHOD"] == "POST") {

            $id = $_GET['id'];
            $stmt = $conn->prepare("DELETE FROM coaches WHERE id=?");
            $stmt->bind_param('i', $id);
            $stmt->execute();
            // TODO: need to add a confirmation - add a message into the top of list_coaches
        }
        header("Location: list_coaches.php");
        break;

    # ##################################################################
    # Parents
    # ##################################################################

    case "/baseball/list_teams.php":
        $CURRENT_PAGE = "Teams";
        $PAGE_TITLE = "Teams";
        $season = $_GET['season'] ?? "2025-Spring";
        $stmt = $pdo->prepare("SELECT * FROM teams WHERE season=?");
        $stmt->execute([
            $season
        ]);
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

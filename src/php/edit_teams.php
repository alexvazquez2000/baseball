<?php
include 'config.php';
include 'templates/header.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $stmt = $pdo->prepare("INSERT INTO teams (name, logo, season) VALUES (?, ?, ?)");
    $stmt->execute([$_POST['name'], $_POST['logo'], $_POST['season']]);
    $team_id = $pdo->lastInsertId();

    foreach ($_POST['players'] as $pid) {
        $pdo->prepare("INSERT INTO team_players (team_id, player_id) VALUES (?, ?)")->execute([$team_id, $pid]);
    }
    foreach ($_POST['coaches'] as $cid) {
        $pdo->prepare("INSERT INTO team_coaches (team_id, coach_id) VALUES (?, ?)")->execute([$team_id, $cid]);
    }
    header("Location: list_teams.php");
}

$players = $pdo->query("SELECT id, name FROM players")->fetchAll();
$coaches = $pdo->query("SELECT id, name FROM coaches")->fetchAll();
?>

<h2>Create Team</h2>
<form method="post">
    Team Name: <input class="form-control" type="text" name="name"><br>
    Logo Filename: <input class="form-control" type="text" name="logo"><br>
    Season: <input class="form-control" type="text" name="season"><br>
    <h4>Select Players</h4>
    <?php foreach ($players as $p): ?>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" name="players[]" value="<?= $p['id'] ?>"> <?= $p['name'] ?>
        </div>
    <?php endforeach; ?>
    <h4>Select Coaches</h4>
    <?php foreach ($coaches as $c): ?>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" name="coaches[]" value="<?= $c['id'] ?>"> <?= $c['name'] ?>
        </div>
    <?php endforeach; ?>
    <input class="btn btn-primary mt-3" type="submit" value="Create Team">
</form>

<?php include 'templates/footer.php'; ?>

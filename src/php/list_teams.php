<?php
include 'config.php';
include 'templates/header.php';
?>

<h1>Teams for Season <?= htmlspecialchars($season) ?></h1>
<br>
<form method="get" class="mb-3">
    <label for="season">Season:</label>
    <input type="text" name="season" value="<?= htmlspecialchars($season) ?>">
    <input class="btn btn-secondary" type="submit" value="View">
</form>

<div class="row">
<?php foreach ($teams as $team): ?>
    <div class="col-md-6">
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title"><?= htmlspecialchars($team['name']) ?> (<?= $team['season'] ?>)</h5>
                <p class="card-text">Logo: <?= htmlspecialchars($team['logo']) ?></p>
                <h6>Players:</h6>
                <ul>
                <?php
                $ps = $pdo->prepare("SELECT p.name FROM players p JOIN team_players tp ON p.id = tp.player_id WHERE tp.team_id=?");
                $ps->execute([$team['id']]);
                foreach ($ps as $player) {
                    echo "<li>" . htmlspecialchars($player['name']) . "</li>";
                }
                ?>
                </ul>
                <h6>Coaches:</h6>
                <ul>
                <?php
                $cs = $pdo->prepare("SELECT c.name FROM coaches c JOIN team_coaches tc ON c.id = tc.coach_id WHERE tc.team_id=?");
                $cs->execute([$team['id']]);
                foreach ($cs as $coach) {
                    echo "<li>" . htmlspecialchars($coach['name']) . "</li>";
                }
                ?>
                </ul>
            </div>
        </div>
    </div>
<?php endforeach; ?>
</div>

<?php include 'templates/footer.php'; ?>

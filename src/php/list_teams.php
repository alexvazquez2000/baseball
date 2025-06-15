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
                <h5 class="card-title"><?= htmlspecialchars($team->teamName) ?> <?= $team->season ?></h5>
                <p class="card-text">Logo: <?= htmlspecialchars($team->logo) ?></p>
            </div>
        </div>
    </div>
<?php endforeach; ?>
</div>

<?php include 'templates/footer.php'; ?>

<?php


#if ($_SERVER["REQUEST_METHOD"] == "POST") {
#    $stmt = $pdo->prepare("UPDATE parents SET name=?, email=?, phone=? WHERE id=?");
#    $stmt->execute([$_POST['name'], $_POST['email'], $_POST['phone'], $_POST['id']]);
#}
#$parent = $pdo->prepare("SELECT * FROM parents WHERE id=?");
#$parent->execute([$_GET['id']]);
#$data = $parent->fetch();
#$players = $pdo->query("SELECT * FROM players")->fetchAll();
#$linked = $pdo->prepare("SELECT players_id FROM players_parents WHERE parents_id=?");
#$linked->execute([$_GET['id']]);
#$linked_ids = array_column($linked->fetchAll(), 'players_id');

#if (isset($_POST['link'])) {
#    $pdo->prepare("DELETE FROM players_parents WHERE parents_id=?")->execute([$_GET['id']]);
#    if (!empty($_POST['players'])) {
#        foreach ($_POST['players'] as $pid) {
#            $pdo->prepare("INSERT INTO players_parents (parents_id, players_id) VALUES (?, ?)")->execute([$_GET['id'], $pid]);
#        }
#    }
#}

<div class="mb-3">
    <label for="children" class="form-label">Children (Players)</label>
    <select name="children" class="form-select" multiple size="5">
      {% for player in parent.players %}
        <option value="{{ player.id }}" {% if player in parent.players %}selected{% endif %}>
          {{ player.name }}
        </option>
      {% endfor %}
    </select>
    <small class="form-text text-muted">Hold Ctrl (Cmd on Mac) to select multiple.</small>
  </div>
<h3>Link Children</h3>
<form method="post">
    <?php foreach ($players as $p): ?>
        <input type="checkbox" name="players[]" value="<?= $p['id'] ?>" <?= in_array($p['id'], $linked_ids) ? 'checked' : '' ?>> <?= $p['name'] ?><br>
    <?php endforeach; ?>
    <input type="submit" name="link" value="Update Children">

   include("config.php");
   session_start();
   $error='';
   if($_SERVER["REQUEST_METHOD"] == "POST") {
   
      // username and password sent from form 
      $myusername = mysqli_real_escape_string($db,$_POST['username']);
      $mypassword = mysqli_real_escape_string($db,$_POST['password']); 

      $sql = "SELECT * FROM admin WHERE username = '$myusername' and passcode = '$mypassword'";

      $result = mysqli_query($db,$sql);      
      $row = mysqli_num_rows($result);      
      $count = mysqli_num_rows($result);

      if($count == 1) {
	  
         // session_register("myusername");
         $_SESSION['login_user'] = $myusername;
         header("location: welcome.php");
      } else {
         $error = "Your Login Name or Password is invalid";
      }
   }
?>
<html>
<head>
   <title>Login Page</title>
   <style type = "text/css">
      body {
         font-family:Arial, Helvetica, sans-serif;
         font-size:14px;
      }
      label {
         font-weight:bold;
         width:100px;
         font-size:14px;
      }
      .box {
         border:#666666 solid 1px;
      }
   </style>
</head>
<body bgcolor = "#FFFFFF">
   <div align = "center">
      <div style = "width:300px; border: solid 1px #333333; " align = "left">
         <div style = "background-color:#333333; color:#FFFFFF; padding:3px;"><b>Login</b></div>
         <div style = "margin:30px">
            <form action = "" method = "post">
               <label>UserName  :</label><input type = "text" name = "username" class = "box"/><br /><br />
               <label>Password  :</label><input type = "password" name = "password" class = "box" /><br/><br />
               <input type = "submit" value = " Submit "/><br />
            </form>
            <div style = "font-size:11px; color:#cc0000; margin-top:10px"><?php echo $error; ?></div>
         </div>
      </div>
   </div>
</body>
</html>
<?php
   // Close the database connection
   mysqli_close($db);
?>


----
initial assumtions

create a php website for a baseball league for children. Use mysql/maria DB. Keep the database connection settings on a config file.
Create separate files for each class.
The children are the players, but don't call them children, call them players. Keep name, date of birth, and jersey number for each player.
Add a page to list all baseball players, with a link to a different page that allows to edit the player's info. 
Add a page to list the parents of the players. Add a link on each parent to allow to edit the parent contact info. Keep name, email and phone for each parent.
On the page to edit the parents, allow to add children.
Add a page that allows creating teams. A team has a name, a logo,the season, one or many coaches, one or many players . We have many teams each season.  The logo is a filename.  Add a link to upload a png or gif file for the logo.
Add a page to show/edit the list of coaches. Keep name, email and phone for each coach.
Add a welcome page with a list of the teams in the current season. On the welcome page add a buttons to show the parents or edit the teams.
A parent can have multiple children, and a child can have multiple parents.
A player can be on multiple teams.
Create pages for add a player, a parent, and coach. 
Create the html template files needed to support the app.



XAMPP installation 
https://www.tutorialspoint.com/php/php_installation.htm

https://127.0.0.1/baseball/

//CSS came from template "Nature Portfolio Template" on https://www.w3schools.com/w3css/w3css_templates.asp
https://www.w3schools.com/w3css/tryw3css_templates_portfolio.htm
https://www.w3schools.com/w3css/tryit.asp?filename=tryw3css_templates_portfolio&stacked=h


https://www.php.net/manual/en/mysql.configuration.php#ini.mysql.default-user
Modify the php.ini with DB credentials


The most secure way is to not have the information specified in your PHP code at all.

If you're using Apache that means to set the connection details in your httpd.conf or virtual hosts file file. If you do that you can call mysql_connect() with no parameters, which means PHP will never ever output your information.

This is how you specify these values in those files:

php_value mysql.default.user      myusername
php_value mysql.default.password  mypassword
php_value mysql.default.host      server

Then you open your mysql connection like this:

<?php
$db = mysqli_connect();

Or like this:

<?php
$db = mysqli_connect(ini_get("mysql.default.user"),
                     ini_get("mysql.default.password"),
                     ini_get("mysql.default.host"));


Unit tests on php 
https://psalm.dev
https://codeception.com testing php

https://fpdf.org  - PDF for php
 

 
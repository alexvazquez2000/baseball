# baseball

#To Install dependencies

	pip install -r requirements.txt


create a python website using flask for a baseball league for children.
Use mysql/maria DB. Keep the database connection settings on a config file.
Create separate files for each class.
The children are the players, but don't call them children, call them players. Keep name, date of birth, and jersey number for each player.
Add a page to list all baseball players, with a link to a different page that allows to edit the player's info. 
Add a page to list the parents of the players. Add a link on each parent to allow to edit the parent contact info. Keep name, email and phone for each parent.
On the page to edit the parents, allow to add children.
Add a page that allows creating teams. A team has a name, the season, one or many coaches, one or many players . We have many teams each season.
Add a page to show/edit the list of coaches. Keep name, email and phone for each coach.
Add a welcome page with a list of the teams in the current season. On the welcome page add a buttons to show the parents or edit the teams.
A parent can have multiple children, and a child can have multiple parents.
A player can be on multiple teams.
Create pages for add a player, a parent, and coach. 
Create the html template files needed to support the app.
Create the app.py file.

Help you with a small shell script to wait for MySQL to be ready before launching Flask.

generate the full app code including models, routes, and templates in this Docker setup


#How to run

    Clone or copy files in a directory.

    Run: docker-compose up --build

    Wait for MySQL to initialize and Flask to start.

    Visit http://localhost:5000/

#Create tables and run app

If you don’t have tables yet, you can run:

	with app.app_context():
    db.create_all()

Add it temporarily in your app.py after defining your models or run from a separate script.


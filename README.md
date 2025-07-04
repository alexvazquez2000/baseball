# baseball

#To Install dependencies

	pip install -r requirements.txt

# create venv environment

	python -m venv venv
	#on windows use:
	venv\Scripts\activate
	#or on linux/Mac use:
	. venv/Scripts/activate
	pip list  #that showed an almost empty list
	#install the requirements
	pip install -r requirements.txt
	pip freeze > requirements.txt
	#now list shows about 20 packages
	pip list


# Run locally with python

	python app.py

# Run locally with gunicorn - but not on windows

	gunicorn app:app
	# Note that this gives an error: ModuleNotFoundError: No module named 'fcntl'
	# because gunicorn can not run on Windows. Could try using portalocker or waitress on Windows, instead of gunicorn



# Initial requirements
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
Create pages to add a player, a parent, and coach. 
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

#To Run Unit tests


Run all tests:

	python run_tests.py

Run tests from a specific module:

	python run_tests.py test_app
	python run_tests.py test_forms
	python run_tests.py test_config

Or using the standard unittest discovery:

    python -m unittest discover -v

The script provides a convenient way to run all your tests with detailed output and proper exit codes for CI/CD integration if needed later.


#Tests:

- Main test suite covering:

    Authentication and session management
    All routes and endpoints
    AJAX functionality
    PDF generation
    Error handling

- Focused model tests covering:

    Model creation and relationships
    Many-to-many relationships between players/parents and teams
    Complex relationship scenarios

    - Test runner script for easy execution

Key Features:

    In-memory SQLite database for fast, isolated testing
    Mock authentication to test protected routes
    Comprehensive coverage of models, routes, and relationships
    AJAX endpoint testing with JSON responses
    Error handling tests for edge cases
    Relationship testing for complex many-to-many associations

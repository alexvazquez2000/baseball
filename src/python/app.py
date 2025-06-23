from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from datetime import datetime
from config import Config
from models import db, Players, Parents, Coaches, Teams
import os
from werkzeug.utils import secure_filename

#for PDF
#from flask import make_response
from fpdf import FPDF

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)

##To create DB
#with app.app_context():
#    db.create_all()

# -- Welcome page: show teams in current season (e.g. "2025") --
@app.route('/')
def welcome():
    current_season = "2025-Spring"  # or dynamic if you want
    teams = Teams.query.filter_by(season=current_season).all()
    return render_template('welcome.html', teams=teams)

# -- Players --

@app.route('/players')
def list_players():
    players = Players.query.all()
    return render_template('players.html', players=players)

@app.route('/player/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        dob = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
        player = Players(
            name=request.form['name'],
            last_name=request.form['last_name'],
            date_of_birth=dob,
            jersey_number=int(request.form['jersey_number'])
        )
        db.session.add(player)
        db.session.commit()
        return redirect(url_for('list_players'))
    return render_template('add_player.html')

@app.route('/player/<int:player_id>/edit', methods=['GET', 'POST'])
def edit_player(player_id):
    player = Players.query.get_or_404(player_id)
    if request.method == 'POST':
        player.name = request.form['name']
        player.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
        player.jersey_number = int(request.form['jersey_number'])
        db.session.commit()
        return redirect(url_for('list_players'))
    return render_template('edit_player.html', player=player)

# -- Parents --

@app.route('/parents')
def list_parents():
    parents = Parents.query.all()
    return render_template('parents.html', parents=parents)

@app.route('/parent/add', methods=['GET', 'POST'])
def add_parent():
    if request.method == 'POST':
        parent = Parents(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone']
        )
        db.session.add(parent)
        db.session.commit()
        return redirect(url_for('list_parents'))
    return render_template('add_parent.html')

@app.route('/parent/<int:parent_id>/edit', methods=['GET', 'POST'])
def edit_parent(parent_id):
    parent = Parents.query.get_or_404(parent_id)
    players = Players.query.all()
    if request.method == 'POST':
        parent.name = request.form['name']
        parent.email = request.form['email']
        parent.phone = request.form['phone']
        # Clear current children
        parent.players.clear()
        # Add selected children
        child_ids = request.form.getlist('children')
        for cid in child_ids:
            player = Players.query.get(int(cid))
            if player:
                parent.players.append(player)
        db.session.commit()
        return redirect(url_for('list_parents'))
    return render_template('edit_parent.html', parent=parent, players=players)

# -- Coaches --

@app.route('/coaches')
def list_coaches():
    coaches = Coaches.query.all()
    return render_template('coaches.html', coaches=coaches)

@app.route('/coach/add', methods=['GET', 'POST'])
def add_coach():
    if request.method == 'POST':
        coach = Coaches(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone']
        )
        db.session.add(coach)
        db.session.commit()
        return redirect(url_for('list_coaches'))
    return render_template('add_coach.html')

@app.route('/coach/<int:coach_id>/edit', methods=['GET', 'POST'])
def edit_coach(coach_id):
    coach = Coaches.query.get_or_404(coach_id)
    if request.method == 'POST':
        coach.name = request.form['name']
        coach.email = request.form['email']
        coach.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('list_coaches'))
    return render_template('edit_coach.html', coach=coach)

# -- Teams --

@app.route('/teams')
def list_teams():
    teams = Teams.query.all()
    return render_template('teams.html', teams=teams)

@app.route('/team/add', methods=['GET', 'POST'])
def add_team():
    coaches = Coaches.query.all()
    players = Players.query.all()
    if request.method == 'POST':
        team = Team(
            teamName=request.form['teamName'],
            season=request.form['season'],
        )
        # Add coaches
        coach_ids = request.form.getlist('coaches')
        for cid in coach_ids:
            coach = Coaches.query.get(int(cid))
            if coach:
                team.coaches.append(coach)
        # Add players
        player_ids = request.form.getlist('players')
        for pid in player_ids:
            player = Players.query.get(int(pid))
            if player:
                team.players.append(player)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for('list_teams'))
    return render_template('add_team.html', coaches=coaches, players=players)

@app.route('/team/<int:team_id>/edit', methods=['GET', 'POST'])
def edit_team(team_id):
    team = Teams.query.get_or_404(team_id)
    coaches = Coaches.query.all()
    players = Players.query.all()
    if request.method == 'POST':
        team.teamName = request.form['teamName']
        team.season = request.form['season']
        # Update coaches
        team.coaches.clear()
        coach_ids = request.form.getlist('coaches')
        for cid in coach_ids:
            coach = Coaches.query.get(int(cid))
            if coach:
                team.coaches.append(coach)
        # Update players
        team.players.clear()
        player_ids = request.form.getlist('players')
        for pid in player_ids:
            player = Players.query.get(int(pid))
            if player:
                team.players.append(player)
        db.session.commit()
        return redirect(url_for('list_teams'))
    return render_template('edit_team.html', team=team, coaches=coaches, players=players)

# -- Experimental section
@app.route('/generate-pdf')
def generate_pdf():
	# https://py-pdf.github.io/fpdf2/Tutorial.html#tuto-1-minimal-example
    #Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    # Add content to the PDF
    pdf.cell(text="Hello from Flask and fpdf2!")
    pdf.ln(10) # Line break
    pdf.cell(text="This is a dynamically generated PDF.")
    # PDF is ready
    # for usage on flask https://py-pdf.github.io/fpdf2/UsageInWebAPI.html
    # Create a Flask response and Output the PDF as bytes
    response = make_response(bytes(pdf.output()))
    # Set appropriate headers for PDF
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=generated_document.pdf" 
    return response

# -- Extra navigation links on welcome page --

@app.route('/parents_page')
def parents_page():
    return redirect(url_for('list_parents'))

@app.route('/teams_page')
def teams_page():
    return redirect(url_for('list_teams'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    app.run()

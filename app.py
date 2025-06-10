from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from config import Config
from models import db, Player, Parent, Coach, Team

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# -- Welcome page: show teams in current season (e.g. "2025") --
@app.route('/')
def welcome():
    current_season = "2025"  # or dynamic if you want
    teams = Team.query.filter_by(season=current_season).all()
    return render_template('welcome.html', teams=teams)

# -- Players --

@app.route('/players')
def list_players():
    players = Player.query.all()
    return render_template('players.html', players=players)

@app.route('/player/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        dob = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
        player = Player(
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
    player = Player.query.get_or_404(player_id)
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
    parents = Parent.query.all()
    return render_template('parents.html', parents=parents)

@app.route('/parent/add', methods=['GET', 'POST'])
def add_parent():
    if request.method == 'POST':
        parent = Parent(
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
    parent = Parent.query.get_or_404(parent_id)
    players = Player.query.all()
    if request.method == 'POST':
        parent.name = request.form['name']
        parent.email = request.form['email']
        parent.phone = request.form['phone']
        # Clear current children
        parent.players.clear()
        # Add selected children
        child_ids = request.form.getlist('children')
        for cid in child_ids:
            player = Player.query.get(int(cid))
            if player:
                parent.players.append(player)
        db.session.commit()
        return redirect(url_for('list_parents'))
    return render_template('edit_parent.html', parent=parent, players=players)

# -- Coaches --

@app.route('/coaches')
def list_coaches():
    coaches = Coach.query.all()
    return render_template('coaches.html', coaches=coaches)

@app.route('/coach/add', methods=['GET', 'POST'])
def add_coach():
    if request.method == 'POST':
        coach = Coach(
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
    coach = Coach.query.get_or_404(coach_id)
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
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)

@app.route('/team/add', methods=['GET', 'POST'])
def add_team():
    coaches = Coach.query.all()
    players = Player.query.all()
    if request.method == 'POST':
        team = Team(
            teamName=request.form['teamName'],
            season=request.form['season'],
        )
        # Add coaches
        coach_ids = request.form.getlist('coaches')
        for cid in coach_ids:
            coach = Coach.query.get(int(cid))
            if coach:
                team.coaches.append(coach)
        # Add players
        player_ids = request.form.getlist('players')
        for pid in player_ids:
            player = Player.query.get(int(pid))
            if player:
                team.players.append(player)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for('list_teams'))
    return render_template('add_team.html', coaches=coaches, players=players)

@app.route('/team/<int:team_id>/edit', methods=['GET', 'POST'])
def edit_team(team_id):
    team = Team.query.get_or_404(team_id)
    coaches = Coach.query.all()
    players = Player.query.all()
    if request.method == 'POST':
        team.teamName = request.form['teamName']
        team.season = request.form['season']
        # Update coaches
        team.coaches.clear()
        coach_ids = request.form.getlist('coaches')
        for cid in coach_ids:
            coach = Coach.query.get(int(cid))
            if coach:
                team.coaches.append(coach)
        # Update players
        team.players.clear()
        player_ids = request.form.getlist('players')
        for pid in player_ids:
            player = Player.query.get(int(pid))
            if player:
                team.players.append(player)
        db.session.commit()
        return redirect(url_for('list_teams'))
    return render_template('edit_team.html', team=team, coaches=coaches, players=players)

# -- Extra navigation links on welcome page --

@app.route('/parents_page')
def parents_page():
    return redirect(url_for('list_parents'))

@app.route('/teams_page')
def teams_page():
    return redirect(url_for('list_teams'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

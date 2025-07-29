from flask import Blueprint, render_template, request, Response, redirect, url_for, session
from datetime import datetime

from sqlalchemy import func

from play_ball.models import db, Players, Teams, teams_players
from play_ball.extension import get_current_season
from play_ball.auth.auth_bp import login_required

players_bp = Blueprint('players', __name__, template_folder='templates')

# -- Players --
@players_bp.route('/')
@login_required
def list_players():
    #now = datetime.now()
    #formatted_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    #print(f"start {formatted_time}")

    players = Players.query.all()

    #now = datetime.now()
    #formatted_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    #print(f"got player {formatted_time}")

    (current_season_id, current_season_name) = get_current_season()

    #now = datetime.now()
    #formatted_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    #print(f"got season {formatted_time}")
    
    #players = db.session.query(Players, teams_players, func.count(teams_players.teams_id))
    #players = db.session.query(Players, teams_players).outerjoin(Players.id==teams_players.players_id ).all
    #.outerjoin(Teams, Teams.id==teams_players.teams_id).filter(Teams.season_id==current_season_id).all()
    #return render_template('players.html', players=players)
    rh = render_template('players.html', players=players)
    
    #now = datetime.now()
    #formatted_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    #print(f"render {formatted_time}")
    
    return rh
@players_bp.route('/player', methods=['GET', 'POST'])
@login_required
def edit_player():
    player = {}
    player_id = request.args.get('player_id')
    if request.method == 'POST':
        #get the ID from the post data if present
        player_id = request.form['id'] 
        if player_id:
            #update existing entry
            player = Players.query.get_or_404(player_id)
            player.first_name = request.form['first_name']
            player.last_name = request.form['last_name']
            player.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            player.jersey_number = int(request.form['jersey_number'])
        else :
            #add new player / player_id is empty
            dob = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            player = Players(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                date_of_birth=dob,
                jersey_number=int(request.form['jersey_number'])
            )
            db.session.add(player)
        db.session.commit()
        #TODO: stay on page to continue editing or redirect to list all players?
        #return redirect(url_for('players.list_players'))

    dob = ''
    if player_id :
        player = Players.query.get_or_404(player_id)
        dob = player.date_of_birth.strftime('%Y-%m-%d')
    return render_template('edit_player.html', player=player, dob=dob)


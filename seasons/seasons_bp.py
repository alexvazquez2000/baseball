from flask import Blueprint, render_template, request, make_response, redirect, url_for, session
from datetime import datetime

#re for regular expression
import re

from decimal import Decimal

from extension import get_current_season
from base_calendar import BaseCalendar

from models import db, Players, Coaches, Teams, Seasons, Levels


seasons_bp = Blueprint('seasons', __name__, template_folder='templates')

# -- Seasons and teams --

@seasons_bp.route('/change_season', methods=['GET', 'POST'])
#@login_required
def change_season():  
    if request.method == 'POST':
        selected_season = request.form['selected_season']
        current_season = Seasons.query.get_or_404(int(selected_season))
        print (f"new season is {current_season.season_name}")
        session['current_season_id'] = current_season.id
        session['current_season_name'] = current_season.season_name
        #return redirect(url_for('seasons.list_teams'))
        response = make_response(redirect(url_for('seasons.list_teams')))
        #add a cookie for 30 days
        #response.set_cookie('current_season_id', current_season_id, max_age=timedelta(days=30).total_seconds())
        #response.set_cookie('current_season_name', current_season_name, max_age=timedelta(days=30).total_seconds())
        return response
    seasons = Seasons.query.all()
    return render_template('change_season.html', seasons=seasons)

@seasons_bp.route('/season/<int:season_id>/edit', methods=['GET', 'POST'])
#@login_required
def edit_season(season_id):
    season = Seasons.query.get_or_404(season_id)
    if request.method == 'POST':
        season.name = request.form['name']
        season.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        season.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        db.session.commit()
        return redirect(url_for('seasons.list_teams'))
    return render_template('edit_season.html', season=season)

# -- Create new season --
@seasons_bp.route('/create_new_season', methods=['GET', 'POST'])
#@login_required
def create_new_season():
    (current_season_id, current_season_name) = get_current_season()
    if request.method == 'POST':
        # Get the current season
        current_season = Seasons.query.order_by(Seasons.id.desc()).first()
        if current_season:
            # Create a new season based on the current one
            newSeason = Seasons(
                season_name=request.form['season_name'],
                base_date = datetime.strptime(request.form['base_date'], '%Y-%m-%d').date()
            )
            db.session.add(newSeason)
            # Commit to get the parent's ID if needed immediately, but parent object needs to be commited before teams can be created
            db.session.commit()

            #set session to new session
            session['current_season_id'] = newSeason.id
            session['current_season_name'] = newSeason.season_name

            #now add the teams
            copyteams = request.form.getlist('copyteams')
            for copy_team_id in copyteams :
                print (f" copy team {copy_team_id } {copy_team_name } to new season")
                old_team = Teams.query.get(int(copy_team_id))
                if old_team:
                    new_team = Teams(
                       season = newSeason,
                       team_name = old_team.team_name,
                       level = old_team.level,
                       coaches = old_team.coaches
                       #TODO: Could copy players here but planning to also do the billing
                    )
                    newSeason.teams.append(new_team)
                # else :
                #     #TODO: Add a warning that we missed one of the teams
            db.session.add(newSeason)
            db.session.commit()
            return redirect(url_for('seasons.list_teams'))
    current_season = Seasons.query.get_or_404(current_season_id)
    return render_template('create_new_season.html', current_season=current_season)

# -- Teams --
@seasons_bp.route('/teams')
#@login_required
def list_teams():
    (current_season_id, current_season_name) = get_current_season()
    teams = Teams.query.filter_by(season_id=current_season_id).all()
    return render_template('teams.html', teams=teams)

@seasons_bp.route('/team', methods=['GET', 'POST'])
#@login_required
def edit_team():
    team = {}
    team_id = request.args.get('team_id')
    (current_season_id, current_season_name) = get_current_season()
    if request.method == 'POST':
        #get the ID from the post data if present
        team_id = request.form['id']
        level_id = request.form['level_id']
        level = Levels.query.get(int(level_id))
        if team_id:
            #update existing entry
            team = Teams.query.get_or_404(team_id)
            team.team_name = request.form['team_name']
            #team.season is read-only on the page
            team.level= level
            db.session.commit()
            #on update then we are done
            return redirect(url_for('seasons.list_teams'))
        else :
            team = Teams(
                team_name = request.form['team_name'],
                season_id = current_season_id,
                level = level
            ) 
            db.session.add(team)
            db.session.commit()
            #it is a new team, continue editing to add coaches and players
    if team_id:
        team = Teams.query.get_or_404(team_id)
        current_season_id = team.season.id
        current_season_name = team.season.season_name
        for player in team.players:
            base_date = team.season.base_date.strftime('%Y-%m-%d')
            player_dob = player.date_of_birth.strftime('%Y-%m-%d')
            player.baseball_age = BaseCalendar.baseball_age(player_dob, base_date)
    levels = Levels.query.all()
    return render_template('edit_team.html', team=team, levels=levels,
      current_season_id=current_season_id, current_season_name=current_season_name )

# -- Fees --
@seasons_bp.route('/levels_fees')
#@login_required
def levels_fees():
    levels = Levels.query.all()
    return render_template('levels_fees.html', levels=levels)

def clean_money(input_string):
	""" Remove any non-char except digits and periods - negative numbers are not allowed """
	return re.sub(r'[^0-9.]','',input_string)

@seasons_bp.route('/level', methods=['GET', 'POST'])
#@login_required
def edit_level():
    level = {}
    level_id = request.args.get('level_id')
    if request.method == 'POST':
        #get the ID from the post data if present
        level_id = request.form['id'] 
        if level_id:
            #update existing entry
            level = Levels.query.get_or_404(level_id)
            level.level_name = request.form['level_name']
            level.target_age = int(request.form['target_age'])
            level.registration = Decimal(clean_money(request.form['registration']) )
            level.team_fee = Decimal(clean_money(request.form['team_fee']) )
            level.uniform = Decimal(clean_money(request.form['uniform']) )

        else :
            #add new level because level_id is empty
            level = Levels(
                level_name=request.form['level_name'],
                target_age=int(request.form['target_age']),
                registration=Decimal(request.form['registration']),
                team_fee=Decimal(request.form['team_fee']),
                uniform=Decimal(request.form['uniform'])
            )
            db.session.add(level)
        db.session.commit()
        return redirect(url_for('seasons.levels_fees'))

    if level_id :
        level = Levels.query.get_or_404(level_id)
    return render_template('edit_level.html', level=level)


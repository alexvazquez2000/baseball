from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from models import db, Players, Parents, Coaches, Teams

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def index():
    return {"message": "Welcome to the Baseball API"}, 200

@api_bp.route('/status', methods=['GET'])
def status():
    return {"status": "API is running"}, 200

#Ajax
@api_bp.route("/player/search")
def search_players():
    """Search players by name, returns JSON."""
    q = request.args.get("q", "")
    results = []
    if q:
        results = Players.query.filter(
          or_(
            Players.first_name.ilike(f"%{q}%"),
            Players.last_name.ilike(f"%{q}%")
          )
        ).all()
    data = [{"id": p.id, "first_name": p.first_name, "last_name": p.last_name, "jersey_number": p.jersey_number} for p in results]
    return jsonify(data)

#Ajax
@api_bp.route("/parents/search")
def search_parents():
    """Search parents by name, returns JSON."""
    q = request.args.get("q", "")
    results = []
    if q:
        results = Parents.query.filter(
          or_(
            Parents.first_name.ilike(f"%{q}%"),
            Parents.last_name.ilike(f"%{q}%")
          )
        ).all()
    data = [{"id": p.id, "first_name": p.first_name, "last_name": p.last_name, "email": p.email, "phone": p.phone} for p in results]
    return jsonify(data)

#Ajax
@api_bp.route("/coaches/search")
def search_coaches():
    """Search coaches by name, returns JSON."""
    q = request.args.get("q", "")
    results = []
    if q:
        results = Coaches.query.filter(
          or_(
            Coaches.first_name.ilike(f"%{q}%"),
            Coaches.last_name.ilike(f"%{q}%")
          )
        ).all()
    data = [{"id": p.id, "first_name": p.first_name, "last_name": p.last_name, "email": p.email, "phone": p.phone} for p in results]
    return jsonify(data)


#Ajax
@api_bp.route("/player/<int:player_id>/add_parent_to_player", methods=["POST"])
def add_parent_to_player(player_id):
    """ Add parent to a player """
    parent_id = request.json.get("parent_id")
    player = Players.query.get(player_id)
    parent = Parents.query.get(parent_id)

    if parent and player and parent not in player.parents:
        player.parents.append(parent)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@api_bp.route("/parent/<int:parent_id>/add_player_to_parent", methods=["POST"])
def add_player_to_parent(parent_id):
    """ Add player to a parent """
    player_id = request.json.get("player_id")
    player = Players.query.get(player_id)
    parent = Parents.query.get(parent_id)

    if parent and player and player not in parent.players:
        parent.players.append(player)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

#Ajax
@api_bp.route("/player/<int:player_id>/remove_parent/<int:parent_id>", methods=["DELETE"])
def remove_parent_ajax(player_id, parent_id):
    #print(f"Deleting child-parent player={player_id} / parent={parent_id}" )
    player = Players.query.get(player_id)
    parent = Parents.query.get(parent_id)
    if parent and player and parent in player.parents:
        player.parents.remove(parent)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@api_bp.route("/team/<int:team_id>/add_coach_to_team", methods=["POST"])
def add_coach_to_team(team_id):
    """ Add coach to a team """
    coach_id = request.json.get("coach_id")
    coach = Coaches.query.get(coach_id)
    team = Teams.query.get(team_id)

    if team and coach and coach not in team.coaches:
        team.coaches.append(coach)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@api_bp.route("/team/<int:team_id>/remove_coach/<int:coach_id>", methods=["DELETE"])
def remove_coach(team_id, coach_id):
    """ remove coach from team """
    coach = Coaches.query.get(coach_id)
    team = Teams.query.get(team_id)
    if coach and team and coach in team.coaches:
        team.coaches.remove(coach)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400



#Nothing is needed below this point
@api_bp.route('/data', methods=['GET'])
def get_data():
    sample_data = {
        "teams": ["Yankees", "Red Sox", "Dodgers"],
        "players": ["Player1", "Player2", "Player3"]
    }
    return sample_data, 200

@api_bp.route('/data', methods=['POST'])
def post_data():
    return {"message": "Data received"}, 201

@api_bp.route('/error', methods=['GET'])
def error():
    return {"error": "This is a sample error message"}, 400 

@api_bp.route('/health', methods=['GET'])
def health():  
    return {"health": "OK"}, 200

@api_bp.route('/info', methods=['GET'])
def info():
    return {"info": "This is a sample API for baseball data"}, 200  

@api_bp.route('/version', methods=['GET'])
def version():
    return {"version": "1.0.0"}, 200

from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from datetime import datetime
from decimal import Decimal

from play_ball.models import db, Players, Parents, Coaches, Teams, Users
from play_ball.models import Account, Journal, Transaction, Entry

api_bp = Blueprint('api', __name__)

@api_bp.after_request
def add_cors_headers(response):
    #add CORS headers
    response.headers.add('Access-Control-Allow-Origin', '*') # Or specify allowed origins
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


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
        results = Users.query.filter(Users.parent_id.isnot(None)).filter(
          or_(
            Users.first_name.ilike(f"%{q}%"),
            Users.last_name.ilike(f"%{q}%")
          )
        ).all()
    data = [{"id": p.id, "parent_id": p.parent.id , "first_name": p.first_name, "last_name": p.last_name, "email": p.email, "phone": p.phone} for p in results]
    return jsonify(data)

#Ajax
@api_bp.route("/coaches/search")
def search_coaches():
    """Search coaches by name, returns JSON."""
    q = request.args.get("q", "")
    results = []
    if q:
        results = Users.query.filter(Users.coach_id.isnot(None)).filter(
          or_(
            Users.first_name.ilike(f"%{q}%"),
            Users.last_name.ilike(f"%{q}%")
          )
        ).all()
    data = [{"id": p.id, "coach_id": p.coach.id , "first_name": p.first_name, "last_name": p.last_name, "email": p.email, "phone": p.phone} for p in results]
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

@api_bp.route("/team/<int:team_id>/add_players", methods=["POST"])
def add_players_to_team(team_id):
    """ Add multiple players to a team """
    team = Teams.query.get(team_id)
    #print(f"Adding to {team.id} {team.team_name}")
    # Get the JSON data from the request body
    # get_json() will return a Python list if the JSON root is an array
    received_data = request.get_json()
    response_dict = {}
    # Check if the received data is indeed a list (representing the JSON array)
    if isinstance(received_data, list):
        print(f"Received JSON array: {received_data}")
        sales_journal = Journal.find_by_name("Sales Journal")
        ar_account=Account.find_by_name("Accounts Receivable")
        sr_account=Account.find_by_name("Service Revenue")
        #print(f"ar = {ar_account.name} sr={sr_account.name} journal={sales_journal.name}")
        
        # Process the array elements
        for item in received_data:
            #print(f"Item: {item} to {team.id} {team.team_name}")
            player_id = item.get('playerid')
            player_name = item.get('player_name')
            reg_fee = Decimal(item.get('reg_fee'))
            team_fee = Decimal(item.get('team_fee'))
            uniform = Decimal(item.get('uniform'))
            player = Players.query.get_or_404(player_id)
            parent = player.parents[0]
            if not parent or not parent.user:
                player_status = f"playerid {player_id} {player_name} doesn't have a parent with a valid user"
            elif player:
                if player in team.players:
                    player_status = f"playerid {player_id} {player_name} was already on {team.id} {team.team_name}" 
                else:
                    memo = f"Add player {player_name} to {team.team_name} season {team.season.season_name}",
                    txn = Transaction(
                        user_id=parent.user.id,
                        description=memo,
                        transaction_date=datetime.now().date(),
                        journal_id=2) #sales_journal.id)
                    db.session.add(txn)
                    db.session.flush()
                    if reg_fee > 0.00:
                        db.session.add(
                            Entry(transaction_id=txn.id, account_id=ar_account.id,
                                amount=reg_fee, entry_type='debit', memo=f"Registration - {memo}"))
                        db.session.add(
                            Entry(transaction_id=txn.id, account_id=sr_account.id,
                                amount=reg_fee, entry_type='credit', memo=f"Registration - {memo}"))
                    if team_fee > 0.00:
                        db.session.add(
                            Entry(transaction_id=txn.id, account_id=ar_account.id,
                                amount=team_fee, entry_type='debit', memo=f"Team fee - {memo}"))
                        db.session.add(
                            Entry(transaction_id=txn.id, account_id=sr_account.id,
                                amount=team_fee, entry_type='credit', memo=f"Team fee - {memo}"))
                    if uniform > 0.00:
                        db.session.add(
                            Entry(transaction_id=txn.id, account_id=ar_account.id,
                                amount=team_fee, entry_type='debit', memo=f"uniform - {memo}"))
                        db.session.add(
                            Entry(transaction_id=txn.id, account_id=sr_account.id,
                                amount=team_fee, entry_type='credit', memo=f"uniform - {memo}"))
                    #finally add user to the team
                    team.players.append(player)
                    db.session.commit()
                    player_status = f"Successfully added player {player_name} to {team.team_name} season {team.season.season_name}"
            else:
                player_status = f"playerid {player_id} {player_name} not found"
            #add status to response
            print(player_status)
            response_dict[f"player_id_{player_id}"] = player_status
            #end for loop
        db.session.commit()
        return jsonify({
            "message": "Array received successfully",
            "received_data": received_data,
            "response_data": response_dict
            }), 200
    else:
        print ("Recived bad data while adding players to team - Expected a JSON array")
        return jsonify({"error": "Expected a JSON array"}), 400


@api_bp.route('/parents_OUT', methods=['GET'])
def get_parents_out():
    results = Users.query.filter(Users.parent_id.isnot(None)).all()
    data = [{
        "id": p.id,
        "parent_id": p.parent.id,
        "first_name": p.first_name,
        "last_name": p.last_name,
        "email": p.email,
        "phone": p.phone
        } for p in results]
    return jsonify(data), 200

@api.route('/parents', methods=['GET'])
def get_parents():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Paginate the query
    pagination = db.session.execute(
        db.select(Users).order_by(Users.parent_id)
    ).paginate(page=page, per_page=per_page, error_out=False)

    results = pagination.items
    
    # Prepare the response data
    results = [{
        "id": p.id,
        "parent_id": p.parent.id,
        "first_name": p.first_name,
        "last_name": p.last_name,
        "email": p.email,
        "phone": p.phone
        } for p in results
        ]

    return jsonify({
        'items': results,
        'total_parents': pagination.total,
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })


#--------------------------------------------------------------------------------------------------
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

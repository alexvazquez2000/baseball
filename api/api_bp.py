from flask import Blueprint

api_bp = Blueprint('api', __name__)
@api_bp.route('/', methods=['GET'])
def index():
    return {"message": "Welcome to the Baseball API"}, 200

@api_bp.route('/status', methods=['GET'])
def status():
    return {"status": "API is running"}, 200
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

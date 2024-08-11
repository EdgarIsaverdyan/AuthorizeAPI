from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to your actual secret key

jwt = JWTManager(app)

# In-memory blacklist for tokens
blacklist = set()

@app.route('/get_token', methods=['POST'])
def get_token():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400

    username = data['username']
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

@app.route('/refresh_token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    new_refresh_token = create_refresh_token(identity=current_user)
    return jsonify(access_token=new_access_token, refresh_token=new_refresh_token), 200

@app.route('/add_to_blocklist', methods=['DELETE'])
@jwt_required()
def add_to_blocklist():
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify({'message': 'Successfully logged out'}), 200

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    jti = jwt_data['jti']
    return jti in blacklist

if __name__ == '__main__':
    app.run(debug=True)

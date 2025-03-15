from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Secret key to encode the JWT token
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# In-memory storage for users (Replace with a database in production)
users = []

# Route for registering a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Extract the username and password from the request data
    username = data.get('username')
    password = data.get('password')

    # Check if username already exists
    if any(user['username'] == username for user in users):
        return jsonify({"message": "User already exists!"}), 400

    # Hash the password using Bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Save user details
    users.append({"username": username, "password": hashed_password})

    return jsonify({"message": "User registered successfully!"}), 201

# Route for logging in (generates JWT token)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Find the user
    user = next((user for user in users if user['username'] == username), None)

    if user is None or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid credentials!"}), 401

    # Create JWT token
    access_token = create_access_token(identity=username)

    return jsonify(access_token=access_token), 200

# Protected route that requires a valid JWT token
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(message="This is a protected route"), 200

if __name__ == '__main__':
    app.run(debug=True)

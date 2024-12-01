import sqlite3
from flask import Flask, request, jsonify
from bcrypt import hashpw, gensalt, checkpw



app = Flask(__name__)

@app.route('/')
def home():
    return "Create Successfully!"


DATABASE = 'users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


def get_db_connection():
    return sqlite3.connect(DATABASE)


def hash_password(password, salt):
    return hashpw(password.encode('utf-8'), salt).decode('utf-8')


def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# create new account 
@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "username and password not null"}), 400


    if get_user_by_username(username):
        return jsonify({"error": "username already exist"}), 400

    
    salt = gensalt()
    password_hash = hash_password(password, salt)


    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)',
        (username, salt.decode('utf-8'), password_hash)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "create account success"}), 201

# log in 
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "username and password not null"}), 400

    # search account info
    user = get_user_by_username(username)
    if not user:
        return jsonify({"error": "username not regist"}), 401

    # get account info
    _, _, stored_salt, stored_hash = user

    # compare old password
    if checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return jsonify({"message": "login success"}), 200
    else:
        return jsonify({"error": "password error"}), 401

# update new passsword
@app.route('/update-password', methods=['PUT'])
def update_password():
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not username or not old_password or not new_password:
        return jsonify({"error": "username password ,new pwd not null"}), 400

    # search account info
    user = get_user_by_username(username)
    if not user:
        return jsonify({"error": "username not regist"}), 401

    # get account info
    user_id, _, stored_salt, stored_hash = user

    # compare old password
    if not checkpw(old_password.encode('utf-8'), stored_hash.encode('utf-8')):
        return jsonify({"error": "password error"}), 401

    # update password
    salt = gensalt()
    new_password_hash = hash_password(new_password, salt)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE users SET salt = ?, password_hash = ? WHERE id = ?',
        (salt.decode('utf-8'), new_password_hash, user_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "update password success"}), 200


# Main
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, render_template, request, flash, redirect, session, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_pymongo import PyMongo
import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

app = Flask(__name__)
secret_key = secrets.token_hex(16)
#"36024aafe2dbe4b763921f96244aa393"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
#"mongodb+srv://rrcoder0167:1F4iy9NBl7LJjcUs@orange-chat.xb2revk.mongodb.net/chat_db"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)
mongo.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Add a new user to the MongoDB database
def add_user(user):
    mongo.db.users.insert_one(user.to_dict())

# Query all users from the MongoDB database
def get_all_users():
    return list(mongo.db.users.find())

# Query a user by email from the MongoDB database
def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

# Update a user in the MongoDB database
def update_user(user):
    mongo.db.users.update_one({"email": user.email}, {"$set": user.to_dict()})

class User(UserMixin):
    def __init__(self, email, password, username, name, join_date, role, last_seen, status, avatar, _id=None):
        self.email = email
        self.password = generate_password_hash(password)
        self.username = username
        self.name = name
        self.join_date = join_date
        self.role = role
        self.last_seen = last_seen
        self.status = status
        self.avatar = avatar
        self._is_authenticated = False
        self._id = _id
        self.id = str(_id) if _id else None

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        if self.id:
            return self.id
        return None
    
    def is_authenticated(self):
        return self._is_authenticated
    
    def authenticate(self):
        self._is_authenticated = True

    def logout(self):
        self._is_authenticated = False
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'name': self.name,
            'join_date': self.join_date,
            'role': self.role,
            'last_seen': self.last_seen,
            'status': self.status,
            'avatar': self.avatar,
            'is_authenticated': self._is_authenticated
        }

def authenticate(email, password):
    user_profile = mongo.db.users.find_one({"email": email})
    if user_profile:
        hashed_password = user_profile['password']
        if check_password_hash(hashed_password, password):
            user = User(user_profile['email'],
                        user_profile['password'],
                        user_profile['username'],
                        user_profile['name'],
                        user_profile['join_date'],
                        user_profile['role'],
                        user_profile['last_seen'],
                        user_profile['status'],
                        user_profile['avatar'],
                        user_profile["_id"])
            return user
    return None


class Friends:
    def __init__(self, user_id, friend_id, friends_since):
        self.user_id = user_id
        self.friend_id = friend_id
        self.friends_since = friends_since

    def add_to_db(self):
        mongo.db.friends.insert_one({
            'user_id': self.user_id,
            'friend_id': self.friend_id
        })

class FriendRequest:
    def __init__(self, sender_id, receiver_id, status):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.status = status

    def add_to_db(self):
        mongo.db.friend_requests.insert_one({
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'status': self.status
        })


@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    return User(
            user['email'],
            user['password'],
            user['username'],
            user['name'],
            user['join_date'],
            user['role'],
            user['last_seen'],
            user['status'],
            user['avatar'],
            str(user["_id"])
        )


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/griddiman')
def griddiman():
    return render_template('rickroll.html')

@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='images/favicon.ico')

@app.route("/")
def home():
    if session.get("logged_in") == True:
        user_id = session.get("id")
        pending_friend_requests = list(mongo.db.friend_requests.find({"sender_id": user_id, "status": "pending"}))
        pending_friend_requests_with_usernames = []
        for pending_friend_request in pending_friend_requests:
            receiver_id = pending_friend_request["receiver_id"]
            receiver = mongo.db.users.find_one({"_id": ObjectId(receiver_id)})
            friend_request_id = pending_friend_request["_id"]
            if receiver:
                pending_friend_requests_with_usernames.append({"username": receiver["username"], "friend_request": pending_friend_request, "id": friend_request_id})
        incoming_friend_requests = list(mongo.db.friend_requests.find({"receiver_id": user_id, "status": "pending"}))
        incoming_friend_requests_with_usernames = []
        for incoming_friend_request in incoming_friend_requests:
            sender_id = incoming_friend_request["sender_id"]
            sender = mongo.db.users.find_one({"_id": ObjectId(sender_id)})
            sender_friend_request_id = incoming_friend_request["_id"]
            if sender:
                incoming_friend_requests_with_usernames.append({"username": sender["username"], "friend_request": incoming_friend_request, "id": sender_friend_request_id})
        print(incoming_friend_requests_with_usernames)
        friendships = list(mongo.db.friends.find({"user_id": user_id}))
        print(friendships)
        friends = []
        for friend in friendships:
            friend_id = friend["friend_id"]
            friend = mongo.db.users.find_one({"_id": ObjectId(friend_id)})
            if friend:
                friends.append(friend)
        return render_template("home.html", pending_friend_requests=pending_friend_requests_with_usernames, incoming_friend_requests=incoming_friend_requests_with_usernames, friends = friends)
    else:
        return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = authenticate(email, password)
        if user:
            login_user(user)
            mongo.db.users.update_one({'email': email}, {'$set': {'status': 'active', 'last_seen': datetime.datetime.utcnow()}})
            flash("Welcome Back!! Logged in successfully.", category="success")
            session["logged_in"] = True
            session["id"] = current_user.id
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.", category="error_high")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        username = request.form["username"]
        if name == "":
            name = username
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            flash("Passwords do not match.")
            return render_template("signup.html")

        existing_user_email = mongo.db.users.find_one({"email": email})
        existing_user_username = mongo.db.users.find_one({"username": username})
        if existing_user_email:
            flash("A user with that email address already exists.", category="error_medium")
            return render_template("signup.html")
        elif existing_user_username:
            flash("A user with that username already exists.", category="error_medium")
            return render_template("signup.html")

        join_date = datetime.datetime.utcnow()
        user = User(email, password, username, name, join_date, 'user', join_date, 'active', 'default.jpg')
        add_user(user)
        flash("You are now signed up!")
        return render_template("home.html")
    else:
        return render_template("signup.html")



@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        session.clear()
        mongo.db.users.update_one({'email': current_user.email}, {'$set': {'status': 'away', 'last_seen': datetime.datetime.utcnow()}})
        logout_user()
        flash("Logged out successfully.", category="success")
    return redirect(url_for("home"))


@app.route('/about')
def about():
    return 'orange chat is like cwazy at life bwo'

@app.route('/testing')
def testing():
    return render_template('testing.html')

@app.route("/search_friends", methods=["GET", "POST"])
@login_required
def search_friends():
    if request.method == "POST":
        search_query = request.form["search_query"]
        user = mongo.db.users.find_one({"email": search_query})
        if user and user["email"] == current_user.email:
            message = f"self_friend_req-error"
            response = {"success": False, "message": message}
            return jsonify(response)
        elif user:
            message = f"We found user {user['username']}!"
            response = {"success": True, "message": message}
            return jsonify(response)
        else:
            message = f"user_exists_none-error"
            response = {"success": False, "message": message}
            return jsonify(response)
    else:
        return render_template("home.html")


@app.route("/send_friend_request", methods=["POST"])
@login_required
def send_friend_request():
    if request.method == "POST":
        receiver_email = request.form["receiver_email"]
        sender = User(_id=current_user.id,
              username=current_user.username,
              email=current_user.email,
              password=current_user.password,
              name=current_user.name,
              join_date=current_user.join_date,
              role=current_user.role,
              last_seen=current_user.last_seen,
              status=current_user.status,
              avatar=current_user.avatar)

        receiver_data = mongo.db.users.find_one({"email": receiver_email})
        receiver = User(
            email=receiver_data['email'],
            password=receiver_data['password'],
            username=receiver_data['username'],
            name=receiver_data['name'],
            join_date=receiver_data['join_date'],
            role=receiver_data['role'],
            last_seen=receiver_data['last_seen'],
            status=receiver_data['status'],
            avatar=receiver_data['avatar'],
            _id=receiver_data['_id']
        )
        if receiver is None:
            return jsonify({"message": "user_exists_none-error"}), 401
        existing_request_to_sender = mongo.db.friend_requests.find_one({"sender_id": receiver._id, "receiver_id": sender._id})
        if existing_request_to_sender is not None:
            return jsonify({"message": "friend_req_alr_received-error"}), 500
        
        existing_friend_request = mongo.db.friend_requests.find_one({"sender_id": sender._id, "receiver_id": receiver._id})

        if existing_friend_request is not None:
            return jsonify({"message": "friend_req_alr_sent-error"}), 400
        
        friend_request = {
            "sender_id": sender.id,
            "receiver_id": receiver.id,
            "status": "pending"
        }
        mongo.db.friend_requests.insert_one(friend_request)
        return jsonify({"message": "send_friend_req-success", "id": receiver.id, "username": receiver.username})
    else:
        flash("A fatal system error has ocurred. Please try again later.", category="error_high")


@app.route("/cancel_friend_request", methods=["POST"])
@login_required
def cancel_friend_request():
    if request.method == "POST":
        friend_request_id = request.form["friend_request_id"]
        print(friend_request_id)
        friend_request = mongo.db.friend_requests.find_one({'_id': ObjectId(friend_request_id)})
        if friend_request is None:
            return jsonify({"message": "friend_request_not_found-error"}), 404
        mongo.db.friend_requests.delete_one({'_id': ObjectId(friend_request_id)})
        flash("Friend Request Cancelled.", category="success")
        return jsonify({"message": "cancel_friend_request-success", "flash_message": "Friend Request Cancelled."})
    else:
        return jsonify({"message": "bad_request-error"}), 400


@app.route("/accept_friend_request", methods=["POST"])
@login_required
def accept_friend_request():
    if request.method == "POST":
        friend_request_id = request.form["friend_request_id"]
        friend_request = mongo.db.friend_requests.find_one({'_id': ObjectId(friend_request_id)})
        if friend_request is None:
            return jsonify({"message": "friend_request_not_found-error"}), 404
        sender = mongo.db.users.find_one({'_id': ObjectId(friend_request['sender_id'])})
        if sender is None:
            return jsonify({"message": "sender_not_found-error"}), 404
        friend_info = {
            'user_id': current_user.id,
            'friend_id': friend_request['sender_id'],
            'friends_since':  datetime.datetime.utcnow()
        }
        mongo.db.friends.insert_one(friend_info)
        mongo.db.friend_requests.delete_one({'_id': ObjectId(friend_request_id)})
        flash("Congrats! Now you're friends with " + sender['username'], category="success")
        return jsonify({"message": "accept_friend_request-success", "friend_id": str(friend_info['_id'])})
    else:
        flash("Sorry, there was an error, please try again later.", category="error_high")
        return jsonify({"message": "bad_request-error"}), 400


@app.route("/decline_friend_request", methods=["POST"])
@login_required
def decline_friend_request():
    if request.method == "POST":
        friend_request_id = request.form["friend_request_id"]
        mongo.db.friend_requests.delete_one({'_id': ObjectId(friend_request_id)})
        flash("Friend Request Declined.", category="success")
        return jsonify({"message": "decline_friend_request-success"})
    else:
        flash("Sorry, there was an error, please try again later.", category="error_high")
        return jsonify({"message": "bad_request-error"}), 400


if __name__ == "__main__":
    app.run()

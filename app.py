from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))
    name = db.Column(db.String(100))
    # methods
    def __init__(self, email, password, username, name):
        self.email = email
        self.password = generate_password_hash(password)
        self.username = username
        self.name = name

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id
    @property
    def is_active(self):
        return True


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    else:
        return None

class Friends(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend = db.relationship('User', foreign_keys=[friend_id])

class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='pending')
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = '019vcxpr!rp5lz13'
db.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(user_id)

@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='images/favicon.ico')

@app.route("/")
def home():
    if current_user.is_authenticated:
        friend_requests = FriendRequest.query.filter_by(receiver_id=current_user.id).all()
        pending_friend_requests = FriendRequest.query.filter_by(sender_id=current_user.id, status='pending').all()
        return render_template("home.html", friend_requests=friend_requests, pending_friend_requests=pending_friend_requests)
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
            flash("Welcome Back!! Logged in successfully.", category="success")
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
        existing_user_email = User.query.filter_by(email=email).first()
        existing_user_username = User.query.filter_by(username=username).first()
        if existing_user_email:
            flash("A user with that email address already exists.", category="error_medium")
            return render_template("signup.html")
        elif existing_user_username:
            flash("A user with that username already exists.", category="error_medium")
            return render_template("signup.html")
        user = User(email, password, username, name)
        db.session.add(user)
        db.session.commit()
        flash("You are now signed up!")
        return render_template("home.html")
    else:
        return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
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
        user = User.query.filter_by(email=search_query).first()
        if user == current_user:
            message = f"self_friend_req-error"
            response = {"success": False, "message": message}
            return jsonify(response)
        elif user:
            message = f"We found user {user.username}!"
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
        receiver = User.query.filter_by(email=receiver_email).first()
        if receiver is None:
            return jsonify({"message": "user_exists_none-error"}), 401
        sender = current_user

        existing_request_to_sender = FriendRequest.query.filter_by(sender_id=receiver.id, receiver_id=sender.id).first()
        if existing_request_to_sender is not None:
            return jsonify({"message": "friend_req_alr_received-error"}), 500
        
        existing_friend_request = FriendRequest.query.filter_by(sender_id=sender.id, receiver_id=receiver.id).first()
        if existing_friend_request is not None:
            return jsonify({"message": "friend_req_alr_sent-error"}), 400
        friend_request = FriendRequest(sender_id=sender.id, receiver_id=receiver.id)
        db.session.add(friend_request)
        db.session.commit()
        return jsonify({"message": "send_friend_req-success", "id": receiver.id, "username": receiver.username})
    else:
        flash("A fatal system error has ocurred. Please try again later.", category="error_high")

@app.route("/cancel_friend_request", methods=["POST"])
@login_required
def cancel_friend_request():
    if request.method == "POST":
        friend_request_id = request.form["friend_request_id"]
        friend_request = FriendRequest.query.get(friend_request_id)
        if friend_request is None:
            return jsonify({"message": "friend_request_not_found-error"}), 404
        db.session.delete(friend_request)
        db.session.commit()
        flash("Friend Request Cancelled.", category="success")
        return jsonify({"message": "cancel_friend_request-success", "flash_message": "Friend Request Cancelled."})
    else:
        return jsonify({"message": "bad_request-error"}), 400




@app.route("/accept_friend_request", methods=["POST"])
@login_required
def accept_friend_request():
    if request.method == "POST":
        friend_request_id = request.form["friend_request_id"]
        friend_request = FriendRequest.query.get(friend_request_id)
        if friend_request is None:
            return jsonify({"message": "friend_request_not_found-error"}), 404
        sender = User.query.get(friend_request.sender_id)
        if sender is None:
            return jsonify({"message": "sender_not_found-error"}), 404
        friend_info = Friends(user_id=current_user.id, friend_id=friend_request.sender_id)
        db.session.add(friend_info)
        db.session.delete(friend_request)
        db.session.commit()
        friend = Friends.query.get(friend_info)
        print(type(friend))
        flash("Congrats! Now you're friends with " + sender.username, category="success")
        return jsonify({"message": "accept_friend_request-success", "friend_id": friend})
    else:
        flash("Sorry, there was an error, please try again later.", category="error_high")
        return jsonify({"message": "bad_request-error"}), 400

@app.route("/decline_friend_request", methods=["POST"])
@login_required
def decline_friend_request():
    if request.method == "POST":
        friend_request_id = request.form["friend_request_id"]
        friend_request = FriendRequest.query.get(friend_request_id)
        if friend_request is None:
            return jsonify({"message": "friend_request_not_found-error"}), 404
        db.session.delete(friend_request)
        db.session.commit()
        flash("Friend Request Declined.", category="success")
        return jsonify({"message": "decline_friend_request-success"})
    else:
        flash("Sorry, there was an error, please try again later.", category="error_high")
        return jsonify({"message": "bad_request-error"}), 400

if __name__ == "__main__":
    app.run(debug=True)
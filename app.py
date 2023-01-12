from flask import Flask, get_flashed_messages, render_template, request, flash, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_security import views

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    #methods 
    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    @property
    def is_active(self):
        return True

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None



app = Flask(__name__)
app.register_blueprint(views.register)
app.register_blueprint(views.reset_password)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users/riddhiman.rana/instance/users.db'
app.config['SECRET_KEY'] = '019vcxpr!rp5lz13'
s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
token = s.dumps({ 'user_id': 1 }).decode('utf-8')

# Verifying a token
s = Serializer(app.config['SECRET_KEY'])
try:
    data = s.loads(token)
    print(data)
except:
    print("Invalid token.")
db.init_app(app)
db.create_all(app=app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = authenticate(email, password)
        if user:
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            flash("Passwords do not match.")
            return render_template("signup.html")
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("A user with that email address already exists.")
            return render_template("signup.html")
        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        flash("you are now signed up!")
        return render_template("home.html")
    else:
        return render_template("signup.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, port=8080)
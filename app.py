from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
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
    return None


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
            flash("A user with that email address already exists.")
            return render_template("signup.html")
        elif existing_user_username:
            flash("A user with that username already exists.")
            return render_template("signup.html")
        user = User(email, password, username, name)
        db.session.add(user)
        db.session.commit()
        flash("you are now signed up!")
        return render_template("home.html")
    else:
        return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

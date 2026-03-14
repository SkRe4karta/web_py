from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Для доступа к странице необходимо войти в систему."

# Пользователь (по заданию)
users = {
    "user": {
        "password": "qwerty"
    }
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None


@app.route("/")
def index():
    if "visits" not in session:
        session["visits"] = 0

    session["visits"] += 1
    visits = session["visits"]

    return render_template("index.html", visits=visits)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user, remember=remember)

            flash("Вы успешно вошли в систему!", "success")

            next_page = request.args.get("next")

            return redirect(next_page) if next_page else redirect(url_for("index"))

        else:
            flash("Неверный логин или пароль", "danger")

    return render_template("login.html")


@app.route("/secret")
@login_required
def secret():
    return render_template("secret.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
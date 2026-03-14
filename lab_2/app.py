from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# URL параметры
# -----------------------------
@app.route("/url")
def url_params():

    resp = make_response(
        render_template(
            "url_params.html",
            args=request.args
        )
    )

    resp.set_cookie("username", "student")

    return resp


# -----------------------------
# Заголовки запроса
# -----------------------------
@app.route("/headers")
def headers():

    return render_template(
        "headers.html",
        headers=request.headers
    )


# -----------------------------
# Cookies
# -----------------------------
@app.route("/cookies")
def cookies():

    return render_template(
        "cookies.html",
        cookies=request.cookies
    )


# -----------------------------
# Форма авторизации
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    login_value = None
    password_value = None

    if request.method == "POST":

        login_value = request.form.get("login")
        password_value = request.form.get("password")

    return render_template(
        "login.html",
        login=login_value,
        password=password_value
    )


# -----------------------------
# Проверка телефона
# -----------------------------
@app.route("/phone", methods=["GET", "POST"])
def phone():

    phone_raw = ""
    error = None
    formatted = None

    if request.method == "POST":

        phone_raw = request.form.get("phone", "")

        allowed = set("0123456789 ()-+.")

        for ch in phone_raw:
            if ch not in allowed:
                error = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
                break

        if error is None:

            digits = ""
            for ch in phone_raw:
                if ch.isdigit():
                    digits += ch

            if phone_raw.startswith("+7") or phone_raw.startswith("8"):
                required = 11
            else:
                required = 10

            if len(digits) != required:
                error = "Недопустимый ввод. Неверное количество цифр."

        if error is None:

            if len(digits) == 11:
                digits = digits[1:]

            a = digits[0:3]
            b = digits[3:6]
            c = digits[6:8]
            d = digits[8:10]

            formatted = f"8-{a}-{b}-{c}-{d}"

    return render_template(
        "phone.html",
        phone_raw=phone_raw,
        error=error,
        formatted=formatted
    )


if __name__ == "__main__":
    app.run(debug=True)
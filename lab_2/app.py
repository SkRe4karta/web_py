from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/request-info")
def request_info():

    resp = make_response(
        render_template(
            "request_info.html",
            args=request.args,
            headers=request.headers,
            cookies=request.cookies,
            form=request.form
        )
    )

    # устанавливаем cookie
    resp.set_cookie("username", "student")

    return resp


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        login_value = request.form.get("login", "")
        password_value = request.form.get("password", "")

        # передаем form напрямую
        return render_template(
            "request_info.html",
            args=request.args,
            headers=request.headers,
            cookies=request.cookies,
            form=request.form
        )

    return render_template("login.html")


@app.route("/phone", methods=["GET", "POST"])
def phone():
    phone_raw = ""
    error = None
    formatted = None

    if request.method == "POST":
        phone_raw = request.form.get("phone", "")

        # Разрешённые дополнительные символы
        allowed_extra = set(" ()-+.")

        # 1) Проверка на недопустимые символы
        for ch in phone_raw:
            if not (ch.isdigit() or ch in allowed_extra):
                error = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
                break

        # 2) Проверка количества цифр
        if error is None:
            digits = "".join(ch for ch in phone_raw if ch.isdigit())
            p = phone_raw.strip()

            # 11 цифр, если начинается с "+7" или "8", иначе 10
            required_len = 11 if (p.startswith("+7") or p.startswith("8")) else 10

            if len(digits) != required_len:
                error = "Недопустимый ввод. Неверное количество цифр."

        # 3) Форматирование, если ошибок нет
        if error is None:
            # приводим к "10 цифрам основной части"
            core = digits[1:] if len(digits) == 11 else digits

            a = core[0:3]
            b = core[3:6]
            c = core[6:8]
            d = core[8:10]
            formatted = f"8-{a}-{b}-{c}-{d}"

    return render_template(
        "phone.html",
        phone_raw=phone_raw,
        error=error,
        formatted=formatted
    )


if __name__ == "__main__":
    app.run(debug=True)
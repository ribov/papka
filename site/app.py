from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if (username == "") or (password == ""):
                return "Вы не ввели логин или пароль!"
            try:
                cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s", (str(username), str(password)))
                records = list(cursor.fetchall())
                return render_template('acc.html', full_name=records[0][1], full_login=records[0][2],
                                       full_password=records[0][3])
            except:
                return "Вы не зарегистрированы!"
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if (name == "") or (login == "") or (password == ""):
            return "Все поля должны быть заполнены!"
        cursor.execute("INSERT INTO users(name, login, password) VALUES (%s,%s,%s)",
                       (str(name), str(login), str(password)))
        conn.commit()
        return redirect("/login/")
    return render_template('registration.html')


conn = psycopg2.connect(database="postgres", user="postgres", password="9094391", host="localhost", port="5432")

cursor = conn.cursor()
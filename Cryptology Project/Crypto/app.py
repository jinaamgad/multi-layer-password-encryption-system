from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import cryptology  # your existing cryptology.py

app = Flask(__name__)
app.secret_key = 'super_secret_key'

register = cryptology.register
login_func = cryptology.login


def get_user_count():
    if os.path.exists("users.txt"):
        with open("users.txt", "r", encoding="utf-8") as f:
            return len(f.readlines())
    return 0


@app.route('/')
def index():
    user_count = get_user_count()
    return render_template('index.html', user_count=user_count)


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def handle_register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
        return redirect(url_for('register_page'))
    else:
        username_exists = False
        if os.path.exists("users.txt"):
            with open("users.txt", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(username + ":"):
                        username_exists = True
                        break
        if username_exists:
            flash("Username already exists!")
            return redirect(url_for('register_page'))
        else:
            register(username, password)
            flash("Registered Successfully!")
            return redirect(url_for('welcome', username=username))


@app.route('/welcome')
def welcome():
    username = request.args.get('username', 'User')
    return render_template('welcome.html', username=username)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
        flash("Please try again")
        return redirect(url_for('login'))

    if login_func(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        flash("Please try again")
        return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/presentation')
def presentation():
    return render_template('presentation.html')


if __name__ == '__main__':
    # debug=True shows errors in the browser
    app.run(debug=True)

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post


@app.route('/post', methods=["POST"])
def post():
    post = Post(author=current_user, body=request.values.get('post'))
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template("index.html", user=current_user, posts=posts)

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        user = User.query.filter_by(username=request.values.get("user")).first()
        if user is None or not user.password == request.values.get("pass"):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        r = request.values.get("remember") == "on"
        login_user(user, remember=r)
        return redirect(url_for('index'))
    return render_template("login.html" , title="Login")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        user = User(username=request.values.get('user'),
                    password=request.values.get('pass'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html" , title="Register")

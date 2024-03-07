from flask import Blueprint, render_template, request,flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password = request.form.get('password')

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password Try Again", category='error')
        else:
            flash("E-Mail Does Not Exists", category='error')

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logot():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email= request.form.get('email')
        username= request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        username_control= User.query.filter_by(email=username).first()
        if username_control:
            flash("This User Name Already Exists", category="error")
        elif user:
            flash("This Email Already Exists", category="error")
        elif password1 != password2:
            flash("Passwords should be the same", category="error")
        elif ' ' in username:
            flash("Username should be a single word", category="error")
        elif not username.isalnum():
            flash("Username should contain only letters and numbers", category="error")
        elif username.isdigit():
            flash("Username should contain letters", category="error")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account Created Successfully", category="success")
            return redirect(url_for('views.home'))


    return render_template("sign_up.html",user=current_user)
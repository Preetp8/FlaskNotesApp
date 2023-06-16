from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash #allows to hash password
from . import db

from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

#defining login, signup, and log out

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # check if we are actually signing in
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # check if email typed in is in the db (queery the db)
        user = User.query.filter_by(email=email).first() #GIVES FIRST result user that has this email
        # check the password
        if user:
            if check_password_hash(user.password, password): #hashes given passowrd then checks the one in db
                flash('LOG IN SUCCESSFUL', category = 'success')
                login_user(user, remember=True) #logs in user and remembers that they are logged in until broweser restarted
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category = 'error')
        else:
            flash('Email does not exist', category = 'error')
            


    # ex) pasign variable to login from backend (this)v
    # return render_template("login.html",  text="testing", user = "preet")
    return render_template("login.html",  user=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required #make sure that you cant log out if you are not logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # differentiate between GET and POST
    if request.method =='POST':
        #get all info from the forms
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first #GIVES FIRST result user that has this email

        if user:
            flash('Email already exists', category='error')
        # make sure info is valid
        elif len(email) < 4:
            flash("Email must be larger than 4 chars.", category="error") #categories can be anything as long as you know what they mean to customize in future
        elif len(first_name) < 2:
            flash("First Name must be larger than 1 char.", category="error")
        elif password1 != password2:
            flash("Passwords dont match.", category="error")
        elif len(password1) < 7:
            flash("Password too short must be at least 7 chars.", category="error")
        else:
            new_user = User(email=email, first_name = first_name, password = generate_password_hash(password1, method='sha256'))
            
            # add the user to the db
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="error")
            login_user(user, remember=True) #logs in user and remembers that they are logged in until broweser restarted

            #redirect them to the home page
            return redirect(url_for('views.home')) #views: name of blueprint // home is the name of the page
            


    return render_template("signup.html", user=current_user)
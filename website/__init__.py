from flask import Flask; 
from flask_sqlalchemy import SQLAlchemy;
from os import path
from flask_login import LoginManager

# pick define new db
db = SQLAlchemy()
DB_NAME = "database.db" # this objeect use when you need to add something to db


#
def create_app():
    app = Flask(__name__) #__name__ = name of file ran

    #needed for flask app
    # secret key should be secret in production
    app.config['SECRET_KEY'] = 'thiscanbeanystring'

    # tell flask you are eusing DB and whre it is
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #located here 

    # init our db by giving flask app
    db.init_app(app)

    #import blueprint
    from .views import views
    from .auth import auth

    #register blueprint
    app.register_blueprint(views, url_prefix='/') # url prefix asks Urls are stored inside the blueprint files how do i access them?

    app.register_blueprint(auth, url_prefix='/') 
    #ex) if url prefix were to be '/auth/' -> then whatever name inside view was  
    ## so youd have to go to /auth/hello -> 


    # check to see if db created before app ran
    from .models import User, Note


    create_database(app)

    # login user
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #where should flask redirect if user not logged in 
    login_manager.init_app(app)

    # trelling flask how we log in a user   
    @login_manager.user_loader
    def load_user(id):
        # were looking for user model and referenceing them to the id
        return User.query.get(int(id)) #user qeuyry get - is like filter by but DEFAULT looks for primary key
    
    

    return app


# check if db exists and if so then make it
def create_database(app):
    if not path.exists('website/' + DB_NAME): #check if db exists
        # db.create_all(app= app) #create it (app passed to tell alchemy which app its for and it has the URI on it for the db

        # from . import models

        with app.app_context():
            db.create_all()

        print("created DB!!!!!!!!") 
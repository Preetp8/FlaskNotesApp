# Here we add blueprint with all URLS or routes defined in it
#
#

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
views = Blueprint('views', __name__)

# to define a view or route
@views.route('/', methods=['GET', 'POST']) #decorator
@login_required #cant get to home page unless loggede in
def home(): # function will run whenever you go to the home page

    #check if requrest.method is == POST
    if request.method == 'POST':
        note = request.form.get("note");
        
        if len(note) < 1:
            flash("Write a longer note.", category="error")
        else:
            new_note = Note(data = note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("NOTE ADDED.", category="success")


    return render_template("home.html", user = current_user)


# this links to fetch in js
@views.route('/delete-note', methods=['POST'])


# access

def delete_note():
    # look for note id that was sent, request comes in as data paramete = JSON
    note = json.loads(request.data) # takes in data from a POST request, load it as JSON obj or python dict
    noteId = note['noteId'] # access note ID attribute
    note = Note.query.get(noteId) #look for the note with that id
    
    # check if that note exists
    if note:
        # if user owns the notee
        if note.user_id == current_user.id:
            db.session.delete(note) #delete it
            db.session.commit() 
            
    return jsonify({}) #reutrn empty response bc view needs a return

def see_db():
    user.query.all();
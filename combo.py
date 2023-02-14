import pprint
from datetime import datetime, timedelta

from flask import Blueprint, redirect, render_template, request

from scripts.helpers import *

# this is hardcoded for now
hardCodeUserId = 0

combo = Blueprint("combo", __name__, template_folder="templates")

@combo.route("/add_combo")
def add_combo():
    db = get_db()
    c = db.cursor()
    
    
    
    db.close()
    return render_template("", )
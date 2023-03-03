import pprint
from datetime import datetime, timedelta

from flask import Blueprint, redirect, render_template, request, url_for

from scripts.helpers import *

# this is hardcoded for now
hardCodeUserId = 0


nutrient = Blueprint("nutrient", __name__, template_folder="templates")


@nutrient.route("/addNutrient", methods=["POST"])
def addNutrient():
    db = get_db()
    c = db.cursor()
    if request.method == "POST":

        name = request.form.get("name")
        description = request.form.get("description")
        header = request.form.get("header")

        c.execute(
            "INSERT INTO nutrient (timestamp, name, description, nutrient_header_id, user_id) VALUES (?, ?, ?, ?, ?)",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                name,
                description,
                header,
                hardCodeUserId,
            ),
        )

    db.commit()
    db.close
    return redirect("/")
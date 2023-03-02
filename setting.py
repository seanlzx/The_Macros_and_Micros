import pprint
from datetime import datetime, timedelta

from flask import Blueprint, redirect, render_template, request, url_for

from scripts.helpers import *

# this is hardcoded for now
hardCodeUserId = 0
hardCodeDriGroupName = "male 19-30"

setting = Blueprint("setting", __name__, template_folder="templates")


@setting.route("/editSetting", methods=["POST"])
def editSetting():
    db = get_db()
    c = db.cursor()

    infoDict = getFormListValues(
        [
            "id", "name", "weight", "height",
            "gender", "age", "from_date", "from_current",
            "to_date", "to_current", "dri_group", "user_type"
        ]
    )
    
    if infoDict["from_current"]:
        infoDict["from_date"] = "curr"
    if infoDict["to_current"]:
        infoDict["to_date"] = "curr"
    
    if not all(key in infoDict for key in ["id", "name", "weight", "height", "gender", "age", "to_date", "from_date", "user_type"]):
        return apology("Form insufficient info")
    
    c.execute("DELETE FROM user WHERE id = ?", (infoDict["id"],),)

    c.execute("""
    INSERT INTO user (id, name, timestamp, weight, height, gender, age, user_type, from_date, to_date, dri_group)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        infoDict["id"],
        infoDict["name"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        infoDict["weight"],
        infoDict["height"],
        infoDict["gender"],
        infoDict["age"],
        infoDict["user_type"],
        infoDict["from_date"],
        infoDict["to_date"],
        infoDict["dri_group"]
    ))

    db.commit()
    db.close()
    return redirect("/")


@setting.route("/setting_dri_search")
def setting_dri_search():
    db = get_db()
    c = db.cursor()

    search_input = request.args.get("search_input")

    raw_dri_results = ()
    if search_input:
        raw_dri_results = c.execute(
            """
            SELECT d.group_name, d.timestamp, u.name 
            FROM dri d
            JOIN user u
            ON d.user_id = u.id 
            WHERE d.active = 1
            AND d.group_name LIKE ?
            GROUP BY d.group_name;                           
            """,
            (f"%{search_input}%",),
        )
    else:
        raw_dri_results = c.execute(
            """
            SELECT d.group_name, d.timestamp, u.name 
            FROM dri d
            JOIN user u
            ON d.user_id = u.id 
            WHERE d.active = 1
            GROUP BY d.group_name;
            """
        )

    dri_results = listOfTuplesToListOfDict(
        raw_dri_results,
        ["name", "timestamp", "username"],
    )

    db.close()
    return render_template("setting_dri_search_result.html", dri_results=dri_results)

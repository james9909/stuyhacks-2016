from flask import Blueprint, request, session

from decorators import api_wrapper, login_required, WebException
from models import db, Project

blueprint = Blueprint("projects", __name__)

@blueprint.route("/add", methods=["POST"])
@api_wrapper
def add_project():
    form = request.form
    title = form.get("title")
    uid = session.get("uid")
    project = Project(uid, title)

    db.session.add(project)
    db.session.commit()

    return { "success": 1, "message": "Project added." }

def get_project(pid=None, uid=None):
    match = {}
    if pid is not None:
        match.update({"pid": pid})
    if uid is not None:
        match.update({"uid": uid})

    return Project.query.filter_by(**match)

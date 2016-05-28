from flask import current_app as app, Blueprint, request

from decorators import api_wrapper, WebException
from models import db, Task

blueprint = Blueprint("tasks", __name__)

@blueprint.route("/add", methods=["POST"])
@api_wrapper
def add_task_request():
    form = request.form
    title = form.get("title")
    parent = form.get("parent", -1)
    priority = form.get("priority", 0)
    task = Task(title, priority=priority, parent=parent)
    with app.app_context():
        db.session.add(task)
        db.session.commit()

    return { "success": 1, "message": "Task added." }

@blueprint.route("/remove", methods=["POST"])
@api_wrapper
def remove_task_request():
    form = request.form
    tid = form.get("tid")
    result = get_task(tid=tid)
    task = result.first()
    if task is None:
        raise WebException("Task does not exist.")

    result.delete()
    db.session.commit()
    return { "success": 1, "message": "Task deleted." }

@blueprint.route("/update", methods=["POST"])
@api_wrapper
def update_task_request():
    form = request.form
    updates = {}
    tid = form.get("tid")
    if "title" in form:
        updates.update({"title": form.get("title")})
    if "priority" in form:
        updates.update({"priority": form.get("priority")})

    result = get_task(tid=tid)
    task = result.first()
    if task is None:
        raise WebException("Task does not exist.")

    task.update(**updates)
    db.session.commit()

    return { "success": 1, "message": "Task updated." }

def get_task(tid=None, parent=None, priority=None, completed=False):
    match = {}
    if tid is not None:
        match.update({"tid": tid})
    if parent is not None:
        match.update({"parent": parent})
    if priority is not None:
        match.update({"priority": priority})
    if completed is not None:
        match.update({"completed": completed})

    return Task.query.filter_by(**match)

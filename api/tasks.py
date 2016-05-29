from flask import current_app as app, Blueprint, request, session

from decorators import api_wrapper, login_required, WebException
from models import db, Task

blueprint = Blueprint("tasks", __name__)

@blueprint.route("/add", methods=["POST"])
@api_wrapper
@login_required
def add_task():
    form = request.form
    title = form.get("title")
    parent = form.get("parent", -1)
    priority = form.get("priority", 0)
    uid = session.get("uid")
    task = Task(uid, title, priority=priority, parent=parent)
    with app.app_context():
        db.session.add(task)
        db.session.commit()

    return { "success": 1, "message": "Task added." }

@blueprint.route("/remove", methods=["POST"])
@api_wrapper
@login_required
def remove_task():
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
@login_required
def update_task():
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

def get_all_tasks():
    return Task.query.all()

def tasks_to_list(tasks):
    taskList = []
    for task in tasks:
#        taskList.append(task.__dict__)
#    return taskList
        taskDict = {
            "title"      : task.title,
            "priority"  : task.priority,
            "completed" : task.completed,
            "children"  : task.children
        }
        taskList.append(taskDict)
    return taskList

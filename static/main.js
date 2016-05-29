var api_call = function(method, url, data, success_callback, fail_callback) {
    $.ajax({
        "type": method,
        "datatype": "json",
        "data": data,
        "url": url
    }).done(function(result) {
        success_callback(result);
    }).error(function(jqXHR) {
        fail_callback(JqXHR);
    });
}

var display_message = function(containerId, alertType, message, callback) {
    $("#" + containerId).html("<div class=\"alert alert-" + alertType + "\">" + message + "</div>");
    $("#" + containerId).hide().slideDown("fast", "swing", function() {
        window.setTimeout(function () {
            $("#" + containerId).slideUp("fast", "swing", callback);
        }, message.length * 40);
    });
};

$.fn.serializeObject = function() {
    var a, o;
    o = {};
    a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            return o[this.name].push(this.value || "");
        } else {
            return o[this.name] = this.value || "";
        }
    });
    return o;
};

var login = function() {
    var data = $("#login_form").serializeObject();
    api_call("POST", "/api/users/login", data, function(result) {
        if (result["success"] == 1) {
            display_message("login_msg", "success", result["message"], function() {
                location.href = "/work";
            });
        } else {
            display_message("login_msg", "danger", result["message"]);
        }
    })
}

var register = function() {
    var data = $("#register_form").serializeObject();
    api_call("POST", "/api/users/register", data, function(result) {
        if (result["success"] == 1) {
            display_message("register_msg", "success", result["message"], function() {
                location.href = "/login";
            });
        } else {
            display_message("register_msg", "danger", result["message"]);
        }
    })
}

var global_parent = -1;
var global_project = -1;

$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

var addTask = function(task, project) {
    global_parent = task;
    global_project = project;
    console.log(project);
    $("#newTaskModal").modal();
}

var checkOffTask = function(task) {
    var box = document.getElementById("taskBox" + task);
    api_call("POST","/api/tasks/update", {"completed" : box.checked}, function() {
        display_message("taskMessage"+task, "success", "yay", function() { });
    }, function(){ });
}


$("#task_form_submit").click(function() {
    var data = $("#task_form").serializeObject();
    data["parent"] = global_parent;
    data["pid"] = global_project;

    api_call("POST","/api/tasks/add", data, function(result) {
        if (result["success"] == 1) {
            location.reload();
        }
    }, function() {
    });
});

var add_project = function() {
    var data = $("#new_project").serializeObject();

    api_call("POST", "/api/projects/add", data, function(result) {
        if (result["success"] == 1) {
            location.reload();
        }
    });
};

var delete_task = function(task) {
    api_call("POST", "/api/tasks/remove", {"tid": task}, function(result) {
        if (result["success"] == 1) {
            location.reload();
        }
    });
};

var delete_project = function(project) {
    api_call("POST", "/api/projects/remove", {"pid": project}, function(result) {
        if (result["success"] == 1) {
            location.reload();
        }
    });
};


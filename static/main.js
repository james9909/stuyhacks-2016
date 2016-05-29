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

'use strict';
(function () {
    jQuery.fn.extend({
        disable: function (state) {
            return this.each(function () {
                this.disabled = state;
            });
        }
    });

    $(document).ready(function () {
        setInterval("serverStatus()", 1000);
        $(".button-call").disable(true);
    });

    $(".button-call").click(function () {
        callClient($(this).attr('id'));
    });

    var serverStatus = function () {
        $.get("conference/status")
            .done(function (data) {
                if (data.status == "in-progress" && data.call == 'False') {
                    $("#status").html("READY!");
                    $(".button-call").disable(false);
                }
                else if (data.status == "completed" && data.call == 'False') {
                    $("#status").html("COMPLETED!");
                    $(".button-call").disable(true);
                }
                else if (data.status == "init" && data.call == 'False') {
                    $("#status").html("INIT");
                    $(".button-call").disable(true);
                }
                else if (data.status == "waiting" && data.call == 'False') {
                    $("#status").html("Waiting...");
                    $(".button-call").disable(true);
                }
                else if (data.status == 'ringing' && data.call == 'True') {
                    $("#status").html("Ringing");
                    $(".button-call").disable(true);
                }
                else if (data.status == 'in-progress' && data.call == 'True') {
                    $("#status").html("Call in Progress");
                    $(".button-call").disable(true);
                }
                else if (data.call == 'True') {
                    $("#status").html("Canceled");
                    $(".button-call").disable(false);
                }
            });
    };

    var callClient = function (clientId) {
        $.post("conference/call/" + clientId)
            .done(function () {
                $(".button-call").disable(true);
            });
    };
})();

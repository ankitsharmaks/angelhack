
function updateMessages() {
    var d = $('#messages');
    d.scrollTop(d.prop("scrollHeight"));
}

function updateTags() {
    $.getJSON('/tags?group=' + group_id,
        function(data,status) {
            var $tags = $('#tags');
            $tags.html('');
            $.each(data, function(index, entry){
                $tags.append('<span class="tag">' + entry + '</span> ');
                console.log(entry);
            });
        });
}

$(document).ready(function() {
    var appid = "cd39e41d-8f45-4406-8218-e7f74ffae2f9";
    var endpointId = user;
    var group;

    var client = respoke.createClient({
        appId: appid,
        developmentMode: true
    });

    console.log("Connecting...");
    client.connect({
        endpointId: endpointId // your username is the endpoint
    });

    // "connect" event fired after successful connection to Respoke
    client.listen('connect', function() {
        console.log("Connected to Respoke as \"" + endpointId + "\"");
        // Update group status message
        console.log('Joining group ' + group_id);
        // Automatically join the group once connected
        client.join({
            id: group_id,
            onSuccess: function(grp) {
                console.log('Joined group ' + grp.id);
                group = grp;
            },
            onMessage: function(evt) {
                $("#messages").append(
                    ""+evt.message.endpointId+": " + evt.message.message + "<br>"
                );
                updateMessages();
                updateTags();
            }
        });
    });
    // Send message

    $("#chat-form").submit(function(event) {
        event.preventDefault();
        $chat_form_input = $("#chat-form input");
        var groupMsg = $chat_form_input.val();
        console.log(groupMsg);
        $chat_form_input.val('');
        group.sendMessage({
            message: groupMsg
        });
        $("#messages").append(
            ""+ endpointId+": "+ groupMsg + "<br>"
        );
        updateMessages();

        $.ajax({
            type: "POST",
            url: "/message",
            data: {
                message: groupMsg,
                user: user,
                group: group_id
            },
            success: function (){
                updateTags();
            },
        });
        return false;
    });
});

function updateMessages() {
    var d = $('#messages');
    d.scrollTop(d.prop("scrollHeight"));
}

colors = [
    '#f44336',
    '#03a9f4',
    '#4caf50',
    '#ff9800'
];

function updateTags() {
    $.getJSON('/tags?group=' + group_id,
        function(data,status) {
            var $tags = $('#tags');
            $tags.html('');
            index = 0;
            $.each(data, function(index, entry){
                $span = $('<span class="tag">' + entry + '</span> ')
                $tags.append($span);
                $span.css({
                    'background' : colors[index % 4],
                });
                index += 1;
                console.log(entry);
            });
        });
}


function updateRecommendations() {
    $.getJSON('/recommendations?group=' + group_id,
        function(data,status) {
            index = 0;
            $(".entry").each(function(index) {
                cur_data = data[index];
                $(this).css({
                    'border-left' : '10px solid ' + colors[index % 4],
                    'background' : 'white',
                    'cursor' : 'pointer'
                });
                $(this).unbind();
                var url = cur_data['yelp_url'];
                $(this).click(function() {
                    window.open(url,'_blank');
                });
                output = '<img class="sample" src="' + cur_data['image_url'] + '"/>';
                output += '<div class="rest-wrap">';
                output += '<div class="name">' + cur_data['name'] + '</div>';
                categories = cur_data['categories'];
                categories_output = "";
                $.each(categories, function(index, element) {
                    categories_output += element[0];
                    if (index != categories.length - 1) {
                        categories_output += ', ';
                    }
                });

                output += '<div class="categories">' + categories_output + '</div>';
                output += '</div>';
                $(this).html(output);
                index++;
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
                updateRecommendations();
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
                updateRecommendations();
            },
        });
        return false;
    });
});
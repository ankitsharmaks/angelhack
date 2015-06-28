
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

var cur_z_index = 1;

function updateRecommendations() {
    $.getJSON('/recommendations?group=' + group_id,
        function(data,status) {
            index = 0;
            var $items_to_delete = $('.entry-abs');
            var $recommendations = $('#recommendations');
            for (var i = 0; i < 6; i++) {
                var $new_entry = $('<div class="entry entry-abs"></div>');

                if (index >= data.length) {
                    break;
                }
                cur_data = data[index];
                $new_entry.css({
                    'border-left' : '10px solid ' + colors[index % 4],
                    'background' : 'white',
                    'cursor' : 'pointer',
                    'top' : (100 * i + 1) + 'px',
                    'opacity' : '0',
                    'z-index' : cur_z_index
                });
                //New scope
                (function() {
                    var url = cur_data['yelp_url'];
                    $new_entry.click(function() {
                        window.open(url,'_blank');
                    });
                }());
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
                $new_entry.html(output);

                $recommendations.append($new_entry);
                $new_entry.fadeTo(500, 1);

                index++;
            }
            setTimeout(500, function() {
                $items_to_delete.remove();
            });
            cur_z_index++;
            /*
            $(".entry").each(function(index) {
                if (index >= data.length) {
                    return;
                }
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
            });*/
        });
}

function do_resize() {
    new_width = $(window).width();
    max_width = 1000;
    if (new_width > max_width) {
        new_width = max_width;
    }
    $("#container").css('width', new_width);
    $("#chat").css('width', new_width - 300);
    $("#messages").css('width', new_width - 320);
    $("#tags").css('width', new_width - 20);
    $(".form-wrapper input").css('width', new_width - 420);
}

$(document).ready(function() {
    $(window).resize(function() {
        do_resize();
    });
    do_resize();


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
                    '<span class="user-name">'+evt.message.endpointId+"</span>: " + evt.message.message + "<br>"
                );
                updateMessages();
                setTimeout(updateTags, 1000);
                setTimeout(updateRecommendations, 1000);
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
            '<span class="user-name">'+ endpointId+"</span>: "+ groupMsg + "<br>"
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
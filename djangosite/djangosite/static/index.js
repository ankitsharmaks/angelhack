geolocation = '';

$(document).ready(function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(savePosition);
    }
});

function savePosition(position) {
    geolocation = position.coords.latitude + ',' + position.coords.longitude;
    $('input[name=location]').val(geolocation);
    console.log(geolocation);
}
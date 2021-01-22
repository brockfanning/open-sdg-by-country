$(document).ready(function() {

    $.getJSON('reference-areas.json', function(data) {
        $.each(data, function(key, val) {
            $('.ref-area-select').append("<option value=" + val.id + ">" + val.name + "</li>");
        });
        $('.ref-area-select').select2({
            width: '75%',
        });
    });

    $('#view-button').click(function() {
        var selectedId = $('.ref-area-select').val();
        location.href = selectedId + '/';
    })
});

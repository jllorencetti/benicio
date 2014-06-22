function toggleCheckboxes(parent, childArray) {
    var childCount = childArray.length;
    for (var counter = 0; counter < childCount; counter++) {
        childArray[counter].checked = parent.checked;
    }
}
$('.delete-record').on('click', function () {
    var registerType = $(this).data('registertype');
    var registerId = $(this).attr('id');
    bootbox.confirm('Do you really want to delete this ' + registerType + '? Id: ' + registerId, function (result) {
        if (result) {
            $.ajax({
                type: 'DELETE',
                url: '/api/' + registerType + 's/' + registerId,
                success: function () {
                    location.reload();
                }
            });
        }
    });
});
$('#load-config-button').on('click', function () {
    $.get("/api/current", function (data) {
        $('.current-config')[0].value = data;
    });
});
$('.group-check').on('click', function () {
    var devices = $('[data-group-id="' + $(this)[0].id + '"]');
    toggleCheckboxes(this, devices);
});
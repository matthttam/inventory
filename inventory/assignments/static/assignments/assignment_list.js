$(document).ready(function () {
    $('#assignment_list').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: "/assignments/dt/",
        },
        searchDelay: 350,
        columns: [
            { name: 'person__first_name' },
            { name: 'device__asset_id' },
            { name: 'assignment_datetime' },
            { name: 'return_datetime'},
        ]
    });
});

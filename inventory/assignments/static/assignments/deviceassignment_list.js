$(document).ready(function () {
    $('#assignment_list').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: "/assignments/dt/",
        },
        searchDelay: 350,
        columns: [
            { name: 'id', data: 'id', render:function(data, type, row, meta){
                return '<a href="' + row.id + '/">' + String(data).toLowerCase() + '</a>';
            }},
            { name: 'person_name' },
            { name: 'device__asset_id' },
            { name: 'assignment_datetime' },
            { name: 'return_datetime'},
        ]
    });
});

$(document).ready(function () {
    $('#person_list').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: "/people/dt/",
        },
        searchDelay: 350,
        columns: [
            { name: 'first_name' },
            { name: 'last_name'},
            { 
                name: 'email', 
                data: 'email', 
                render:function(data, type, row, meta){
                    console.log(row)
                    return '<a href="' + row.id + '/">' + data.toLowerCase() + '</a>';
                }
            },
            { name: 'internal_id', data: 'internal_id'},
            { name: 'type__name', data: 'type__name'},
            { name: 'status__name', data: 'status__name'},
            { name: 'building_name_list', data: 'building_name_list', orderable: false},
        ]
    });
});

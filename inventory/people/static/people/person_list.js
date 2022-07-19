// $(document).ready(function () {
//     $('#person_list').DataTable();
// });

$(document).ready(function () {
    $('#person_list').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: "/people/dt/",
        },
        columns: [
            { data: 'first_name', searchable: true},
            { data: 'middle_name', searchable: false},
            { data: 'last_name', searchable: false},
            { data: 'email', searchable: false},
            { data: 'internal_id'},
            { data: 'type__name', searchable: false},
            { data: 'status__name', searchable: false},
            { data: 'building_name_list', orderable: false},
        ]
    });
});

/*,
        "serverSide": true,
        
        */

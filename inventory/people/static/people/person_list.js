// $(document).ready(function () {
//     $('#person_list').DataTable();
// });

$(document).ready(function () {
    $('#person_list').DataTable({
        processing: true,
        serverSide: true,
        ajax: "/people/dt/",
        columns: [
            { data: 'first_name'},
            { data: 'middle_name'},
            { data: 'last_name'},
            { data: 'email'},
            { data: 'internal_id'},
            { data: 'type__name'},
            { data: 'status__name'},
            { data: 'building_name_list'},
        ]
    });
});

/*,
        "serverSide": true,
        
        */

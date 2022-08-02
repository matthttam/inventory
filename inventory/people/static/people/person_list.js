$(document).ready(function () {
    $('#person_list').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: "/people/dt/",
        },
        colReorder: {
            fixedColumnsRight:1
        },
        fixedHeader: true,
        searchDelay: 350,
        columns: [
            { name: 'id', data: 'id', visible: false},
            { name: 'first_name', data: 'first_name' },
            { name: 'last_name', data: 'last_name'},
            { name: 'email', data: 'email'},
            { name: 'internal_id', data: 'internal_id'},
            { name: 'type__name', data: 'type__name'},
            { name: 'status__name', data: 'status__name'},
            { name: 'primary_building__name', data: 'primary_building__name'},
            getActionColumnDef(),
        ]
    });
});

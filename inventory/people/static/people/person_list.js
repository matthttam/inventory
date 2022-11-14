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
            { data: 'id', visible: false},
            { data: 'first_name' },
            { data: 'last_name' },
            { data: 'email' },
            { data: 'internal_id' },
            { data: 'type__name' },
            { data: 'status__name' },
            { data: 'primary_building__name' },
            { data: 'outstanding_assignment_count' },
            { data: 'actions', sortable: false, filterable: false },
        ]
    });
});

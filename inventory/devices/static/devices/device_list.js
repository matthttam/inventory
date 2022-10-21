$(document).ready(function () {
    $('#device_list').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: "/devices/dt/",
        },
        colReorder: {
            fixedColumnsRight:1
        },
        fixedHeader: true,
        searchDelay: 350,
        columnDefs: [
            {
                render: function (data, type, row) {
                    console.log(row)
                    if(data == 1){
                        return '<div class="text-center"><i class="bi bi-check-lg text-success text-center" width="32" height="32"></i></div>'
                    }
                    return '<div class="text-center"><i class="bi bi-x-lg text-danger text-center" width="32" height="32"></i></div>'
                },
                targets: 9,
            }
        ],
        columns: [
            { data: 'id', visible: false },
            { data: 'is_currently_assigned', visible: false },
            { data: 'current_assignment_count', visible: false},
            { data: 'asset_id' },
            { data: 'serial_number' },
            { data: 'status__name' },
            { data: 'device_model__manufacturer__name' },
            { data: 'device_model__name' },
            { data: 'building__name' },
            { data: 'is_google_linked', visible: false, searchable: false },
            { data: 'google_device__organization_unit' },
            { data: 'google_device__most_recent_user', visible: false },
            { data: 'actions', sortable: false, filterable: false },
        ]
    });
});
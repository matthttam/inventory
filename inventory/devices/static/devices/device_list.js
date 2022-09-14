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
        columns: [
            { data: 'id', visible: false},
            { data: 'asset_id'},
            { data: 'serial_number'},
            { data: 'status__name'},
            { data: 'device_model__manufacturer__name'},
            { data: 'device_model__name'},
            { data: 'building__name'},
            { data: 'is_google_linked', visible: false},
            { data: 'google_device__organization_unit'},
            { data: 'google_device__most_recent_user', visible: false},
            getActionColumnDef(),
        ]
    });
});
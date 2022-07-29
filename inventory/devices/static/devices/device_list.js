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
            { name: 'id', data: 'id', visible: false},
            { name: 'asset_id', data: 'asset_id'},
            { name: 'serial_number', data: 'serial_number'},
            getActionColumnDef(),
        ]
    });
});

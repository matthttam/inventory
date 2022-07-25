$(document).ready(function () {
    $('#device_list').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: "/devices/dt/",
        },
        searchDelay: 350,
        columns: [
            { name: 'asset_id' },
            { name: 'serial_number'},
        ]
    });
});

$(document).ready(function () {
    $('#assignment_list').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: "/assignments/dt/",
        },
        colReorder: {
            fixedColumnsRight:1
        },
        fixedHeader: true,
        searchDelay: 350,
        rowId: function(a) {
            return 'deviceassignment_' + a.id;
        },
        columns: [
            { name: 'id', data: 'id', visible: false},
            { name: 'person__internal_id', data: 'person__internal_id', visible: false},
            { name: 'person_name', data: 'person_name' },
            { name: 'person__first_name', data: 'person__first_name', visible: false },
            { name: 'person__last_name', data: 'person__last_name', visible: false },
            { name: 'person__type__name', data: 'person__type__name'},
            { name: 'device_str', data: 'device_str' },
            { name: 'device__asset_id', data: 'device__asset_id', visible: false },
            { name: 'device__serial_number', data: 'device__serial_number', visible: false },
            { name: 'device__device_model__name', data: 'device__device_model__name'},
            { 
                name: 'assignment_datetime', 
                data: 'assignment_datetime',
                render: function(data, type, row, meta){
                    if(!data) return ''
                    return new Date(data).toLocaleDateString()
                }
            },
            { 
                name: 'return_datetime', 
                data: 'return_datetime',
                render: function(data, type, row, meta){
                    if(!data) return ''
                    return new Date(data).toLocaleDateString()
                }
            },
            getActionColumnDef(),
        ]
    });
});

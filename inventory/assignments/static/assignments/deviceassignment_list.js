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
        columns: [
            {
                className: 'dt-control',
                orderable: false,
                data: null,
                defaultContent: '',
            },
            { name: 'id', data: 'id', visible: false},
            { name: 'person_name', data: 'person_name' },
            { name: 'person_type', data: 'person_type' },
            { name: 'device__asset_id', data: 'device__asset_id' },
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

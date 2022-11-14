$(document).ready(function () {
    // $('#assignment_list tfoot th').each( function (i) {
    //     var title = $('#assignment_list thead th').eq( $(this).index() ).text();
    //     $(this).html( '<input type="text" placeholder="'+title+'" data-index="'+i+'" />' );
    // } );

    table = $('#assignment_list').DataTable({
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
            { data: 'id', visible: false},
            { data: 'person__internal_id', visible: false},
            { data: 'person_name' },
            { data: 'person__first_name', visible: false },
            { data: 'person__last_name', visible: false },
            { data: 'person__type__name'},
            { data: 'device_str' },
            { data: 'device__asset_id', visible: false },
            { data: 'device__serial_number', visible: false },
            { data: 'device__device_model__name'},
            {
                data: 'assignment_datetime',
                render: function(data, type, row, meta){
                    if(!data) return ''
                    return new Date(data).toLocaleDateString()
                }
            },
            {
                data: 'return_datetime',
                render: function(data, type, row, meta){
                    if(!data) return ''
                    return new Date(data).toLocaleDateString()
                }
            },
            { 
                name: 'actions', 
                data: 'actions', 
                sortable: false,
                filterable: false,},

        ]
    });

    // Filter event handler
    // $( '#assignment_list' ).on( 'keyup change', 'tfoot input', function () {
    //     table.column( $(this).parent().index()+':visible' )
    //     .search( this.value )
    //     .draw();
    // } );
});

// Configure the defaults for all datatables
$.extend(true, $.fn.dataTable.defaults, {
    dom: `<'row'<'col-sm-4 col-md-2'l><'col-sm-4 col-md-6'B><'col-sm-4 col-md-4'f>>
    <'row'<'col-sm-12'tr>>
    <'row'<'col-sm-12 col-md-3'i><'col-sm-12 col-md-6'p>>`,
    lengthMenu: [
        [ 10, 25, 50, 100, 1000, -1],
        [ '10', '25', '50', '100', '1000', 'All']
    ],
    stateSave: true,
    buttons:{
        dom: {
            button: {
                className: 'btn btn-primary button'
            }
        },
        buttons: [
            {
                extend: 'colvis',
                text: '<i class="bi bi-table pe-1" alt="Column Visibility"></i>',
            },
            {
                extend: 'collection',
                text: '<i class="bi bi-save pe-1" alt="Export Options"></i>',
                buttons:[
                    {
                        extend: 'excel',
                        exportOptions: {
                            columns: ':visible',
                        }
                    },
                    { 
                        extend: 'csv',
                        exportOptions: {
                            columns: ':visible',
                        }
                    },
                    { 
                        extend: 'pdf',
                        exportOptions: {
                            columns: ':visible',
                        }
                    },
                    { 
                        extend: 'print',
                        exportOptions: {
                            columns: ':visible',
                        }
                    },
                ], 

                fade: 200,
                autoClose: true,
            },  
        ],
    },
    responseive: true,
});
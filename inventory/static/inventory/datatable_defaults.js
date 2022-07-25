// Configure the defaults for all datatables
$.extend(true, $.fn.dataTable.defaults, {
    dom: `<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>
    <'row'<'col-sm-12'tr>>
    <'row'<'col-sm-12 col-md-3'i><'col-sm-12 col-md-3'B><'col-sm-12 col-md-6'p>>`,
    buttons:{
        dom: {
            button: {
                className: 'btn btn-primary button'
            }
        },
        buttons: [
                
            {
                extend: 'collection',
                text: '<i class="bi bi-save pe-1"></i>',
                buttons:[
                    'excel',
                    'csv',
                    'pdf',
                    'print',
                ], 
                fade: 200,
                autoClose: true,
            },  
        ],
    },
    responseive: true,
});
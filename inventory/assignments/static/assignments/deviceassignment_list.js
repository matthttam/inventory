function getActionButtons(row){
    const actions = JSON.parse(document.getElementById('actions').textContent);
    console.log(actions)
    action_buttons = 
    `
        <div class="btn-toolbar" role="toolbar" aria-label="Toolbar with button groups">
            <div class="btn-group me-2" role="group" aria-label="First group">
                <a type="button" class="btn btn-primary" alt="view"><i class="bi bi-eye">${row.id}</i></a>
                <a type="button" class="btn btn-primary" alt="edit"><i class="bi bi-pencil">${actions.test}</i></a>
                <a type="button" class="btn btn-primary alt="delete"><i class="bi bi-pencil"></i></a>
            </div>
        </div>
    `
    return action_buttons
}

$(document).ready(function () {
    $('#assignment_list').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: "/assignments/dt/",
        },
        searchDelay: 350,
        columns: [
            { name: 'id', data: 'id', render:function(data, type, row, meta){
                return '<a href="' + row.id + '/">' + String(data).toLowerCase() + '</a>';
            }},
            { name: 'person_name' },
            { name: 'device__asset_id' },
            { name: 'assignment_datetime' },
            { name: 'return_datetime'},
            { 
                name: 'actions', 
                data: 'id', 
                render:function(data, type, row, meta){
                    return getActionButtons(row)
                    //'<a href="' + row.id + '/">' + String(data).toLowerCase() + '</a>';
                }
            },
        ]
    });
});

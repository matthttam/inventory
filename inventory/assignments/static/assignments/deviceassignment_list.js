function getActionButtons(row){
    /**
     * getActionButtons takes a row object.
     * The return value is a string of valid HTML to show action buttons available.
     * A text element with id actions must be present or this will return ""
     * @param {object} - row - Datatable row object
     */
    const actions = JSON.parse(document.getElementById('actions').textContent);
    if(!actions) return ""

    console.log(actions)
    action_buttons = 
    `
        <div class="btn-toolbar" role="toolbar" aria-label="Toolbar with button groups">
            <div class="btn-group me-2" role="group" aria-label="First group">
    `
    if(actions.view.allowed) {
        action_buttons += `<a href="${actions.view.path.replace("__id_placeholder__", row.id)}" type="button" class="btn btn-primary" alt="view"><i class="bi bi-eye"></i></a>`
    }
    if(actions.change.allowed) {
        action_buttons += `<a href="${actions.change.path.replace("__id_placeholder__", row.id)}" type="button" class="btn btn-primary" alt="edit"><i class="bi bi-pencil"></i></a>`
    }
    if(actions.delete.allowed) {
        action_buttons += `<a href="${actions.delete.path.replace("__id_placeholder__", row.id)}" type="button" class="btn btn-primary alt="delete"><i class="bi bi-trash2"></i></a>`
    }
    action_buttons += 
    `
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
                },
                sortable: false,
                filterable: false,
            },
        ]
    });
});

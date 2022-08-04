function getActionButtons(row){
    /**
     * getActionButtons takes a row object.
     * The return value is a string of valid HTML to show action buttons available.
     * A text element with id actions must be present or this will return ""
     * @param {object} - row - Datatable row object
     */
    const actions = JSON.parse(document.getElementById('permitted_actions').textContent);
    if(!actions) return ""

    ActionButtons = 
    `
    <div class="container d-flex justify-content-center">
        <div class="btn-toolbar" role="toolbar" aria-label="Toolbar with button groups">
            <div name='action_buttons' class="btn-group me-2" role="group" aria-label="First group">
    `
    if(actions.view.allowed) {
        ActionButtons += `<a href="${actions.view.path.replace("__id_placeholder__", row.id)}" type="button" class="btn btn-primary" alt="view"><i class="bi bi-eye"></i></a>`
    }
    if(actions.change.allowed) {
        ActionButtons += `<a href="${actions.change.path.replace("__id_placeholder__", row.id)}" type="button" class="btn btn-primary" alt="edit"><i class="bi bi-pencil"></i></a>`
    }
    if(actions.delete.allowed) {
        ActionButtons += `<a href="${actions.delete.path.replace("__id_placeholder__", row.id)}" type="button" class="btn btn-primary alt="delete"><i class="bi bi-trash2"></i></a>`
    }
    ActionButtons += 
    `
            </div>
        </div>
    </div>
    `
    return ActionButtons
}

function getActionColumnDef(){
    return { 
        name: 'actions', 
        data: 'id', 
        render:function(data, type, row, meta){
            return getActionButtons(row)
        },
        sortable: false,
        filterable: false,
        title: '<div class="text-center">Action</div>',
    }
}
function get_ajax_url(key){
    const ajax_urls = JSON.parse(document.getElementById('ajax_urls').textContent);
    return ajax_urls[key]
}

$(document).ready(function() {

    
    function get_person_text(obj){
        text = `${obj.last_name}, ${obj.first_name} - ${obj.internal_id}`
        text += obj.is_active ? "": " (inactive)"
        text += obj.is_currently_assigned ? " (assigned)" : ""
        return text
    }
    function get_device_text(obj){
        text = `${obj.asset_id} (${obj.serial_number})`
        text += obj.is_active ? "": " (inactive)"
        text += obj.is_currently_assigned ? " (assigned)" : ""
        return text
    }

 
    var deviceSelect = $('#device').select2({
        ajax: {
            url: get_ajax_url('devices'),
            delay: 250,
            dataType: 'json',

            processResults: function (data) {                    
                var searchTerm = deviceSelect.data("select2").$dropdown.find("input").val();
                if (
                        data.results.length == 1 && 
                        data.results[0].is_active && 
                        ! data.results[0].is_currently_assigned && 
                        (data.results[0].asset_id.toUpperCase() == searchTerm.toUpperCase() || data.results[0].serial_number.toUpperCase() == searchTerm.toUpperCase())
                    )  {
                    deviceSelect.append($("<option />")
                        .attr("value", data.results[0].id)
                        .html(get_device_text(data.results[0]))
                    ).val(data.results[0].id).trigger("change").select2('close').trigger('select2:select');
                }
                $.map(data.results, function (obj) {
                    obj.text = get_device_text(obj)
                    obj.disabled = ! obj.is_active || obj.is_currently_assigned
                    return obj;
                })
                return data;
            },
        },
        theme: 'bootstrap-5',
        placeholder: 'L######',
        minimumInputLength: 3,
        dropdownParent: $('div[name=device_search]'),
        
    }).focus()
    .select2('open')
    .on('select2:select', function(e) {
        $('#person').focus().select2('open');
    });

    var personSelect = $('#person').select2({
        ajax: {
            url:  get_ajax_url('people'),
            delay: 250,
            dataType: 'json',
            processResults: function (data) {            
                
                var searchTerm = personSelect.data("select2").$dropdown.find("input").val();

                if (
                        data.results.length == 1 && 
                        (data.results[0].internal_id.toUpperCase() == searchTerm.toUpperCase() || data.results[0].email.toUpperCase() == searchTerm.toUpperCase()) &&
                        data.results[0].is_active &&
                        !data.results[0].is_currently_assigned
                    ) {

                    personSelect.append($("<option />")
                        .attr("value", data.results[0].id)
                        .html(get_person_text(data.results[0]))
                    ).val(data.results[0].id).trigger("change").select2('close').trigger('select2:select');
                    $('form').find('[type=submit]').focus()
                    return {'results':[]};
                }
                
                $.map(data.results, function (obj) {
                    obj.text = get_person_text(obj)
                    obj.disabled = ! obj.is_active || obj.is_currently_assigned
                    return obj;
                })
                return data;
            },
        },
        theme: 'bootstrap-5',
        placeholder: "ID, Email, or Name",
        minimumInputLength: 3,
        dropdownParent: $('div[name=person_search]'),
    })


    $(document).on('submit', 'form#check_form', function(e){
        var form = $('form#check_form')
        var form_inputs = $(this).find('select, input')
        var submit_button = $('form').find('[type=submit]')
        // Disable submit button
        submit_button.attr("disabled", true)

        // Perform post
        $.ajax({
            method: "POST",
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            url: get_ajax_url('submit'),
            data: form.serialize(),
        }).done(function(data){
            if(! data.success){
                // Splash fail
                CreateSplash('alert-danger', 'Error saving record. Error Code: ' + data.errors.join(', '));
            }else if(data.success){
                // Splash success
                let splash = CreateSplash('alert-success', 'Record saved!');
                $(splash).delay(1500).fadeOut();
                // Clear fields
                form.find('select').val(null).trigger('change')
                $('#device').select2('open').trigger('select2:open')
            }else{
                CreateSplash('alert-danger', 'The response from the server is invalid.');
            }
        }).fail(function(){
            // Splash unknown error
            CreateSplash('alert-danger', 'An unknown error occurred. Refresh this page to continue.');
            submit_button.attr("disabled", true)
        }).always(function(e){
            // Unlock Submit Button
            submit_button.attr("disabled", false)
        });

        // Prevent Defaults
        e.preventDefault();
        e.stopPropagation();
    });

    function CreateSplash(class_name, message){
        $splash = $(`
            <div name="splash" class="alert alert-dismissible fade show" role="alert">
                <p id="splash_message">${message}</p>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
                </button>
            </div>`);
        $splash.addClass(class_name)
        $('#splash_area').append($splash)
        return $splash
    }
    
});

/*
 * Hacky fix for a bug in select2 with jQuery 3.6.0's new nested-focus "protection"
 * see: https://github.com/select2/select2/issues/5993
 * see: https://github.com/jquery/jquery/issues/4382
 *
 * TODO: Recheck with the select2 GH issue and remove once this is fixed on their side
 */

$(document).on('select2:open', (e) => {
    var id = e.target.id
    $(document.querySelector('div[name='+id+'_search]')).find('input').get(0).focus()
});
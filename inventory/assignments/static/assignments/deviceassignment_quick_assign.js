$(document).ready(function() {

    var personSelect = $('#person').select2({
        ajax: {
            url: 'ajax/users/',
            delay: 250,
            dataType: 'json',
            processResults: function (data) {            
                
                var searchTerm = personSelect.data("select2").$dropdown.find("input").val();
                
                if (
                        data.results.length == 1 && 
                        data.results[0].internal_id == searchTerm && 
                        data.results[0].is_active &&
                        !data.results[0].has_outstanding_assignment
                    ) {
                    console.log('triggered')
                    personSelect.append($("<option />")
                        .attr("value", data.results[0].id)
                        .html(data.results[0].text)
                    ).val(data.results[0].id).trigger("change").select2('close').trigger('select2:select');
                }
                
                $.map(data.results, function (obj) {
                    obj.text = `${obj.last_name}, ${obj.first_name} - ${obj.internal_id}`
                    if(! obj.is_active){
                        obj.disabled = true;
                        obj.text = obj.text + " (inactive)"
                    } 
                    if(obj.has_outstanding_assignment){
                        obj.disabled = true;
                        obj.text = obj.text + " (assigned)"
                    } 
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
/*
    var assetSelect = $('#asset').select2({
        ajax: {
            url: 'ajax/assets.php',
            delay: 250,
            dataType: 'json',

            processResults: function (data) {                    
                var searchTerm = assetSelect.data("select2").$dropdown.find("input").val();
                if (data.results.length == 1 && data.results[0].id == searchTerm) {
                    assetSelect.append($("<option />")
                        .attr("value", data.results[0].id)
                        .html(data.results[0].text)
                    ).val(data.results[0].id).trigger("change").select2('close').trigger('select2:select');
                }
                return data;
            },
        },
        theme: 'bootstrap4',
        placeholder: 'L######',
        minimumInputLength: 3,
        dropdownParent: $('div[name=asset_search]'),
        
    }).focus()
    .select2('open')
    .on('select2:select', function(e) {
        $('#student').focus().select2('open');
    });

    var studentSelect = $('#student').select2({
        ajax: {
            url: 'ajax/users/',
            delay: 250,
            dataType: 'json',
            processResults: function (data) {                    
                var searchTerm = studentSelect.data("select2").$dropdown.find("input").val();
                if (data.results.length == 1 && data.results[0].id == searchTerm) {
                    studentSelect.append($("<option />")
                        .attr("value", data.results[0].id)
                        .html(data.results[0].text)
                    ).val(data.results[0].id).trigger("change").select2('close').trigger('select2:select');
                }
                return data;
            },
        },
        theme: 'bootstrap4',
        placeholder: "ID, Username, or Email",
        minimumInputLength: 3,
        dropdownParent: $('div[name=student_search]'),
    })
    .on('select2:select', function(e) {
        $('#needs_repair').focus();
    });
*/
    $(document).on('submit', 'form#check_form', function(e){
        var form = $('form#check_form')
        var form_inputs = $(this).find('select, input')
        var submit_button = $('form').find('[type=submit]')
        // Disable submit button
        submit_button.attr("disabled", true)

        // Perform post
        $.ajax({
            method: "POST",
            url: "submit.php",
            data: form.serialize(),
        }).done(function(data){
            if(data.status == 'error'){
                // Splash fail
                CreateSplash('alert-danger', 'Error saving record. Error Code: ' + data.error_code);
            }else if(data.status == 'success'){
                // Splash success
                let splash = CreateSplash('alert-success', 'Record saved!');
                $(splash).delay(1500).fadeOut();
                // Clear fields
                form.find('input[type=checkbox]').prop( "checked", false)
                form.find('select').val(null).trigger('change')
                $('#asset').select2('open').trigger('select2:open')
            }else{
                CreateSplash('alert-danger', 'The response from the server is invalid.');
            }
        }).fail(function(){
            // Splash unknown error
            CreateSplash('alert-danger', 'An unknown error occurred.');
        }).always(function(e){
            // Unlock Submit Button
            submit_button.attr("disabled", false)
        });

        // Prevent Defaults
        e.preventDefault();
        e.stopPropagation();
    });

    function CreateSplash(class_name, message){
        $splash = $('\
            <div name="splash" class="alert alert-dismissible fade show" role="alert">\
                <p id="splash_message">'+ message +'</p>\
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
                    <span aria-hidden="true">&times;</span>\
                </button>\
            </div>');
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
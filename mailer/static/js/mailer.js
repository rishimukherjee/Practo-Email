function toggle(source) {
  // Used for selecting/de-selecting email recipients.
  var checkboxes = document.getElementsByName('patientcheck');
  var n = checkboxes.length;
  for(var i=0;i<n;i++) {
    // If selectAll is checked, all are checked else unchecked.
    checkboxes[i].checked = source.checked;
  }
}

function error_html(error){
    // Utility function to generate error message in bootstrap style.
    var errorhtml = " \
    <div class='alert alert-danger alert-dismissable'> \
        <button type='button' class='close' data-dismiss='alert' aria-hidden='true'> \
            &times; \
        </button> \
        <strong> \
            Warning! \
        </strong>";
    errorhtml += error + "</div>";
    return errorhtml;
}

function validate() {
    // Validation function. It is called before
    // Submiting the form.

    // Check if at least 1 recipient is selected.
    var checkedAtLeastOne = false;
    $('input[type="checkbox"]').each(function() {
        if ($(this).is(":checked")) {
            checkedAtLeastOne = true;
        }
    });
    if(!checkedAtLeastOne){
        $('#error').html("");
        $('#error').html(error_html("Select at least one mail recipient."));
        return false;
    }

    // Check if exe file is being sent in mail.
    var file_name = $("#attachment").val();
    var extension = file_name.substr((file_name.lastIndexOf('.') + 1));
    if(extension == 'exe' || extension == 'msi'){
        $('#error').html("");       
        $('#error').html(error_html("Executable file not allowed."));
        return false;
    }

    // Check for correct email format.
    // Regex taken from http://stackoverflow.com/questions/46155/validate-email-address-in-javascript?rq=1
    var email = $('#email').val();
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if(re.test(email) == false){
        $('#error').html("");
        $('#error').html(error_html("Does not seem to be a correct email-id."));
        return false;
    }
    return true;
}

$(document).ready(function($) {
    $(".clickableRow").click(function() {
        // Used for making a row clickable to
        // Show sent mail details in /sent/
        var content = $(this).find('.content').attr('value');
        var patients_json = $(this).find('.patients').attr('value');
        var patients = $.parseJSON(patients_json);
        var sent_html = "<div class='row'><div class='span6'><div><label>Sent to</label><textarea id='patientArea' class='form-control' rows='5'>";
        $.each(patients, function(index, value) {
            sent_html += value + "\n";
        });
        sent_html += "</textarea></div>";
        var msg_html = "<div><label>Message</label><textarea id='messageArea' class='form-control' rows='12' cols='5'>" + content +"</textarea></div></div><div>";
        $('#message').html(sent_html + msg_html);
        $("#patientArea").prop("disabled", true);
        $("#messageArea").prop("disabled", true);
    });
});
import $ from 'jquery'

var activateNoteWidget = function() {
    // Hide and show Notes section
    $('#notes_button').on('click', function() {
        if ($.trim($(this).text()) == 'Hide Notes') {
            $(this).text('Show Notes');
            $('#notes_box').hide();
        } else {
            $(this).text('Hide Notes');
            $('#notes_box').show();
        }
    });
};

var activateFormWidget = function() {
    // Show options based on Quality for student responses
    $('.quality').on('change', function() {
        var current_quality = $(this).val();
        console.log(current_quality);
        if (current_quality == 't') {
            // Junk   - hide other fields
            $(this).parent().parent().parent().next().hide();
        } else {
            // Not Junk  - show other fields
            $(this).parent().parent().parent().next().show();
        }
    });
}; 

var activateGraderSubmitButton = function(callback) {
    $('#graderSubmit').on('click', callback);
};

export {activateFormWidget, activateNoteWidget, activateGraderSubmitButton}
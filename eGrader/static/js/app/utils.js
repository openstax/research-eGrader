import $ from 'jquery'

function getFormData($form){
    let unindexed_array = $form.serializeArray();
    let indexed_array = {};

    $.map(unindexed_array, function(n, i){
        if (n['value']){
            indexed_array[n['name']] = n['value'];
        }

    });

    return indexed_array;
}

function preventCloseOrRefresh(callback) {
    window.onbeforeunload = function(){

        if (typeof(callback) == 'function') {
            callback()
        }

        //var optoutmessage = "By leaving this page, you opt out of the experiment.";
        //alert(optoutmessage);
        return "By leaving or reloading this page, you will stop your grading session.  Are you sure you want to leave the grading session?";
    }
}


export default getFormData

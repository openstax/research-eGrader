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

export default getFormData

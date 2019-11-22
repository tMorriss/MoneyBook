function separate(num){
    return String(num).replace( /(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
}
function unseparate(num) {
    return num.replace(",", "");
}
function unseparate_value(id) {
    var elm = document.getElementById(id);
    elm.value = unseparate(elm.value);
}

function separate_value(id) {
    var elm = document.getElementById(id);
    elm.value = separate(Number(unseparate(elm.value)));
}

function separate_html(id) {
    var elm = document.getElementById(id);
    elm.innerHTML = separate(Number(unseparate(elm.innerHTML)));
}

function delete_value(id) {
    var elm = document.getElementById(id);
    elm.value = "";
}

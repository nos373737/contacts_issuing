setTimeout(function() {var checkbox = document.getElementById('checkbox');
var box = document.getElementById('dpn_second_box');
checkbox.onclick = function() {
    console.log(this);
    if (this.checked) {
        box.style['display'] = 'block';
    } else {
        box.style['display'] = 'none';
    }
};}, 1);
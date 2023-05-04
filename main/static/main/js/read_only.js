Array.prototype.slice.call(document.querySelectorAll('input[type]:not([type="checkbox"]), textarea'),0).forEach(function(elem) {
    elem.setAttribute('readonly', true);
});
Array.prototype.slice.call(document.querySelectorAll('input[type="checkbox"]'),0).forEach(function(elem) {
    elem.setAttribute('onclick', 'return false;');
});
function helperConfirmationCheckboxValidator() {
    const confirmCB = Array.prototype.slice.call(document.querySelectorAll('input[confirm_read="true"]'), 0);
    const confirmCBLabel = confirmCB.map(function (elem) {
        return document.querySelector(`label[for="${elem.id}"]`)
    });
    const form = document.getElementsByTagName('form')[0];
    const inputs = Array.prototype.slice.call(form.querySelectorAll('input'), 0);
    function validityCB(elem) {
        return elem.validity.valid;
    }
    document.getElementById('submit-button').addEventListener('click', function (evt) {
        evt.preventDefault();
        confirmCB.map(function (elem, i) {
            if (!elem.validity.valid) {
                elem.classList.add('is-danger');
                elem.classList.add('has-background-color');
                confirmCBLabel[i].classList.add('has-text-danger');
            } else {
                elem.classList.remove('is-danger');
                elem.classList.remove('has-background-color');
                confirmCBLabel[i].classList.remove('has-text-danger');
            }
        });
        if (confirmCB.every(validityCB) && inputs.every(validityCB)) {
            form.submit()
        }
    });
}
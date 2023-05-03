function prepend0(val, len) {
    str = String(val)
    while (str.length < len) {
        str = '0' + str;
    }
    return str
}

const now = new Date();
const yearUTC = prepend0(now.getUTCFullYear(), 4);
const monthUTC = prepend0(now.getUTCMonth()+1, 2);
const dayUTC = prepend0(now.getUTCDate(), 2);

const formattedDates = [yearUTC, monthUTC, dayUTC].join('-');

const dateInputs = document.querySelectorAll('input[type="date"]');
dateInputs.forEach(e => {
    e.value = formattedDates
});
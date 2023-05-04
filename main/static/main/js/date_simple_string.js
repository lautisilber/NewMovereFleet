Date.prototype.simpleString = function() {
    function prepend0(val, len) {
        str = String(val)
        while (str.length < len) {
            str = '0' + str;
        }
        return str
    }
    const yearUTC = prepend0(this.getUTCFullYear(), 4);
    const monthUTC = prepend0(this.getUTCMonth()+1, 2);
    const dayUTC = prepend0(this.getUTCDate(), 2);
    return [yearUTC, monthUTC, dayUTC].join('-');
}

Date.fromSimpleString = function(str) {
    const split = str.split("-");
    return new Date(split[0], split[1] - 1, split[2]);
}
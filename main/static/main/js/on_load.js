function onLoad(cb) {
    if(window.addEventListener) {
        window.addEventListener('load', () => {cb()}); //W3C
    } else {
        window.attachEvent('onload', () => {cb()}); //IE
    }
}
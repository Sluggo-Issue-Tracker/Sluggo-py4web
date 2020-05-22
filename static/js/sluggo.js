sluggo = {}

sluggo.formatDate = (date) => { // consistent date formatting
    return date.toLocaleDateString('default', {weekday: 'long'})
    + ", " + date.toLocaleDateString('default', {month: 'long', day: 'numeric', year: 'numeric'})
    + ".";
}

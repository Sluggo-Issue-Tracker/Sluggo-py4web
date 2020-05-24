sluggo = {}

sluggo.formatDate = (date) => { // consistent date formatting
    return date.toLocaleDateString('default', {weekday: 'long'})
    + ", " + date.toLocaleDateString('default', {month: 'long', day: 'numeric', year: 'numeric'})
    + ".";
}

sluggo.placeholder = () => {
    alert("This has not been implemented yet.");
}
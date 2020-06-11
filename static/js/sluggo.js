sluggo = {}

sluggo.formatDate = (date) => { // consistent date formatting
    return date.toLocaleDateString('default', {weekday: 'long'})
    + ", " + date.toLocaleDateString('default', {month: 'long', day: 'numeric', year: 'numeric'});
}

sluggo.placeholder = () => {
    alert("This has not been implemented yet.");
}

sluggo.capitalizeString = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

sluggo.isOverdue = (dueDate) => {
    // get current date
    let currDateTime = new Date(new Date().toDateString());
    // round due date 
    let fixedDueDate = new Date(new Date(dueDate).getTime() + (new Date()).getTimezoneOffset()*60*1000)

    let difference = currDateTime.getTime() - fixedDueDate.getTime();
    
    console.log(difference);

    return (difference > 0);
}

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


sluggo.checkTagsList = (tag_list) => {

    if(tag_list.length === 0) {
        return true;
    }

    let patt = /^[\w]+$/;

    let matches = tag_list.filter((e) => e.match(patt));


    if(matches.length < tag_list.length) {
        return false;
    }

    return true;
};


sluggo.checkTagsString = (tag) => {

    if(tag.length === 0) {
        return true;
    }

    let patt = /^[\w]+$/;

    let matches = patt.test(tag);


    if(!matches) {
        return false;
    }

    return true;
};




sluggo.checkNameString = (name) => {

    if(name.length === 0) {
        return true;
    }

    let patt = /^[\w ]+$/;

    let matches = patt.test(name);


    if(!matches) {
        return false;
    }

    return true;
};

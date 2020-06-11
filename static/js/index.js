// index.js - Vue/JavaScript code for homepage

app = {};

app.data = {
    formatted_date: "a new day",
    pinned_tickets: [], // this is to be replaced by data passed in by py4web
    priority_tickets: [],
    user_tags: [],
    user_tags: [],
    recent_events: [],
    assigned_tickets_count: assigned_tickets_count,
    approved: approved  == "True"
}

app.setFormattedDate = () => {
    app.data.formatted_date = sluggo.formatDate(new Date(date));
}

app.placeholder = () => {
    sluggo.placeholder();
}

app.goToTicket = (ticket_id) => {
    // redirect to the ticket details page
    window.location.href = ticket_details_url + "/" + ticket_id;
}

app.formatTag = (tag_str) => {
    return sluggo.capitalizeString(tag_str);
}

app.goToTag = (tag_id) => {
    window.location.href = tickets_url + "?tag_id=" + tag_id
}

app.formatDate = (date) => {
    console.log(date);
    if(typeof(date) !== "undefined" && date !== null) {
        return sluggo.formatDate(new Date(date));
    } else {
        return "";
    }
}

app.formatBadDate = (badDate) => {
    // this is for formatting non whole dates
    // i hate javascript and dates with a burning passion
    // the likes of which will never be satiated
    // it carves away at my very being 
    // for all time

    console.log(date);
    if(typeof(date) !== "undefined" && date !== null) {
        return sluggo.formatDate(new Date(new Date(badDate).getTime() + (new Date()).getTimezoneOffset()*60*1000));
    } else {
        return "";
    }
}

app.fixDate = (date) => {
    return date + new Date().getTimezoneOffset();
}

app.checkOverdue = (webTicket) => {
    if(webTicket.due === null) {
        return false;
    }
    // else we parse the web due
    let webTicketDue = new Date(webTicket.web_due);

    return sluggo.isOverdue(webTicketDue);
}

app.checkStarted = (webTicket) => {
    return !(webTicket.started === null);
}

app.checkCompleted = (webTicket) => {
    return (webTicket.completed !== null);
}

app.goToSelfAssignee = () => {
    window.location.href = tickets_url + "?assignee_id=" + user_id;
}

app.fetchEventIconForEvent = (event) => {
    return axios.get(get_icons_url + '?id=' + event.action_user).then((response) => {
        console.log(response);
        Vue.set(event, "image", response.data.imgbytes);
    })
}

app.unpinTicket = (pinnedTicket) => {
    Vue.set(app.data, "pinned_tickets", app.data.pinned_tickets.filter(pt => pt.id !== pinnedTicket.id));
    axios.post(pin_ticket_url, {
        ticket_id: pinnedTicket.id
    });
}

app.methods = {
    setFormattedDate: app.setFormattedDate,
    placeholder: app.placeholder,
    goToTicket: app.goToTicket,
    formatTag: app.formatTag,
    goToTag: app.goToTag,
    formatDate: app.formatDate,
    checkOverdue: app.checkOverdue,
    goToSelfAssignee: app.goToSelfAssignee,
    checkStarted: app.checkStarted,
    checkCompleted: app.checkCompleted,
    unpinTicket: app.unpinTicket,
    formatBadDate: app.formatBadDate
}

app.vm = new Vue({
    el: '#hp-target',
    data: app.data,
    methods: app.methods
});

app.init = () => {
    app.setFormattedDate();

    // Add the pinned tickets from the passed date
    Vue.set(app.data, "pinned_tickets", JSON.parse(pinned_tickets));

    // Add the priority tickets from the passed data
    Vue.set(app.data, "priority_tickets", JSON.parse(priority_tickets));

    // Add the user tags from the passed user tags
    Vue.set(app.data, "user_tags", JSON.parse(user_tags));

    Vue.set(app.data, "recent_events", JSON.parse(recent_events));
    for(event of app.data.recent_events) {
        // make a request
        app.fetchEventIconForEvent(event);
    }
}

app.init();

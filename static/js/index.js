// index.js - Vue/JavaScript code for homepage

app = {};

app.data = {
    formatted_date: "a new day",
    pinned_tickets: [], // this is to be replaced by data passed in by py4web
    priority_tickets: [],
    user_tags: []
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

app.methods = {
    setFormattedDate: app.setFormattedDate,
    placeholder: app.placeholder,
    goToTicket: app.goToTicket,
    formatTag: app.formatTag,
    goToTag: app.goToTag,
    formatDate: app.formatDate
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
}

app.init();
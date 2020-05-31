// index.js - Vue/JavaScript code for homepage

app = {};

app.data = {
    formatted_date: "a new day",
    pinned_tickets: [] // this is to be replaced by data passed in by py4web
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

app.methods = {
    setFormattedDate: app.setFormattedDate,
    placeholder: app.placeholder,
    goToTicket: app.goToTicket
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
}

app.init();
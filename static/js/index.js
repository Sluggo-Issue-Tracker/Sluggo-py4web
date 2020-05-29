// index.js - Vue/JavaScript code for homepage

app = {};

app.data = {
    formatted_date: "a new day"
}

app.setFormattedDate = () => {
    app.data.formatted_date = sluggo.formatDate(new Date(date));
}

app.placeholder = () => {
    sluggo.placeholder();
}

app.getPinnedTickets = () => {
    axios.get(get_pinned_tickets_url);
}

app.methods = {
    setFormattedDate: app.setFormattedDate,
    placeholder: app.placeholder,
    getPinnedTickets: app.getPinnedTickets
}

app.vm = new Vue({
    el: '#hp-target',
    data: app.data,
    methods: app.methods
});

app.init = () => {
    app.setFormattedDate();
    app.getPinnedTickets();
}

app.init();
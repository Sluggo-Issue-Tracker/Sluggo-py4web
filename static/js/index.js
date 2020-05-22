// index.js - Vue/JavaScript code for homepage

const DATES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

app = {};

app.data = {
    formatted_date: "a new day"
}

app.setFormattedDate = () => {
    app.data.formatted_date = sluggo.formatDate(new Date(date));
}

app.methods = {
    setFormattedDate: app.setFormattedDate
}

app.vm = new Vue({
    el: '#hp-target',
    data: app.data,
    methods: app.methods
});

app.init = () => {
    app.setFormattedDate();
}

app.init();
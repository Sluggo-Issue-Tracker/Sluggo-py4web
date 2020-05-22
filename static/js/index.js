// index.js - Vue/JavaScript code for homepage

const DATES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

app = {};

app.data = {
    formatted_date: "a new day"
}

app.setFormattedDate = () => {
    const jsDate = new Date(date)
    app.data.formatted_date = jsDate.toLocaleDateString('default', {weekday: 'long'})
        + ", " + jsDate.toLocaleDateString('default', {month: 'long', day: 'numeric', year: 'numeric'})
        + ".";
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
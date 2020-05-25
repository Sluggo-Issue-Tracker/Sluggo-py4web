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

app.methods = {
    setFormattedDate: app.setFormattedDate,
    placeholder: app.placeholder
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
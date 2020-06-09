
// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    app.data = {
        page: "start_view",
    };

    app.reindex = (a) => {
        let idx = 0;
        for (p of a) {
            p._idx = idx++;
        }
        return a;
    };

    app.goto = (page) => {
        app.data.page = page;
    };

    app.methods = {
        goto : app.goto
    };

    app.vue = new Vue({
        el: "#help-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
        
    };

    app.init();
};

init(app);

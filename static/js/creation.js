Vue.component('v-select', VueSelect.VueSelect);

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        username: username,
        selected: [],
        bio_text: "",
        options: tags,
        bio_empty: false,
        tag_empty: false,
        admin: admin === "True" ? true : false,

        // Complete.
    };

    app.add_user = () => {

        if (app.data.admin === true && app.data.selected.length == 0) {
            app.data.tag_empty = true;
            return;
        }

        if(app.data.bio_text.trim().length !== 0) {
            axios.post(add_user_url, {
                bio: app.data.bio_text,
                tags: app.data.selected
            }).then(() => {
                window.location.href = "../index";
            });
        }
        else {
            app.data.bio_empty = true;
        }
    };



    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        add_user: app.add_user,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

   app.init = () => {

    };




    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);



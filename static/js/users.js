Vue.component('v-select', VueSelect.VueSelect);
// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        user_email: user_email,
        username: username,
        users: [],
        master: [],
        searchText: "",

        // Complete.
    };
    // Use this function to reindex the posts, when you get them, and when
    // you add / delete one of them.
    app.reindex = (a) => {
        let idx = 0;
        for (p of a) {
            p._idx = idx++;
        }
        return a;
    };

    app.show_user = (user_index) => {
        let user = app.data.users[user_index];
        if(user !== false) {
            window.location.href = "../users/" + user.id;
        }
    };


    app.filter_list = () => {
        app.data.users = app.data.master.filter((user) => {
            return user.full_name.toLowerCase().includes(app.data.searchText.trim().toLowerCase()) ||
                   user.role.toLowerCase().includes(app.data.searchText.trim().toLowerCase()) ||
                   user.bio.toLowerCase().includes(app.data.searchText.trim().toLowerCase()) ||
                   user.tags_list.filter(v => v.toLowerCase().includes(app.data.searchText.trim().toLowerCase())).length > 0;
        });
    };

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        show_user: app.show_user,
        filter_list: app.filter_list,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-users",
        data: app.data,
        methods: app.methods
    });

  app.init = () => {
        axios.get(get_users_url).then((result) => {
            var user_promises = [];
            let users = result.data.users;
            app.data.options = result.data.tags;
            app.reindex(users);
            for (let user of users) {
                let user_el = user;
                Vue.set(user_el, 'url', user["icon"]);
                app.data.users.push(user_el);
            }
            app.data.master = app.data.users;
        });
    };

    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);

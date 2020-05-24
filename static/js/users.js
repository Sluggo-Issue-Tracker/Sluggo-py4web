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
        page: 'list',
        current_user: {},
        options: [],
        searchText: "",
        is_pending: false,
        error: false,
        success: false,

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

    app.goto = (destination) => {
        app.data.page = destination;
        if(destination === "list") {
            app.data.current_user = {};
        }
        // app.data.add_post_text = "";
    };

    app.show_user = (user_index) => {
        let user = app.data.users[user_index];
        if(user !== false) {
            axios.get(show_user_url, { id: user.id })
            .then((response) => {

            });
        }
        app.goto('user');
    };

    app.checkUser = () => {
        return app.data.user_email == app.data.current_user.user_email;
    };

    app.filter_list = () => {
        app.goto('list');
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
        goto: app.goto,
        show_user: app.show_user,
        checkUser: app.checkUser,
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
                // We create an element in the images data structure.
                // Note: it is SUPER important here to have the url attribute
                // of img_el already defined.
                let user_el = user;
                app.data.users.push(user_el);
                // We create a promise for when the image loads.
                let p = axios.get(
                    get_icon_url,
                    {params: {"img": user["icon"]}}).then((result) => {
                    // Puts the image URL.
                    // See https://vuejs.org/v2/guide/reactivity.html#For-Objects
                    Vue.set(user_el, 'url', result.data.imgbytes);
                    return "ok";
                });
                user_promises.push(p);
            }
            app.data.master = app.data.users;
            Promise.all(user_promises).then((r) => {
                    app.data.done = "All done";
                    console.log(r);
            });
        });
    };




    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);

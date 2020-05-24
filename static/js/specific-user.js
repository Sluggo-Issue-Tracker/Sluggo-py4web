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
        id: id,

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

    app.resetCurrent = () => {
        app.show_user(app.data.current_user._idx);
    };


    app.updateCurrent = () => {
        let user = app.data.current_user;

        if(user !== false) {
            app.data.is_pending = true;
            axios.post(edit_user_url, { bio : user.bio,
                                        role : user.role,
                                        tags_list : user.tags_list,
                                        full_name : user.full_name,
                                        id : user.id })
            .then((response) => {
                let old_user = app.data.users[user._idx];
                app.data.is_pending = false;
                app.show_value(false);
                old_user.bio = user.bio,
                old_user.full_name = user.full_name,
                old_user.url = user.url,
                old_user.role = user.role,
                old_user.tags_list = user.tags_list,
                old_user.user_email = user.user_email

                app.reindex(app.data.users);
            }).catch((error) => {
                console.log(error);
                app.show_value(true);
            });
        }
    };


    app.sleep = (ms) => {
            return function (x) {
                return new Promise(resolve => setTimeout(() => resolve(x), ms));
            };
        }

    app.show_value = (flag) => {
        // Flashes an error if an error occurred.

        if(flag === true) {
            app.data.error = true;
            app.data.success = false;
        }
        else {
            app.data.error = false;
            app.data.success = true;
        }
        app.data.is_pending = false;
        app.sleep(1000)()
            .then(() => {
                app.data.error = false;
                app.data.success = false;
            });
    }

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
        updateCurrent: app.updateCurrent,
        resetCurrent: app.resetCurrent,
        checkUser: app.checkUser,
        filter_list: app.filter_list,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-user",
        data: app.data,
        methods: app.methods
    });

  app.init = () => {
        axios.get(show_user_url, {params: {"id": id).then((result) => {

            let current_user = result.data.users;
            app.data.options = result.data.tags;
            let p = axios.get(
                    get_icon_url,
                    {params: {"img": user["icon"]}}).then((result) => {
                    // Puts the image URL.
                    // See https://vuejs.org/v2/guide/reactivity.html#For-Objects
                    Vue.set(user_el, 'url', result.data.imgbytes);
                    return "ok";
                });
            app.data.master = app.data.users;
        });
    };




    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);

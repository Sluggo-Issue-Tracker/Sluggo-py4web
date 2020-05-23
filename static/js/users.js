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
        page: 'list',
        current_user: {},
        current_name: "",
        current_tag: [],
        current_bio: "",
        options: [],

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
        app.vue.page = destination;
        // app.vue.add_post_text = "";
    };

    app.show_user = (user_index) => {
        let user = app.vue.users[user_index];
        if(user !== false) {
            app.data.current_user = {
                _idx: user._idx,
                id: user.id,
                bio: user.bio,
                full_name: user.full_name,
                url: user.url,
                role: user.role,
                tags_list: user.tags_list,
                user_email: user.user_email
            };
        }
        app.goto('user');
    };


    app.resetCurrent = () => {
        app.show_user(app.vue.current_user._idx);
    };


    app.updateCurrent = () => {
        let user = app.data.current_user;

        if(user !== false) {

            axios.post(edit_user_url, { bio : user.bio,
                                        role : user.role,
                                        tags_list : user.tags_list,
                                        full_name : user.full_name,
                                        id : user.id }).then((response) => {
                let old_user = app.data.users[user._idx];

                old_user.bio = user.bio,
                old_user.full_name = user.full_name,
                old_user.url = user.url,
                old_user.role = user.role,
                old_user.tags_list = user.tags_list,
                old_user.user_email = user.user_email

                app.reindex(app.data.users);
            }).catch((error) => {
                console.log(error);
            });
        }
    };

    app.checkUser = () => {
        return app.vue.user_email == app.vue.current_user.user_email;
    };


    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        goto: app.goto,
        show_user: app.show_user,
        updateCurrent: app.updateCurrent,
        resetCurrent: app.resetCurrent,
        checkUser: app.checkUser,
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
            app.vue.options = result.data.tags;
            app.reindex(users);
            for (let user of users) {
                // We create an element in the images data structure.
                // Note: it is SUPER important here to have the url attribute
                // of img_el already defined.
                let user_el = user;
                app.vue.users.push(user_el);
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
            Promise.all(user_promises).then((r) => {
                    app.vue.done = "All done";
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

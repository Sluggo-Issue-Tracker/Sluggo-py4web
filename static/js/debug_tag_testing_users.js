Vue.component('v-select', VueSelect.VueSelect);
// This will be the object that will contain the Vue attributes
// and be used to usersInitialize it.
let usersApp = {};

// Given an empty usersApp object, usersInitializes it filling its attributes,
// creates a Vue instance, and then usersInitializes the Vue instance.
let usersInit = (usersApp) => {

    // This is the Vue data.
    usersApp.data = {
        user_email: user_email,
        username: username,
        users: [],
        page: 'list',
        current_user: {},
        options: [],
        is_pending: false,
        error: false,
        success: false,

        // Complete.
    };
    // Use this function to reindex the posts, when you get them, and when
    // you add / delete one of them.
    usersApp.reindex = (a) => {
        let idx = 0;
        for (p of a) {
            p._idx = idx++;
        }
        return a;
    };

    usersApp.goto = (destination) => {
        usersApp.vue.page = destination;
        // usersApp.vue.add_post_text = "";
    };

    usersApp.show_user = (user_index) => {
        let user = usersApp.vue.users[user_index];
        if(user !== false) {
            usersApp.data.current_user = {
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
        usersApp.goto('user');
    };


    usersApp.resetCurrent = () => {
        usersApp.show_user(usersApp.vue.current_user._idx);
    };


    usersApp.updateCurrent = () => {
        let user = usersApp.data.current_user;

        if(user !== false) {
            usersApp.vue.is_pending = true;
            axios.post(edit_user_url, { bio : user.bio,
                                        role : user.role,
                                        tags_list : user.tags_list,
                                        full_name : user.full_name,
                                        id : user.id })
            .then((response) => {
                let old_user = usersApp.data.users[user._idx];
                usersApp.vue.is_pending = false;
                usersApp.show_value(false);
                old_user.bio = user.bio,
                old_user.full_name = user.full_name,
                old_user.url = user.url,
                old_user.role = user.role,
                old_user.tags_list = user.tags_list,
                old_user.user_email = user.user_email

                usersApp.reindex(usersApp.data.users);
            }).catch((error) => {
                console.log(error);
                usersApp.show_value(true);
            });
        }
    };


    usersApp.sleep = (ms) => {
            return function (x) {
                return new Promise(resolve => setTimeout(() => resolve(x), ms));
            };
        }

    usersApp.show_value = (flag) => {
        // Flashes an error if an error occurred.

        if(flag === true) {
            usersApp.vue.error = true;
            usersApp.vue.success = false;
        }
        else {
            usersApp.vue.error = false;
            usersApp.vue.success = true;
        }
        usersApp.vue.is_pending = false;
        usersApp.sleep(1000)()
            .then(() => {
                usersApp.vue.error = false;
                usersApp.vue.success = false;
            });
    }

    usersApp.checkUser = () => {
        return usersApp.vue.user_email == usersApp.vue.current_user.user_email;
    };


    // We form the dictionary of all methods, so we can assign them
    // to the Vue usersApp in a single blow.
    usersApp.methods = {
        goto: usersApp.goto,
        show_user: usersApp.show_user,
        updateCurrent: usersApp.updateCurrent,
        resetCurrent: usersApp.resetCurrent,
        checkUser: usersApp.checkUser,
    };

    // This creates the Vue instance.
    usersApp.vue = new Vue({
        el: "#vue-users",
        data: usersApp.data,
        methods: usersApp.methods
    });

  usersApp.usersInit = () => {
        axios.get(get_users_url).then((result) => {
            var user_promises = [];
            let users = result.data.users;
            usersApp.vue.options = result.data.tags;
            usersApp.reindex(users);
            for (let user of users) {
                // We create an element in the images data structure.
                // Note: it is SUPER important here to have the url attribute
                // of img_el already defined.
                let user_el = user;
                usersApp.vue.users.push(user_el);
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
                    usersApp.vue.done = "All done";
                    console.log(r);
            });
        });
    };




    // Call to the usersInitializer.
    usersApp.usersInit();
};

// This takes the (empty) usersApp object, and usersInitializes it,
// putting all the code i
usersInit(usersApp);


// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    app.data = {
        users: [],
        all_users: [],
        is_pending: false,
        page: "approve"


    };


    app.reindex = (a) => {
        let idx = 0;
        for (p of a) {
            p._idx = idx++;
        }
        return a;
    };

    app.updateRoles = (user_index, value, table) => {

        let user = table === 'all' ?
            app.data.all_users[user_index] : app.data.users[user_index];

        if (user.role === value) return;
        user.role = value;
        axios.post(set_role_url, {
                                id: user.id,
                                role: user.role })
        .then((response) => {
            app.init();
        }).catch((error) => {
            console.log(error);
            app.show_value(true);
        });
    };

    app.goto = (page) => {
        app.data.page = page;
    };

    app.methods = {
        updateRoles: app.updateRoles,
        goto : app.goto,

    };


    app.vue = new Vue({
        el: "#vue-admin",
        data: app.data,
        methods: app.methods
    });


    app.init = () => {
        axios.get(get_unapproved_users_url).then((result) => {
            let users = result.data.users;
            app.reindex(users);
            app.data.users = users;
        });

        axios.get(get_users_url).then((result) => {
            let users = result.data.users;
            users.sort((a,b) => (a.role > b.role) ? 1 : ((b.role > a.role) ? -1 : 0));
            app.reindex(users);
            app.data.all_users = users;
        });



    };

    app.init();
};

init(app);

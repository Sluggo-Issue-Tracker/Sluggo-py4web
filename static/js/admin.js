
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
        page: "start_view",
        tags: [],
        all_tags: [],
        add_tag_text: "",
        length_check: false,
        user_email : user_email,

    };


    app.reindex = (a) => {
        let idx = 0;
        for (p of a) {
            p._idx = idx++;
            p.edited = false;
            p.dirty = "";
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
        }).catch((error) => {
            console.log(error);
        });
    };


    app.approveTags = (tag_index, value, table) => {

        let tag = table === 1 ?
            app.data.all_tags[tag_index] : app.data.tags[tag_index];

        if (tag.approved === value) return;
        tag.approved = value
        axios.post(set_tag_url, {
                                id: tag.id,
                                approved: tag.approved })
        .then((response) => {
            axios.get(get_unapproved_tags_url).then((result) => {
                let tags = result.data.tags;
                app.reindex(tags);
                app.data.tags = tags;
            });

            axios.get(get_tags_url).then((result) => {
                let tags = result.data.tags;
                tags.sort((a,b) => (a.approved > b.approved) ? 1 : ((b.approved > a.approved) ? -1 : 0));
                app.reindex(tags);
                app.data.all_tags = tags;
            });
        }).catch((error) => {
            console.log(error);
        });
    };

    app.deleteTag = (tag_index) => {

        let tag = app.data.all_tags[tag_index] ;

        axios.post(del_tag_url, {
                                id: tag.id })
        .then((response) => {
            axios.get(get_unapproved_tags_url).then((result) => {
                let tags = result.data.tags;
                app.reindex(tags);
                app.data.tags = tags;
            });

            axios.get(get_tags_url).then((result) => {
                let tags = result.data.tags;
                tags.sort((a,b) => (a.approved > b.approved) ? 1 : ((b.approved > a.approved) ? -1 : 0));
                app.reindex(tags);
                app.data.all_tags = tags;
            });
        }).catch((error) => {
            console.log(error);
        });
    };

    app.editTag = (tag_index) => {

        let tag = app.data.all_tags[tag_index];
        tag.dirty = tag.tag_name; // Store old tag value as a dirty element
        tag.edited = true;

    };

    app.saveTag = (tag_index) => {

        let tag = app.data.all_tags[tag_index];
        let value = tag.tag_name;
        if (value.trim() === tag.dirty.trim()) {
            tag.dirty = "";
            tag.edited = false;
            return;
        }

        axios.post(edit_tag_url, {
                                    id: tag.id,
                                    val: value})
        .then((response) => {
            tag.dirty = "";
            tag.edited = false;
        });

    };

    app.addTag = () => {

        let val = app.data.add_tag_text;
        if(val.trim().length === 0) {
            app.data.length_check = true;
            return;
        }
        app.data.length_check = false;

        app.data.text_check = false;

        axios.post(add_tag_url, {
            tag_text: val,
        }).then((result) => {
            if (result.data.id == null) {
                app.data.add_tag_text = "";
                return;
            }
            app.data.all_tags.unshift({
                id: result.data.id,
                tag_name: val,
                approved: true,
            });
            app.reindex(app.data.all_tags);
            app.data.add_tag_text = "";
        }).catch((error) => {
            console.log(error);
        });

    };


    app.cancelEdit = (tag_index) => {

        let tag = app.data.all_tags[tag_index];
        tag.tag_name = tag.dirty;
        tag.edited = false;
    };


    app.goto = (page) => {
        app.data.page = page;
    };

    app.gotoBiosExport = () => {
        console.log(bios_export_url);
        window.location.href = bios_export_url;
    }


    app.getColor = (user_index) => {
        let user = app.data.all_users[user_index];

        if (user.role === "Admin")
            return 'has-text-success';

        else if (user.role === "Approved")
            return 'has-text-info';

        return 'has-text-danger';
    };

    app.methods = {
        updateRoles: app.updateRoles,
        approveTags: app.approveTags,
        goto : app.goto,
        getColor : app.getColor,
        deleteTag : app.deleteTag,
        gotoBiosExport: app.gotoBiosExport,
        editTag : app.editTag,
        cancelEdit : app.cancelEdit,
        saveTag : app.saveTag,
        addTag : app.addTag,
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

        axios.get(get_unapproved_tags_url).then((result) => {
            let tags = result.data.tags;
            app.reindex(tags);
            app.data.tags = tags;
        });

        axios.get(get_tags_url).then((result) => {
            let tags = result.data.tags;
            tags.sort((a,b) => (a.approved > b.approved) ? 1 : ((b.approved > a.approved) ? -1 : 0));
            app.reindex(tags);
            app.data.all_tags = tags;
        });
    };

    app.init();
};

init(app);

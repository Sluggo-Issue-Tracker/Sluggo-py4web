Vue.component('v-select', VueSelect.VueSelect);


// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

/** Sam's thoughts
 * title, description, and tags are the only places where we want to confirm our changes
 * progress, assignment, and subtickets can be registered instantly
 */


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        ticket : {}, // this is the main data object
        // fields to visually represent the current ticket --------------------------------------
        ticket_id: "",
        title: "",
        description: "",
        author: "",
        status: "",
        // data used by input
        new_ticket: {},
        selected_tags: [],
        current_status: "",
        assigned: "No one has been assigned", // going to be the string for the assigned user
        // represents values allowed by the backend
        tag_options: [],
        status_strings: [],
        possible_users: [],
        // control ------------------------------------------------------------------------------
        edit: false,
        show_modal: false,
        color_class: {
            0: "is-link",
            1: "is-warning",
            2: "is-success"
        }
    };

    app.pre_add = () => {
        app.data.new_ticket = { // object that the modal uses
            id: "",
            ticket_title: "",
            ticket_description: "",
            ticket_author: "",
            created: "",
            started: "",
            completed: "",
            tag_list: [],
            sub_tickets: [],
            parent_id: app.data.ticket.id,
            status: 0,
        };
        app.data.show_modal = true;
    };

    /**
     * uses the value newly generated from the submitted modal
     */
    app.add_ticket = () => {
        axios.post(add_sub_ticket_url, app.data.new_ticket).then((response) => {
           app.data.ticket.sub_tickets.unshift(response.data.ticket);
        }).catch((error) => {
            console.log(error);
        });
        app.close_modal();
    };

    /**
     * close modal and assign new_ticket to empty object
     */
    app.close_modal = () => {
        app.data.show_modal = false;
        app.data.new_ticket = {};
    };

    /**
     * this should do a post request to register the assignment of a ticket
     * @param user
     */
    app.assign_user= (user) => {
        // TODO: implement this
    };

    /**
     * redirect t
     * @param id
     */
    app.redirect_ticket = (id) => {
        window.location.href = tickets_details_url + '/' + id;
    };

    /**
     * resets the fields to their previous value kept track in ticket object
     */
    app.cancel_edit = () => {
        app.data.edit = false;
    };

    /**
     * submits the modified values to the backend
     * on success, updates the displayed values
     */
    app.submit_edit = () => {
        if(app.data.ticket === null)
            return;
        axios.post(edit_ticket_url, {
            id: app.data.ticket_id,
            title: app.data.title,
            text: app.data.description,
            tag_list: app.data.selected_tags,
        }).then((response) => {
            return axios.post(get_users_by_tag_list_url, {tag_list: app.data.selected_tags})
        }).then((result) => {
            app.data.possible_users = app.reindex(result.data.users);
        }).catch((error) => {
            console.log(error);
        });

        app.data.edit = false;
    };

    /**
     * called by v-select on selection of the status
     */
    app.change_status = () => {
        if(app.data.status === null)
            return;

        axios.post(update_progress_url, {
            ticket_id: app.data.ticket.id,
            status: app.data.current_status
        }).then((response) => {
            app.data.status = response.data.status;
            app.data.current_status = response.data.status;
        }).catch((error) => {
            console.log(error);
        });
    };

    app.set_fields = (ticket_object) => {
        app.data.ticket_id = ticket_object.id;
        app.data.title = ticket_object.ticket_title;
        app.data.description = ticket_object.ticket_text;
        app.data.author = ticket_object.ticket_author;
        app.data.status = ticket_object.status;
        app.data.current_status = app.data.status;
    };

    /**
     *
     * @param list
     * @returns {*}
     */
    app.reindex = (list) => {
        let i = 0;
        for(let l of list) {
            l._idx = i++;
            l.label = l.full_name;
        }
        return list;
    };

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        pre_add: app.pre_add,
        add_ticket: app.add_ticket,
        close_modal: app.close_modal,
        assign_user: app.assign_user,
        redirect_ticket: app.redirect_ticket,
        submit_edit: app.submit_edit,
        change_status: app.change_status,
        cancel_edit: app.cancel_edit
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        axios.get(get_ticket_by_id_url).then((result) => {
            app.data.ticket = result.data.ticket;

            app.set_fields(result.data.ticket);

            app.data.selected_tags = app.data.ticket.tag_list.map((e) => {
                e.label = e.tag_name;
                return e;
            });

        });
        axios.get(get_all_tags).then((result) => {
            app.data.tag_options = result.data.tags.map((e) => {
                e.label = e.tag_name;
                return e;
            });
            return axios.post(get_users_by_tag_list_url, {tag_list: app.data.selected_tags})
        }).then((result) => {
            app.data.possible_users = app.reindex(result.data.users);
        });
        axios.get(get_all_progress).then((result) => {
           app.data.status_strings = result.data.valid_statuses;
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);

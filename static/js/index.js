// vanilla javascript for tracking if click is registered outside of object

Vue.directive('click-outside', {
    bind(el, binding, vnode) {
        var vm = vnode.context;
        var callback = binding.value;

        el.clickOutsideEvent = function (event){
            if (!(el === event.target || el.contains(event.target))) {
                return callback.call(vm, event);
            }
        };
        document.body.addEventListener('click', el.clickOutsideEvent);
    },
    unbind(el) {
        document.body.removeEventListener('click', el.clickOutsideEvent);
    }
});


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
        tickets: [],
        add_ticket_text:  "",
        add_ticket_title:  "",
        add_ticket_priority: "",
        add_ticket_status: "",
        is_add_empty: false,
        page: 'list',
        showModal: false,
        selectedIdx: false,
        submitCallback: null,
        cancelCallback: null,
        searchText: "",
        selected_ticket: {},
        // Complete.
    };

    // Add here the various functions you need.
    app.add_ticket = () => {
        app.data.submitCallback = app.submit_add;
        app.data.cancelCallback = app.close_modal;
        app.data.selected_ticket = {};
        app.data.showModal = true;
    };

    app.submit_add = () => {
        let error = false;
        console.log(app.data.selected_ticket);
        if(!app.check_ticket_text()) {
            // do a post request
            let ticket = {
                ticket_title: app.data.add_ticket_title,
                ticket_text: app.data.add_ticket_text,
                ticket_status: app.data.add_ticket_status,
                ticket_priority: app.data.add_ticket_priority,
                ticket_author: app.data.username
            };

            axios.post(add_tickets_url, ticket).then((response) => {
                ticket.id = response.data.id;
                app.data.tickets.unshift(ticket);
                app.reindex(app.data.tickets);
                app.reset_input();
                app.data.showModal = false;
                app.data.submitCallback = false;
            }).catch((error) => {
                console.log(error);
            });
        }
    };

    app.edit_ticket = (ticket_idx) => {
       app.data.selectedIdx = ticket_idx;
       let selected = app.data.tickets[ticket_idx];

       if(selected !== false) {
           app.data.add_ticket_text = selected.ticket_text;
           app.data.add_ticket_title = selected.ticket_title;
           app.data.add_ticket_status = selected.ticket_status;
           app.data.add_ticket_priority = selected.ticket_priority;
       }

       app.data.submitCallback = app.submit_edit;
       app.data.showModal = true;
    };

    app.submit_edit = () => {
        console.log(app.data.selectedIdx);
        let idx = app.data.selectedIdx;
        if(idx !== false) {
            let ticket = app.data.tickets[idx];

            ticket = {
                id: ticket.id,
                ticket_title: app.data.add_ticket_title,
                ticket_text: app.data.add_ticket_text,
                ticket_status: app.data.add_ticket_status,
                ticket_priority: app.data.add_ticket_priority,
                ticket_author: ticket.ticket_author,
            };

            axios.post(edit_ticket_url, ticket).then((response) => {
                app.data.tickets[idx] = ticket; // only reassign if post was successful
                app.reset_input();
                app.data.showModal = false;
            }).catch((error) => {
                console.log(error);
            });
        }
    };

    app.reset_input = () => {
        app.data.add_ticket_text = "";
        app.data.add_ticket_title = "";
        app.data.add_ticket_priority = "";
        app.data.add_ticket_status = "";
        app.vue.is_add_empty = false;
    };

    app.check_ticket_text = () => {
       return (app.vue.add_ticket_text.trim().length === 0);
    };


    app.delete_ticket = (ticket_idx) => {
        let t = app.vue.tickets[ticket_idx];

        axios.post(delete_tickets_url, {id:t.id}).then(() => {
            app.vue.tickets.splice(ticket_idx, 1);
            app.reindex(app.vue.tickets);
        })
    };

    app.close_modal = () => {
        app.data.selectedIdx = false;
        app.reset_input();
        app.data.showModal = false;
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

    app.filterList = (event) => {
        app.data.tickets.filter(ticket => ticket.ticket_text.includes(app.data.searchText));
    };

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        // Complete.
        goto: app.goto,
        add_ticket: app.add_ticket,
        check_ticket_text: app.check_ticket_text,
        delete_ticket: app.delete_ticket,
        edit_ticket: app.edit_ticket,
        close_modal: app.close_modal,
        submit_add: app.submit_add,
        filterList: app.filterList,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        axios.get(get_tickets_url).then((result) => {
            let tickets = result.data.tickets;
            app.reindex(tickets);
            app.vue.tickets = tickets;

        })
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);

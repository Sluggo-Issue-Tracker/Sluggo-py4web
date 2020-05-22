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
        master: [],
        page: 'list',
        showModal: false,
        selectedIdx: false,
        submitCallback: null,
        cancelCallback: null,
        searchText: "",
        searchTag: "",
        searchStatus: "",
        selected_ticket: {},
        tagList: ["", "hello", "there"],
        tagString: "",
        placeHolder: "tag",
        ticket_tags: [],
        // Complete.
    };

    // Add here the various functions you need.
    app.add_ticket = () => {
        // this initializes the modal to handle adding
        app.data.submitCallback = app.submit_add;
        app.data.selected_ticket = {show: false, tag_list: []};
        app.data.showModal = true;
    };

    app.submit_add = () => {
        let error = false;
        let ticket = app.data.selected_ticket;
        if(app.check_ticket_text(ticket)) {
            // do a post request
            axios.post(add_tickets_url, ticket).then((response) => { // TODO: Sam 5 / 22 / 2020 implement tag submission
                ticket.id = response.data.id;
                app.data.tickets.unshift(ticket);
                app.reindex(app.data.tickets);
                app.data.showModal = false;
                app.data.submitCallback = null;
            }).catch((error) => {
                console.log(error);
            });
        }
    };

    app.edit_ticket = (ticket_idx) => {
        // this initializes the modal to handle editing
        app.data.submitCallback = app.submit_edit;
        let ticket = app.data.tickets[ticket_idx];

        if(ticket !== false) {
            app.data.selected_ticket = {
                _idx: ticket._idx,
                id: ticket.id,
                ticket_title: ticket.ticket_title,
                ticket_text: ticket.ticket_text,
                ticket_priority: ticket.ticket_priority,
                ticket_status: ticket.ticket_status
            };
            app.data.showModal = true;
        }
    };

    app.submit_edit = () => {
        console.log(app.data.selected_ticket);
        let ticket = app.data.selected_ticket;

        if(ticket !== false) {

            axios.post(edit_ticket_url, ticket).then((response) => {
                let old_ticket = app.data.tickets[ticket._idx];

                old_ticket.ticket_title = ticket.ticket_title;
                old_ticket.ticket_text = ticket.ticket_text;
                old_ticket.ticket_priority = ticket.ticket_priority;
                old_ticket.ticket_status = ticket.ticket_status;

                app.reindex(app.data.tickets);
            }).catch((error) => {
                console.log(error);
            });

        }

        app.data.showModal = false;
    };

    app.check_ticket_text = (ticket) => {
      return (ticket.ticket_text.trim().length > 0 &&
              ticket.ticket_title.trim().length > 0 &&
              ticket.ticket_status.trim().length > 0 &&
              ticket.ticket_priority.trim().length > 0);
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
        app.data.showModal = false;
    };


    // Use this function to reindex the posts, when you get them, and when
    // you add / delete one of them.
    app.reindex = (a) => {
        let idx = 0;
        for (p of a) {
            p._idx = idx++;
            p.show = false;
        }
        return a;
    };

    app.filter_list = () => {
        app.data.tickets = app.data.master.filter((ticket) => {
            return ticket.ticket_text.toLowerCase().includes(app.data.searchText.trim().toLowerCase()) ||
                   ticket.ticket_title.toLowerCase().includes(app.data.searchText.trim().toLowerCase()) ||
                   ticket.ticket_status.toLowerCase().includes(app.data.searchText.trim().toLowerCase()) ||
                   ticket.ticket_priority.toLowerCase().includes(app.data.searchText.trim().toLowerCase());
        });
    };

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        // Complete.
        add_ticket: app.add_ticket,
        check_ticket_text: app.check_ticket_text,
        delete_ticket: app.delete_ticket,
        edit_ticket: app.edit_ticket,
        close_modal: app.close_modal,
        submit_add: app.submit_add,
        filter_list: app.filter_list,
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
            app.vue.master = tickets;
            app.vue.tickets = app.vue.master;
            app.vue.ticket_tags = result.data.ticket_tags
        })
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);

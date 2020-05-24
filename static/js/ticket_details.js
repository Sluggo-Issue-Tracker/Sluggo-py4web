
Vue.component('v-select', VueSelect.VueSelect);

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
        ticket : { // this is the main object
            id: "",
            ticket_title: "",
            ticket_description: "",
            ticket_author: "",
            created: "",
            started: "",
            completed: "",
            tag_list: [],
            sub_tickets: [],
        },
        new_ticket: {},
        show_modal: false,
        tag_options: ["hello"],
        selected_tags: [],

        assigned: "No one has been assigned", // going to be the string for the assigned user
        edit: false,
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
            parent_id: app.data.ticket.id
        };
        app.data.show_modal = true;
    };

    app.add_ticket = () => {
        axios.post(add_sub_ticket_url, app.data.new_ticket).then((response) => {
           app.data.ticket.sub_tickets.unshift(response.data.ticket);
        }).catch((error) => {
            console.log(error);
        });
        app.close_modal();
    };

    app.close_modal = () => {
        app.data.show_modal = false;
        app.data.new_ticket = {};
    };

    app.assign = (user) => {
        // TODO: implement this
    };

    app.redirect = (id) => {
        window.location.href = tickets_details_url + '/' + id;
    };

    app.do_edit = () => {
        app.data.edit = true;
    };

    app.submit_edit = () => {
        axios.post(edit_ticket_url, app.data.ticket).then((response) => {
            console.log(response)
        }).catch((error) => {
            console.log(error);
        });

        app.data.edit = false;
    };

    app.remove_tag = (idx) => {
        tag = app.data.selected_tags[idx];

        if(tag !== false){
            axios.post(delete_tag_url,{
                tag_id: tag.id,
                ticket_id: app.data.ticket.id
            }).then((result) => {
                console.log(result.data.handle);
                app.data.selected_tags.splice(idx, 1);
            }).catch((error) => {
                console.log(error);
            })
        }
    };

    app.reindex = (list) => {
        let i = 0;
        for(let l of list) {
            l._idx = i++;
        }
        return list;
    };

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        pre_add: app.pre_add,
        add_ticket: app.add_ticket,
        close_modal: app.close_modal,
        assign: app.assign,
        redirect: app.redirect,
        do_edit: app.do_edit,
        submit_edit: app.submit_edit,
        remove_tag: app.remove_tag
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
            app.data.selected_tags = app.data.ticket.tag_list.map(e => e.tag_name);
            return axios.get(get_all_tags)
        }).then((result) => {
            app.data.tag_options = result.data.tags.map(e => e.tag_name);
        })
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);

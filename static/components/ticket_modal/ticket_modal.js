Vue.component('v-select', VueSelect.VueSelect);

(function() {

    let ticket_modal = {
        props: {'ticket': Object, 'options': Array, 'users': Array},
        data: null,
        methods: {}
    };

    ticket_modal.data = function(){

        return {
            priority_list: [],
            status_list: [],
            selected: [],
            date: "",
            due_date: "",
            assigned_user: "",
            time_zone: luxon.DateTime.local().zoneName
        };
    };

    ticket_modal.methods.submit = function () {
        let i = 0;
        for(let a of this.selected) {
            this.ticket.tag_list.unshift(a);
        }

        this.ticket.due_date = this.due_date;
        this.ticket.assigned_user = this.assigned_user;
        this.$emit('submit');
    };

    ticket_modal.methods.close = function () {
        this.$emit('cancel');
    };

    utils.register_vue_component('ticket-modal', 'components/ticket_modal/ticket_modal.html',
        function(template) {
            ticket_modal.template = template.data;
            return ticket_modal;
        });
})();
Vue.component('v-select', VueSelect.VueSelect);

(function() {

    let ticket_modal = {
        props: {'ticket': Object, 'options': Array},
        data: null,
        methods: {}
    };

    ticket_modal.data = function(){

        let data = {
            priority_list: [],
            status_list: [],
            selected: [],
        };

        ticket_modal.methods.load.call(data);
        return data;
    };

    ticket_modal.methods.load = function () {
        // potentially have this do a get request in the event that we want custom statuses
    };

    ticket_modal.methods.submit = function () {
        let i = 0;
        for(let a of this.selected) {
            this.ticket.tag_list.unshift({tag_name: a});
        }
        console.log(this.ticket.tag_list);
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
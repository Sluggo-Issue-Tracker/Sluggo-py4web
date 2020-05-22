(function() {
    let ticket_modal = {
        props: {'ticket': Object},
        data: null,
        methods: {}
    };

    ticket_modal.data = function(){

        let data = {
            priority_list: [],
            status_list: [],
        };

        ticket_modal.methods.load.call(data);
        return data;
    };

    ticket_modal.methods.load = function () {
        // potentially have this do a get request in the event that we want custom statuses
        this.status_list = ["To do", "In progress", "Completed"];
        this.priority_list = ["Done Yesterday", "High Priority", "Meh", "Take your time"];
    };

    ticket_modal.methods.submit = function () {
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
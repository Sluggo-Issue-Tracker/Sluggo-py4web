Vue.component('v-select', VueSelect.VueSelect);

(function() {

    let add_subticket_modal = {
        props: {'selected': Object, 'options': Array},
        data: null,
        methods: {}
    };

    add_subticket_modal.data = function(){
        return {
            ticket: null,
        };
    };

    add_subticket_modal.methods.submit = function() {
        this.selected.id = this.ticket.id;
        this.$emit('submit');
    };

    add_subticket_modal.methods.close = function() {
        this.$emit('cancel')
    };

    utils.register_vue_component('add-subticket-modal', 'components/add_subticket_modal/add_subticket_modal.html',
        function(template) {
            add_subticket_modal.template = template.data;
            return add_subticket_modal;
        });
})();

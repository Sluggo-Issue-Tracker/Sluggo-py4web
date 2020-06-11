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
            error: false,
            time_zone: luxon.DateTime.local().zoneName
        };
    };

    ticket_modal.methods.sleep = function(ms) {
        return function (x) {
            return new Promise(resolve => setTimeout(() => resolve(x), ms));
        };
    };
    
    
    // the data can either come in mm / dd / yyyy (on mac) or
    // yyyy-mm-dd because using normal things is not the safari way
    // so we have a function that handles that hogwash for us
    /*ticket.methods.check_date = function(input) {
        let month, day, year, invalid;
        month = day = year = 0;
        invalid = false;
    }*/

    ticket_modal.methods.check_date = function(date) {
        let month, day, year;
        let invalid = true;
        console.log(date);
        console.log(date.match("/\/|\-/g"));

    }

    ticket_modal.methods.submit = function () {
        let i = 0;
        for(let a of this.selected) {
            this.ticket.tag_list.unshift(a);
        }

        ticket_modal.methods.check_date(this.due_date);

        let date = this.due_date ? luxon.DateTime.fromSQL(this.due_date) : this.due_date;
        if(!this.ticket.ticket_title || this.ticket.ticket_title.length === 0 || date.invalid) {
            this.error = true;
            this.sleep(2000)().then(() => {
                this.error = false;
            });
            return;
        }

        // TODO: convert the timestamp
        this.ticket.due_date = date ? date.setZone("utc").toString() : date;
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
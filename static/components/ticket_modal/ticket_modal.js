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
            text_error: false,
            date_error: false,
            title_type_error: false,
            text_type_error: false,
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
    ticket_modal.methods.check_date = function(date) {
        let month, day, year;
        month = day = year = null;

        format = date.match(/[\/-]/g);

        if(format && format.length === 2 && format[0] === format[1]) {
            date_array = date.split(format[0]);

            if(date_array.length === 3) {
                if(format[0] === "/")
                    date_array.unshift(date_array.pop());

                year = parseInt(date_array[0]);
                month = parseInt(date_array[1]);
                day = parseInt(date_array[2]);

            }
        }

        return luxon.DateTime.local(year, month, day);
    };

    ticket_modal.methods.submit = function () {
        let i = 0;
        let error = false;
        for(let a of this.selected) {
            this.ticket.tag_list.unshift(a);
        }

        date = this.due_date ? ticket_modal.methods.check_date(this.due_date) : this.due_date;
        if(date.invalid) {
            this.date_error = true;
            this.sleep(2000)().then(() => {
                this.date_error = false;
            });
            error = true;
        }

        if(!this.ticket.ticket_title || this.ticket.ticket_title.length === 0) {
            this.text_error = true;
            this.sleep(2000)().then(() => {
                this.text_error = false;
            });
            error = true;
        }

        if(sluggo.checkNameString(this.ticket.ticket_title) === false) {
            this.title_type_error = true;
            this.sleep(2000)().then(() => {
                this.title_type_error = false;
            });
            error = true;

        }

        if(sluggo.checkNameString(this.ticket.ticket_text) === false) {
            this.text_type_error = true;
            this.sleep(2000)().then(() => {
                this.text_type_error = false;
            });
            error = true;

        }
        if(!error) {

            // TODO: convert the timestamp
            this.ticket.due_date = date ? date.setZone("utc").toString() : date;
            this.ticket.assigned_user = this.assigned_user;

            this.$emit('submit');
        }
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

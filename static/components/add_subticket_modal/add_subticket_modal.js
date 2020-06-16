/*
    add_subticket_modal.js - JavaScript code for subticket modal component
    part of Sluggo, a free and open source issue tracker
    Copyright (c) 2020 Slugbotics - see git repository history for individual committers

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at https://mozilla.org/MPL/2.0/.
*/

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
            error: false
        };
    };

    add_subticket_modal.methods.sleep = function(ms) {
        return function (x) {
            return new Promise(resolve => setTimeout(() => resolve(x), ms));
        };
    };

    add_subticket_modal.methods.submit = function() {
        if(!this.ticket) {
            this.error = true;
            this.sleep(2000)().then(() => {
                this.error = false;
            });
            return;
        }
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

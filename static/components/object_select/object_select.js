(function() {

    // the idea is to have selected and options lists and also have add and remove callbacks
    // so the calls become easier
    // also v-select is buttfuck ugly

    let object_select = {

    };

    object_select.data = function(){

    };

    object_select.methods.load = function () {
        // potentially have this do a get request in the event that we want custom statuses
    };

    object_select.methods.submit = function () {
        this.$emit('submit');
    };

    object_select.methods.close = function () {
        this.$emit('cancel');
    };

    utils.register_vue_component('object-select', 'components/object_select/object_select.html',
        function(template) {
            object_select.template = template.data;
            return object_select;
        });
})();

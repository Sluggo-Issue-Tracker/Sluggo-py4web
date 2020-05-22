(function() {
    let dropdown = {
        props: {'list': Array, 'result': String, 'placeholder': String},
        data: null,
        methods: {}
    };

    dropdown.data = function () {
        let data = {
            show: false,
            selected: this.placeholder
        };

        return data;
    };

    dropdown.methods.select = function (selection) {
        this.result = selection;
        if(selection.length === 0)
            selection = this.placeholder;
        this.selected = selection;
        this.show = false;
    };

    dropdown.methods.close = function () {
        if(this.show === true) {
            this.result = "";
            this.show = false;
        }
    };

    utils.register_vue_component('dropdown', 'components/dropdown/dropdown.html',
        function(template) {
            dropdown.template = template.data;
            return dropdown;
        });

})();

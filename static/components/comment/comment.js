(function() {
    let comment = {
        props: {'get-url': String, 'add-url': String},
        data: null,
        methods: {}
    };

    comment.data = function () {
        let data = {
            new_comment: "",
            comments: [],
            edit: false,
            show_settings: false,
        };

        this.load.call(data);
        return data;
    };

    comment.methods.load = function() {
        // dynamically attach comment information

    };

    comment.methods.cancel = function() {
        // clears the new comment text area
        this.new_comment = "";
        this.edit = false;
    };

    comment.methods.submit = function() {
        // submit the newly added comment to the backend, then add to the comments list
        this.new_comment = "";
        this.edit = false;
    };

    comment.methods.edit_comment = function() {
        // prepare the comment for editing, if necessary
        // gotta set the edit flag for the currently selected ticket, maybe the submit functionality will be separate
        // after all
        this.show_settings = false;
    };

    comment.methods.delete_comment = function() {
        // delete the comment
        this.show_settings = false;
    };

    utils.register_vue_component('comment', 'components/comment/comment.html',
        function(template) {
            comment.template = template.data;
            return comment;
        });

})();

(function() {
    let comment = {
        props: {'get_url': String,
                'add_url': String,
                'edit_url': String,
                'delete_url': String},
        data: null,
        methods: {}
    };

    comment.data = function () {
        let data = {
            new_comment: "",
            comments: [],
            edit: false,
            show_settings: false,
            get_url: this.get_url,
            add_url: this.add_url,
            edit_url: this.edit_url,
            delete_url: this.delete_url,
        };

        data = comment.methods.load(data);
        return data;
    };

    comment.methods.load = function(data) {
        // dynamically attach comment information
        axios.get(data.get_url).then((result) => {
            data.comments = result.data.comments;

            let _idx = 0;
            for(let c of data.comments) {
                c._idx = _idx++;
                c.show_settings = false;
            }
        });
        return data;
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

    comment.methods.edit_comment = function(idx) {
        // prepare the comment for editing, if necessary
        // gotta set the edit flag for the currently selected ticket, maybe the submit functionality will be separate
        // after all
        this.comments[idx].show_settings = false;
    };

    comment.methods.delete_comment = function(idx) {
        // delete the comment
        this.comments[idx].show_settings = false;
    };

    utils.register_vue_component('comment', 'components/comment/comment.html',
        function(template) {
            comment.template = template.data;
            return comment;
        });

})();

(function() {
    let comment = {
        props: {'get_url': String,
                'add_url': String,
                'edit_url': String,
                'delete_url': String,
                'ticket_id': String},
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
            error: false,
            text_type_error: false,
        };

        data = comment.methods.load(data);
        return data;
    };

    comment.methods.reindex = function(comments) {
        let _idx = 0;
        for(let c of comments) {
            c._idx = _idx++;
            c.show_settings = false;
            c.edit = false;
            c.error = false;
            c.text_type_error = false;
        }
        return comments;
    };

    comment.methods.load = function(data) {
        // dynamically attach comment information
        axios.get(data.get_url).then((result) => {
            data.comments = result.data.comments;
            data.comments = comment.methods.reindex(data.comments);
        });
        return data;
    };

    comment.methods.cancel = function() {
        // clears the new comment text area
        this.new_comment = "";
        this.edit = false;
    };

    comment.methods.toggle = function(idx) {
        // using this blasphemy because the vue doesn't detect changes to array elements
        let selected = this.comments[idx];
        selected.show_settings = !selected.show_settings;
        this.comments.splice(idx, 1, selected);
    };

    comment.methods.sleep = function(ms) {
        return function (x) {
            return new Promise(resolve => setTimeout(() => resolve(x), ms));
        };
    };

    comment.methods.submit = function() {
        // submit the newly added comment to the backend, then add to the comments list
        if (!this.new_comment || this.new_comment.length === 0) {
            this.error = true;
            this.sleep(2000)().then(() => {
                this.error = false;
            });
            return;
        }

        if (!this.new_comment || sluggo.checkNameString(this.new_comment) === false) {
            this.text_type_error = true;
            this.sleep(2000)().then(() => {
                this.text_type_error = false;
            });
            return;
        }



        axios.post(this.add_url, {
            content: this.new_comment,
            ticket_id: this.ticket_id
        }).then((result) => {
            this.comments.push({
                content: this.new_comment,
                id: result.data.id,
                first_name: result.data.first_name,
                last_name: result.data.last_name,
                editable: true,
                img_url: result.data.img_url
            });
            this.comments = comment.methods.reindex(this.comments);
            this.new_comment = "";
        });
        this.edit = false;
    };



    comment.methods.edit_comment = function(idx) {
        // prepare the comment for editing, if necessary
        // gotta set the edit flag for the currently selected ticket, maybe the submit functionality will be separate
        // after all
        comment.methods.toggle.call(this,idx);
        let selected = this.comments[idx];
        selected.edit = true;
        selected.new_content = selected.content;
        this.comments.splice(idx, 1, selected);
    };

    comment.methods.cancel_edit = function(idx) {
        let selected = this.comments[idx];
        selected.edit = false;
        selected.new_content = "";
        this.comments.splice(idx, 1, selected);
    };

    comment.methods.submit_edit = function(idx) {
        let selected = this.comments[idx];

        if(!selected.new_content || selected.new_content.length === 0) {
            selected.error = true;
            this.comments.splice(idx, 1, selected);
            this.sleep(2000)().then(() => {
                selected.text_type_error = false;
                this.comments.splice(idx, 1, selected);
            });
            return;
        }
        if (sluggo.checkNameString(selected.new_content) === false) {
            selected.text_type_error = true;
            this.comments.splice(idx, 1, selected);
            this.sleep(2000)().then(() => {
                selected.text_type_error = false;
                this.comments.splice(idx, 1, selected);
            });
            return;
        }

        axios.post(this.edit_url, {
            comment_id: selected.id,
            content: selected.new_content
        }).then((result) => {
            selected.content = selected.new_content;
            selected.new_content = "";
            selected.edit = false;
            this.comments.splice(idx, 1, selected);
        });
    };

    comment.methods.delete_comment = function(idx) {
        // delete the comment
        comment.methods.toggle.call(this,idx);
        axios.post(this.delete_url, {
            comment_id:  this.comments[idx].id
        }).then((result) => {
            this.comments.splice(idx, 1);
            this.comments = comment.methods.reindex(this.comments);
        });
    };

    utils.register_vue_component('comment', 'components/comment/comment.html',
        function(template) {
            comment.template = template.data;
            return comment;
        });

})();

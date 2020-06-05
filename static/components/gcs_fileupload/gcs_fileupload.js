(function(){

    var uploader = {
        props: ['callback_url', 'obtain_gcs_url', 'notify_url', 'delete_url'],
        data: null,
        methods: {}
    };

    uploader.data = function() {
        var data = {
            my_obtain_gcs_url: this.obtain_gcs_url,
            my_notify_url: this.notify_url,
            my_callback_url: this.callback_url,
            my_delete_url: this.delete_url,
            // File information
            file_name: "",
            file_date: "",
            file_info: "", // Displayable to the user.
            file_id: "", // Id of the file to talk to the server.
            download_url: null, // Used to download the file.
            // Operation control
            writable: false,
            deletable: false,
            // Phases: upload
            uploading: false,
            fileerror: false,
            // Phases: deletion
            delete_confirmation: false,
            deleting: false,
        };
        uploader.methods.load.call(data);
        return data;
    };

    uploader.methods.load = function () {
        let self = this;
        axios.get(self.my_callback_url).then(function(res) {
            set_results(self, res);

        });

    };

    function set_results(self, res) {
        self.writable = res.data.writable;
        self.deletable = res.data.deletable;
        self.download_url = res.data.download_url;
        self.file_id = res.data.file_id;
        self.file_name = res.data.file_name;
        self.file_date = res.data.file_date;

        if (self.file_date) {
            let d = new Sugar.Date(self.file_date + "Z");
            self.file_info = self.file_name + ", uploaded on " + d.long();
        } else {
            self.file_info = self.file_name;
        }
    }

    uploader.methods.upload_file = function (event) {
        let self = this;
        // Reads the file.
        let input = event.target;
        let file = input.files[0];
        if (file) {
            self.uploading = true;
            let file_type = file.type;
            let file_name = file.name;
            // Requests the upload URL.
            axios.post(self.my_obtain_gcs_url, {action: "PUT", mimetype: file_type})
                .then ((res) => {
                    let upload_url = res.data.signed_url;
                    let file_path = res.data.path;
                    // Uploads the file, using the low-level interface.
                    let req = new XMLHttpRequest();
                    // We listen to the load event = the file is uploaded, and we call upload_complete.
                    // That function will notify the server `of the location of the image.
                    req.addEventListener("load", upload_complete(self, file_name, file_type, file_path));
                    // TODO: if you like, add a listener for "error" to detect failure.
                    req.open("PUT", upload_url, true);
                    req.send(file);
                }).catch((error) => {
                    self.uploading = false;
                    self.fileerror = true;
                    app.sleep(3000)()
                        .then(() => {
                            self.fileerror = false;
                    });

                    console.log(error);
                });
        }
    };

    function sleep(ms) {
        return function (x) {
            return new Promise(resolve => setTimeout(() => resolve(x), ms));
        };
    };


    function upload_complete(self, file_name, file_type, file_path) {
        axios.post(self.my_notify_url, {
            file_name: file_name,
            file_type: file_type,
            file_path: file_path})
            .then((res) => {
                self.uploading = false;
                set_results(self, res);

                self.$emit('download_url', self.download_url);
                console.log("Uploaded.");
            });
    }

    uploader.methods.delete_file = function () {
        let self = this;
        if (self.deletable) {
            let self = this;
            if (!self.delete_confirmation) {
                self.delete_confirmation = true;
            } else {
                self.delete_confirmation = false;
                self.deleting = true;
                // Obtains the delete URL.
                axios.post(self.my_obtain_gcs_url, {action: "DELETE", file_id: self.file_id})
                    .then((res) => {
                        let delete_url = res.data.signed_url;
                        let req = new XMLHttpRequest();
                        req.addEventListener("load", deletion_complete(self));
                        // TODO: if you like, add a listener for "error" to detect failure.
                        req.open("DELETE", delete_url);
                        req.send();
                    })
            }
        }
    };

    function deletion_complete(self) {
        // Confirms the deletion to the server.
        axios.post(self.my_delete_url, {file_id: self.file_id})
            .then((res) => {
                self.deleting = false;
                set_results(self, res);
                console.log("Deleted.");
            });
    }

    utils.register_vue_component('gcsfileupload', 'components/gcs_fileupload/gcs_fileupload.html', function(template) {
            uploader.template = template.data;
            return uploader;
        });
})();

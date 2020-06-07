(function() {

    let profile_uploader = {
        props: {'url': String, 'file_type': String, 'user': Number},
        data: null,
        methods: {}
    };

    profile_uploader.data = function(){

        return {
            fileerror: false,
            uploading: false,
            success: false,
            sizeerror: false,
            servererror: false
        };
    };


    profile_uploader.methods.upload_file = function (event) {
        let data = new FormData();
        let input = event.target;
        let file = input.files[0];




        let self = this;
        // Reads the file.

        if (file) {
            self.uploading = true;
            let file_type = file.type;
            let file_name = file.name;

            // If wrong filetype, tell the user and return
            if(!file_type.includes(self.file_type)) {
                self.uploading = false;
                self.fileerror = true;
                app.sleep(3000)()
                    .then(() => {
                        self.fileerror = false;
                });
                return;
            }

            // If the file is too large, tell the user and return
            if(file.size > 1000000) {
                self.uploading = false;
                self.sizeerror = true;
                app.sleep(3000)()
                    .then(() => {
                        self.sizeerror = false;
                });
                return;
            }


            data.append('name', file_name);
            data.append('file', file);
            data.append('id', self.user)

            let config = {
                header : {
                    'Content-Type' : 'multipart/form-data'
                }
            }

            axios.post(self.url, data, config)
            .then((response) => {
                self.uploading = false;
                self.success = true;
                app.sleep(2000)()
                        .then(() => {
                            self.success = false;

                    });
                self.submit();

            }).catch((error) => {
                self.uploading = false;
                self.servererror = true;
                app.sleep(2000)()
                        .then(() => {
                            self.servererror = false;
                    });
            });

        }
    };

    profile_uploader.methods.submit = function () {
            this.$emit('submit');
        };

    function sleep(ms) {
        return function (x) {
            return new Promise(resolve => setTimeout(() => resolve(x), ms));
        };
    };

    utils.register_vue_component('profile_uploader', 'components/profile_uploader/profile.html',
        function(template) {
            profile_uploader.template = template.data;
            return profile_uploader;
        });
})();

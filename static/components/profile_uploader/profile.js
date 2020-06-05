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

            if(!file_type.includes(self.file_type)) {
                self.uploading = false;
                self.fileerror = true;
                app.sleep(3000)()
                    .then(() => {
                        self.fileerror = false;
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
                self.submit();
            }).catch((error) => {
                self.uploading = false;
                self.fileerror = true;
                app.sleep(3000)()
                        .then(() => {
                            self.fileerror = false;
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

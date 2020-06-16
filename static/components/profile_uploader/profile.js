/*
    profile.js - JavaScript code for user profiles component
    part of Sluggo, a free and open source issue tracker
    Copyright (c) 2020 Slugbotics - see git repository history for individual committers

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at https://mozilla.org/MPL/2.0/.
*/

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
			servererror: false,
			dimensionerror: false,
			error: false,
			error_text: ""
		};
	};

	function sleep(ms) {
		return function (x) {
			return new Promise(resolve => setTimeout(() => resolve(x), ms));
		};
	};


	function loadImage(url) {
		return new Promise((resolve, reject) => {
			let img = new Image();
			img.addEventListener('load', e => resolve(img));
			img.addEventListener('error', () => {
				reject(new Error(`Failed to load image's URL: ${url}`));
			});
			img.src = url;
		});
	}

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
				self.success = false;
				self.error = true;
				self.error_text = "Wrong Filetype";
				app.sleep(3000)()
				.then(() => {
					self.error = false;
					self.error_text = "";
				});
				return;
			}


			// If the file is too large or small, tell the user and return
			if(file.size > 10000000 || file.size <= 0) {
				self.uploading = false;
				self.success = false;
				self.error = true;
				self.error_text = "File Too Large (10MB Limit)";
				app.sleep(3000)()
				.then(() => {
					self.error = false;
					self.error_text = "";
				});
				return;
			}

			var reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onload = evt => {
				let img = new Image();
				img.onload = () => {

					// If the file is not a square error
					if(img.width != img.height) {
						self.uploading = false;
						self.success = false;
						self.error = true;
						self.error_text = "File must be Exact Square";
						app.sleep(3000)()
						.then(() => {
							self.error = false;
							self.error_text = "";
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
						self.error = false;
						self.success = true;
						app.sleep(2000)()
						.then(() => {
							self.success = false;

						});
						self.submit();

					}).catch((error) => {
						self.uploading = false;
						self.success = false;
						self.error = true;
						self.error_text = " Server Error Occured";
						app.sleep(3000)()
						.then(() => {
							self.error = false;
							self.error_text = "";
						});
					});
				}
				img.src = evt.target.result;
			}


		}
	};

	profile_uploader.methods.submit = function () {
		this.$emit('submit');
	};






	utils.register_vue_component('profile_uploader', 'components/profile_uploader/profile.html',
		function(template) {
			profile_uploader.template = template.data;
			return profile_uploader;
		});
})();

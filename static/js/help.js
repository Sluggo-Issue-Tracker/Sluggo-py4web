/*
    help.js - JavaScript code for help page
    part of Sluggo, a free and open source issue tracker
    Copyright (c) 2020 Slugbotics - see git repository history for individual committers

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at https://mozilla.org/MPL/2.0/.
*/

VALID_HELP_PAGENAMES = [
    "usage",
    "attribution"
]
// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
 app.data = {
    page: "start_view",
    pageData: {},
    loadedPages: []
};

app.reindex = (a) => {
    let idx = 0;
    for (p of a) {
        p._idx = idx++;
    }
    return a;
};

app.goto = (page) => {
    app.data.page = page;
    if((page !== 'start_view') && !(app.data.loadedPages.includes(page))) {
        app.get(page);
    }
};

app.get = (pageName) => {
    return new Promise(function(resolve, reject) {
        if(!app.data.loadedPages.includes(pageName)) {
            reject("invalid-pagename");
        }

        // make a GET request to the server
        axios.get(base_url + 'get_help_page/' + pageName).then(function (response) {
            if(response.status === 200) {
                app.data.pageData[pageName] = marked(response.data);
                app.data.loadedPages.push(pageName);
            }
        }).catch(function (error) {
            alert(error);
        })
    })
}

app.methods = {
    goto : app.goto,
    get: app.get
};

app.vue = new Vue({
    el: "#help-target",
    data: app.data,
    methods: app.methods
});

app.init = () => {
    console.log(base_url);
    for(pageName of VALID_HELP_PAGENAMES) {
        Vue.set(app.data.pageData, pageName, "Loading...");
    }
};

app.init();
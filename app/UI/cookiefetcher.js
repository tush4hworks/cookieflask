
const idp_select = document.querySelector("#baseurl");
const user_select = document.querySelector("#username");
const pass_select = document.querySelector("#password");
const user_finder_select = document.querySelector("#username_finder_findby");
const pass_finder_select = document.querySelector("#password_finder_findby");
const button_finder_select = document.querySelector("#button_finder_findby");
const user_finder_find = document.querySelector("#username_to_find");
const pass_finder_find = document.querySelector("#password_to_find");
const button_finder_find = document.querySelector("#button_to_find");
const cookie_select = document.querySelector("#cookie_filter");
const output_div = document.querySelector('#output');
//let params = new Array();
//params.push(idp_select, user_select, user_finder_find, user_finder_select, pass_select, pass_finder_find, button_finder_select, pass_finder_select, button_finder_find);


function status(response) {
    if (response.status >= 200 && response.status < 300) {
        console.log(response.statusText);
        console.log(response.status);
        return Promise.resolve(response)
    } else {
        return Promise.reject(new Error(response.statusText))
    }
};

class CookieRequest {
    constructor(baseurl, username, password) {
        this.baseurl = baseurl
        this.username = username
        this.password = password
    };
    setUserFinder = userfinder => this.username_finder = userfinder;
    setPasswordFinder = passwordfinder => this.password_finder = passwordfinder;
    setButtonFinder = btnFinder => this.button_finder = btnFinder;

};

class Finder {
    constructor(findby, value) {
        this.findby = findby;
        this.value = value;
    }
};

showLoadingGif = () => {
    document.querySelector("#loading").style.display = 'block';
};

hideLoadingGif = () => {
    document.querySelector("#loading").style.display = 'none';
};

console.log(document.querySelector("#cookieOne"));

document.querySelector("#cookieOne").addEventListener("click", fetchOneCookie);
document.querySelector("#cookieAll").addEventListener("click", fetchAllCookies);

function getHtmlCookieContent(data) {
    console.log(data);
    let obj_keys = Object.keys(data);
    let obj_values = Object.values(data);
    let d = '';
    for (let i = 0; i < obj_keys.length; i++) {
        d += `<li>${obj_keys[i]}: ${obj_values[i]}</li>`;
    };
    return d;
};


function displayCookies(data, color) {
    output_div.style.color = color;
    if (typeof data === 'string') {
        output_div.textContent = data;
    } else if (typeof data === 'object') {
        output_div.appendChild(document.createTextNode(JSON.stringify(data)));
    }
};


function cookiefetch(url) {
    output_div.innerHTML = '';
    let requestObj = new CookieRequest(idp_select.value, user_select.value, pass_select.value);
    requestObj.setUserFinder(new Finder(user_finder_select.value, user_finder_find.value));
    requestObj.setPasswordFinder(new Finder(pass_finder_select.value, pass_finder_find.value));
    requestObj.setButtonFinder(new Finder(button_finder_select.value, button_finder_find.value));
    console.log(JSON.stringify(requestObj));
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(requestObj)
    }).then(status)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            hideLoadingGif();
            displayCookies(data, 'green');
        })
        .catch(err => {
            console.log(err);
            hideLoadingGif();
            displayCookies(`${err.message}: ${err.name}: ${err.stack}` , 'red');
        });
    console.log('After fetch block!');
    showLoadingGif();
    //document.querySelector("#inputForm").reset();
};

function fetchOneCookie(e) {
    e.preventDefault();
    cookiefetch(`/fetch/api/cookie/${cookie_select.value}`);
};

function fetchAllCookies(e) {
    e.preventDefault();
    cookiefetch(`/fetch/api/cookie`);
};
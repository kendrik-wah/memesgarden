var cookieValues = {};

function checkCookies() {

  var currDate = new Date();
  var cookie = document.cookie;
  var cookieEntries = cookie.split(';');
  

  cookieEntries.forEach(function (cookieValue) {
    var lst = cookieValue.split("=");
    cookieValues[lst[0]] = lst[1];
  });

  // setTimeout(function(){
  //   var now = new Date();
  //   console.log(now - currDate);
  // }, 10000);


  // if (cookieValues.email !== undefined) {

  //   var lastLogin = cookieValues.last_login_date;

  // }

}

function setCookies(email, name) {
  console.log(email);
  console.log(name);

  var date = new Date();
  var cookie = document.cookie;
  var cookieEntries = cookie.split(';');
  
  cookieValues['email'] = email;
  cookieValues['name'] = name;
  cookieValues['last_login_date'] = date;

}

function logOut() {
  
}
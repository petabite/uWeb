//random js
function post() {

  var xhr = new XMLHttpRequest();
  xhr.open("POST", 'http://0.0.0.0:8080', true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify({"username":"xyz","password":"xyz"}));
}

let switch_ = document.getElementById("flexSwitchCheckDefault");
let body = document.getElementById("body")

switch_.addEventListener('change', function() {
    if (this.checked) {
      console.log("Checkbox is checked..");
      body.style.backgroundColor = "#222831"
    } else {
      console.log("Checkbox is not checked..");
      body.style.backgroundColor = "#DDDDDD"
    }
  });